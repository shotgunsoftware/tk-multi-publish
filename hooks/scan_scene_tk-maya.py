"""
Copyright (c) 2013 Shotgun Software, Inc
----------------------------------------------------

"""

import os
import maya.cmds as cmds

import tank
from tank import Hook

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
                                            
                            other_params:   Dictionary
                                            Optional dictionary that will be passed to the
                                            pre-publish and publish hooks
                        }
        """   
                
        items = []
        
        # get the main scene:
        scene_path = os.path.abspath(cmds.file(query=True, sn=True))
        name = os.path.basename(scene_path)
        if not name:
            name = "untitled"    
            
        items.append({ 
            "type": "maya_scene", 
            "name": name,
            "description": ""})
        
        # (AD) - FOR DEBUG ONLY!
        
        """
        items.append({ 
            "type": "light_rig", 
            "name": "|primary_lighting",
            "description": "blah blah blah"})
        """
        items.append({ 
            "type": "light_rig", 
            "name": "|secondary_lighting",
            "description": "blah blah blah"})
        
        items.append({ 
            "type": "model", 
            "name": "|car",
            "description": "blah blah blah"})
        items.append({ 
            "type": "model", 
            "name": "|boat",
            "description": "blah blah blah"})
        
        return items
