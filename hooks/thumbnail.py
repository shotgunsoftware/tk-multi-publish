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
    return None