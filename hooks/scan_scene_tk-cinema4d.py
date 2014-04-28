"""
Copyright (c) 2013 Shotgun Software, Inc
----------------------------------------------------

"""

import os
import c4d

from tank import Hook
from tank import TankError


class ScanSceneHook(Hook):
    """
    Hook to scan scene for items to publish
    """

    def execute(self, **kwargs):
        """
        Main hook entry point
        :returns:       A list of any items that were found to be published.
                        Each item in the list should be a dictionary containing
                        the following keys:
                        {
                            type:   String
                                    This should match a scene_item_type defined in
                                    one of the outputs in the configuration and is
                                    used to determine the outputs that should be
                                    published for the item

                            name:   String
                                    Name to use for the item in the UI

                            description:    String
                                            Description of the item to use in the UI

                            selected:       Bool
                                            Initial selected state of item in the UI.
                                            Items are selected by default.

                            required:       Bool
                                            Required state of item in the UI.  If True then
                                            item will not be deselectable.  Items are not
                                            required by default.

                            other_params:   Dictionary
                                            Optional dictionary that will be passed to the
                                            pre-publish and publish hooks
                        }
        """

        items = []

        # get the main scene:
        doc = c4d.documents.GetActiveDocument()
        scene_name = doc.GetDocumentName()
        if not scene_name:
            raise TankError("Please Save your file before Publishing")

        scene_path = os.path.join(doc.GetDocumentPath(), doc.GetDocumentName())
        name = os.path.basename(scene_path)

        # create the primary item - this will match the primary output 'scene_item_type':
        items.append({"type": "work_file", "name": name})

        # (AD) - FOR DEBUG ONLY!
        """
        items.append({
            "type": "light_rig",
            "name": "|secondary_lighting",
            "selected":True,
            "description": "blah blah blah"})

        items.append({
            "type": "model",
            "name": "|car",
            "required":True,
            "description": "blah blah blah"})
        items.append({
            "type": "model",
            "name": "|boat",
            "selected":False,
            "required":False,
            "description": "blah blah blah"})
        """
        return items
