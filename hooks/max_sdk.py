# Copyright (c) 2013 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.


class MaxSdk(object):
    """
    Unifies Py3dsMax and MaxPlus for common publishing functions.
    """

    @staticmethod
    def Save(scene_path, engine_name): 
        """
        Save Scene.
        """
        if engine_name == "tk-3dsmax":
            from Py3dsMax import mxs
            mxs.saveMaxFile(scene_path)
        elif engine_name == "tk-3dsmax-plus":
            import MaxPlus
            MaxPlus.FileManager.Save(scene_path)

    @staticmethod
    def GetScenePath(engine_name):
        """
        Get full Path (including filename) of current scene.
        """

        scene_path = ''
        if engine_name == "tk-3dsmax":
            from Py3dsMax import mxs
            scene_path = os.path.abspath(os.path.join(mxs.maxFilePath, mxs.maxFileName))
        elif engine_name == "tk-3dsmax-plus":
            import MaxPlus
            scene_path = MaxPlus.FileManager.GetFileNameAndPath()

        return scene_path;
