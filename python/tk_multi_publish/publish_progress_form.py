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
    
        self._reporter = None
    
        # set up the UI
        from .ui.publish_progress_form import Ui_PublishProgressForm
        self._ui = Ui_PublishProgressForm() 
        self._ui.setupUi(self)
        
        self._ui.progress_bar.setValue(0)
        self._ui.details.setText("")
        
    @property
    def title(self):
        return self._ui.title.toPlainText()
    @title.setter
    def title(self, value):
        self._ui.title.setText(value)
        QtCore.QCoreApplication.processEvents()
        
    def set_reporter(self, reporter):
        """
        Connect to the reporter:
        """
        if self._reporter:
            self._reporter.progress.disconnect(self._on_progress)
        self._reporter = reporter
        if self._reporter:
            self._reporter.progress.connect(self._on_progress)    
    
    def _on_progress(self, amount, msg):
        self._ui.progress_bar.setValue(amount)
        if msg != None:
            self._ui.details.setText(msg)
        
        QtCore.QCoreApplication.processEvents()
        
        
        
        
        
        
        