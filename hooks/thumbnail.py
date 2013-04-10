"""
Copyright (c) 2013 Shotgun Software, Inc
----------------------------------------------------

"""
import tank
from tank import Hook

class ThumbnailHook(Hook):
    """
    Hook that can be used to provide a pre-defined primary 
    thumbnail for the publish
    """
    def execute(self, **kwargs):
        """
        Main hook entry point
        :returns:       String
                        Hook should return a file path pointing to the location of
                        a thumbnail file on disk that will be used for the publish.
                        If the hook returns None then the screenshot functionality
                        will be enabled in the UI.
        """
        
        # Note: the engine name can be accessed from the hook's parent:
        # engine_name = self.parent.engine.name
        
        # default implementation does nothing
        return None