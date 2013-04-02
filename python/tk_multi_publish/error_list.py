"""
Copyright (c) 2013 Shotgun Software, Inc
----------------------------------------------------
"""

import tank
from tank.platform.qt import QtCore, QtGui

class ErrorItem(QtGui.QWidget):
    """
    """
    def __init__(self, parent=None):
        """
        Construction
        """
        QtGui.QWidget.__init__(self, parent)
    
        # set up the UI
        from .ui.error_item import Ui_ErrorItem
        self._ui = Ui_ErrorItem() 
        self._ui.setupUi(self)

class ErrorList(QtGui.QWidget):
    """
    """
    def __init__(self, parent=None):
        """
        Construction
        """
        QtGui.QWidget.__init__(self, parent)
    
        # set up the UI
        from .ui.error_list import Ui_ErrorList
        self._ui = Ui_ErrorList() 
        self._ui.setupUi(self)
        
