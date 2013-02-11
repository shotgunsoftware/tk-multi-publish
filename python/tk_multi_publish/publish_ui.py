"""
Copyright (c) 2012 Shotgun Software, Inc
----------------------------------------------------
"""
"""
import tank
import os
import sys
import time
import threading
"""

# (AD) - TODO - replace with tank core versions so works with PyQt
from PySide import QtCore, QtGui


from .ui.publish_ui import Ui_Form
"""
from .ui.progress import Ui_Progress
"""

class PublishUI(QtGui.QWidget):
    
    def __init__(self, app):
        QtGui.QWidget.__init__(self)#, parent = QtGui.QApplication.activeWindow())#(AD) - this should be derived from TankDialog
        self._app = app
        
        # set up the UI
        self.ui = Ui_Form() 
        self.ui.setupUi(self)
        
        """
        # set up the browsers
        self.ui.left_browser.set_app(self._app)
        self.ui.left_browser.set_label("Step 1. Choose items to publish")
        self.ui.left_browser.enable_multi_select(True)
        self.ui.left_browser.enable_search(False)
                
        self.ui.right_browser.set_app(self._app)
        
        entity_type = self._app.context.entity.get("type", "")
        entity_name = self._app.context.entity.get("name", "")
        
        self.ui.right_browser.set_label("Step 2. Select a Task (%s %s)" % (entity_type, entity_name))
        self.ui.right_browser.enable_search(False)

        # refresh when the checkbox is clicked
        self.ui.hide_tasks.toggled.connect( self._load_tasks )
        
        # publish
        self.ui.publish.clicked.connect( self.accept )
        
        # load data from shotgun
        self._load_scene_contents()    
        self._load_tasks()    
        """
        
    """
    ########################################################################################
    # make sure we trap when the dialog is closed so that we can shut down 
    # our threads. Nuke does not do proper cleanup on exit.
    
    def _cleanup(self):
        self.ui.left_browser.destroy()
        self.ui.right_browser.destroy()
        
    def closeEvent(self, event):
        self._cleanup()
        # okay to close!
        event.accept()
        
    def accept(self):
        self._cleanup()
        QtGui.QDialog.accept(self)
        
    def reject(self):
        self._cleanup()
        QtGui.QDialog.reject(self)
        
    def done(self, status):
        self._cleanup()
        QtGui.QDialog.done(self, status)
        
    ########################################################################################
    # basic business logic        
        
    def _load_scene_contents(self): 
        self.ui.left_browser.clear()
        self.ui.left_browser.load({})
        
    def _load_tasks(self): 
        self.ui.right_browser.clear()
        d = {}
        d["own_tasks_only"] = self.ui.hide_tasks.isChecked()        
        self.ui.right_browser.load(d)
    
    def get_description(self):
        return self.ui.comments.toPlainText()
        
    def get_task(self):
        task_item = self.ui.right_browser.get_selected_item()
        if task_item:
            return task_item.sg_data
        else:
            return None
    
    def get_selected_nodes(self):
        # the mandatory nuke script node returns item.node None so check for that
        tank_write_nodes = []
        for x in self.ui.left_browser.get_selected_items():
            if x.node:
                tank_write_nodes.append(x.node)
        return tank_write_nodes
    """
        