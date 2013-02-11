"""
Copyright (c) 2012 Shotgun Software, Inc
----------------------------------------------------

"""
class PublishHandler(object):
    def __init__(self, app):
        self._app = app
        
    
    def show_dialog(self):
        from .publish_ui import PublishUI
        
        self._app.engine.show_dialog("Multi-Publish!", self._app, PublishUI, self._app)