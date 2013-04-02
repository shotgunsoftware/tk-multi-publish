"""
Copyright (c) 2013 Shotgun Software, Inc
----------------------------------------------------
"""

import tank
from tank.platform.qt import QtCore, QtGui

class ErrorItemWidget(QtGui.QWidget):
    """
    """
    def __init__(self, parent=None):
        """
        Construction
        """
        QtGui.QWidget.__init__(self, parent)
    
        # set up the UI
        from .ui.error_item_ui import Ui_ErrorItem
        self._ui = Ui_Form() 
        self._ui.setupUi(self)

class ErrorListWidget(QtGui.QWidget):
    """
    """
    def __init__(self, parent=None):
        """
        Construction
        """
        QtGui.QWidget.__init__(self, parent)
    
        # set up the UI
        from .ui.error_list_ui import Ui_ErrorList
        self._ui = Ui_Form() 
        self._ui.setupUi(self)
        
