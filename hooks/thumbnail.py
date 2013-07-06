"""
Copyright (c) 2013 Shotgun Software, Inc
----------------------------------------------------

"""
import os
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
        

        # get the engine name from the parent object (app/engine/etc.)
        engine_name = self.parent.engine.name
        
        # depending on engine:
        if engine_name == "tk-hiero":
            return self._extract_hiero_thumbnail()

        # default implementation does nothing        
        return None
    
    
    def _extract_hiero_thumbnail(self):
        """
        Extracts the 
        
        """
        import hiero.core
        from PySide import QtCore
        import tempfile
        import uuid
        
        # get the menu selection from hiero engine
        selection = self.parent.engine.get_menu_selection()

        if len(selection) != 1:
            raise TankError("Please select a single Project!")
        
        if not isinstance(selection[0] , hiero.core.Bin):
            raise TankError("Please select a Hiero Project!")
            
        project = selection[0].project()
        if project is None:
            # apparently bins can be without projects (child bins I think)
            raise TankError("Please select a Hiero Project!")
        
        # find first sequence with a poster frame
        for s in project.sequences():            
            if s.posterFrame():
                try:
                    # this sequence has got a poster frame!
                    thumb_qimage = s.thumbnail(s.posterFrame())
                    # scale it down to 600px wide
                    thumb_qimage_scaled = thumb_qimage.scaledToWidth(600, QtCore.Qt.SmoothTransformation)
                    # save it to tmp location
                    png_thumb = os.path.join(tempfile.gettempdir(), "sgtk_thumb_%s.png" % uuid.uuid4().hex)
                    thumb_qimage_scaled.save(png_thumb)
                    return png_thumb
                except:
                    return None
        
        return None
