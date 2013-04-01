"""
Copyright (c) 2013 Shotgun Software, Inc
----------------------------------------------------
"""

import tank
from tank.platform.qt import QtCore, QtGui

thumbnail_widget = tank.platform.import_framework("tk-framework-widget", "thumbnail_widget")
class ThumbnailWidget(thumbnail_widget.ThumbnailWidget):
    """
    """
    pass
        
class PublishDetailsWidget(QtGui.QWidget):
    """
    Implementation of the main publish UI
    """

    # signals
    publish = QtCore.Signal()
    cancel = QtCore.Signal()
    
    def __init__(self, parent=None):
        """
        Construction
        """
        QtGui.QWidget.__init__(self, parent)
    
        # set up the UI
        from .ui.publish_details_ui import Ui_Form
        self._ui = Ui_Form() 
        self._ui.setupUi(self)
        
        self._ui.publish_btn.clicked.connect(self._on_publish)
        self._ui.cancel_btn.clicked.connect(self._on_cancel)
        
        # TODO: remove browse functionality completely from
        # widget in framework
        self._ui.thumbnail_widget.enable_fs_browse(False)
        
        
    def _on_publish(self):
        self.publish.emit()
        
    def _on_cancel(self):
        self.cancel.emit()