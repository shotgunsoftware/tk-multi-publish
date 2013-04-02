"""
Copyright (c) 2013 Shotgun Software, Inc
----------------------------------------------------
"""

import tank
from tank.platform.qt import QtCore, QtGui
 
class PublishResultWidget(QtGui.QWidget):
    """
    Implementation of the main publish UI
    """
    
    close = QtCore.Signal()
    
    def __init__(self, parent=None):
        """
        Construction
        """
        QtGui.QWidget.__init__(self, parent)
    
        # set up the UI
        from .ui.publish_result_ui import Ui_PublishResulForm
        self._ui = Ui_Form() 
        self._ui.setupUi(self)
        
        self._ui.close_btn.clicked.connect(self._on_close)
        
    def _on_close(self):
        self.close.emit()