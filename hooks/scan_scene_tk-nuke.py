"""
Copyright (c) 2013 Shotgun Software, Inc
----------------------------------------------------

"""
import os
import nuke

import tank
from tank import Hook

class ScanSceneHook(Hook):
    """
    Hook to scan scene for items to publish
    """
    
    def execute(self, engine_name, **kwargs):
        """
        Main hook entry point
        """
        
        items = []
        
        # get current script:
        script_file = nuke.root().name().replace("/", os.path.sep)
        script_name = os.path.basename(script_file)
        items.append({ 
            "type": "nuke_script",
            "name": script_name, 
            "description": ""})
        
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