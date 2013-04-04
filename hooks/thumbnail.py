"""
Copyright (c) 2013 Shotgun Software, Inc
----------------------------------------------------

"""
import tank
from tank import Hook

class ThumbnailHook(Hook, engine_name):
    """
    Hook to scan scene for items to publish
    """
    def execute(self, **kwargs):
        """
        Main hook entry point
        
        :return:    String
                    Hook should return a file path pointing to the location of
                    a thumbnail file on disk that will be used as the primary
                    publish thumbnail.
        """
        
        # default implementation does nothing
        return None