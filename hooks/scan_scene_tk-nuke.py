# Copyright (c) 2013 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.

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
                is_disabled = write_node.knob("disable").value()
                
                items.append({"name":"Shotgun Write Node: %s" % name,
                              "type":"write_node",
                              "description":"Render Profile: %s" % profile_name,
                              "selected":not is_disabled,
                              "other_params":{"node":write_node}})
                 
        return items