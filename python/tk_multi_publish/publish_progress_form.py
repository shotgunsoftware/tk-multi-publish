"""
Copyright (c) 2013 Shotgun Software, Inc
----------------------------------------------------
"""

import tank
from tank.platform.qt import QtCore, QtGui
 
class PublishProgressForm(QtGui.QWidget):
    """
    Implementation of the main publish UI
    """
    
    def __init__(self, parent=None):
        """
        Construction
        """
        QtGui.QWidget.__init__(self, parent)
    
        # set up the UI
        from .ui.publish_result_form import Ui_PublishProgressForm
        self._ui = Ui_PublishProgressForm() 
        self._ui.setupUi(self)
        
    def report(self, percent, msg):
        # (AD) - or something..
        pass