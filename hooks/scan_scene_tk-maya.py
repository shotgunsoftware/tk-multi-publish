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
