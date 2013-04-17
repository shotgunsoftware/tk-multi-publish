"""
Copyright (c) 2013 Shotgun Software, Inc
----------------------------------------------------

"""
import os
import nuke

import tank
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
        
        # get current script:
        script_name = nuke.root().name()
        if script_name == "Root":
            raise TankError("Please Save your file before Publishing")
        
        script_file = script_name.replace("/", os.path.sep)
        script_name = os.path.basename(script_file)
        items.append({"type": "work_file", "name": script_name})
        
        # find tk-nuke-writenode app
        app = tank.platform.current_engine().apps.get("tk-nuke-writenode")
        if app:
            # Find tank write nodes:
            write_nodes = app.get_write_nodes()

            for write_node in write_nodes:
                # use app to get node details:
                name = app.get_node_name(write_node)
                profile_name = app.get_node_profile_name(write_node)
                
                items.append({"name":name,
                              "type":"write_node",
                              "description":profile_name,
                              "other_params":{"node":write_node}})
                 
        return items