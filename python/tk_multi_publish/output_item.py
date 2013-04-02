"""
Copyright (c) 2013 Shotgun Software, Inc
----------------------------------------------------
"""
import os
import tank
from tank.platform.qt import QtCore, QtGui
              
class OutputItem(QtGui.QWidget):
    """
    """
    def __init__(self, output, parent=None):
        """
        Construction
        """
        QtGui.QWidget.__init__(self, parent)
    
        self._output = output
    
        # set up the UI
        from .ui.output_item import Ui_OutputItem
        self._ui = Ui_OutputItem() 
        self._ui.setupUi(self)
        
        self._update_ui()
        
    @property
    def output(self):
        return self._output
        
    @property
    def selected(self):
        return self._ui.select_cb.isChecked()
        
    def mousePressEvent(self, event):
        if self._ui.select_cb.isEnabled():
            self._ui.select_cb.setChecked(not self._ui.select_cb.isChecked())
        
    def _update_ui(self):
        """
        Update UI
        """
        
        # set label text
        lines = []
        lines.append("<b>%s</b>" % self._output.display_name)
        lines.append("%s" % self._output.description)
        self._ui.details_label.setText("<br>".join(lines))

        # set icon:
        icon_path = self._output.icon_path
        if os.path.exists(icon_path):
            pm = QPixmap(icon_path)
            self._ui.icon_label.setPixmap(pm)
        
        # selected state
        self._ui.select_cb.setChecked(self._output.selected)
        self._ui.select_cb.setEnabled(not self._output.required)
        