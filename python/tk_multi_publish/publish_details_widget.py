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
    
        # (AD) temp
        self._shotgun_task = None
    
        # set up the UI
        from .ui.publish_details_ui import Ui_Form
        self._ui = Ui_Form() 
        self._ui.setupUi(self)
        
        self._ui.publish_btn.clicked.connect(self._on_publish)
        self._ui.cancel_btn.clicked.connect(self._on_cancel)
        
        # TODO: remove browse functionality completely from
        # widget in framework
        self._ui.thumbnail_widget.enable_fs_browse(False)

    @property
    def shotgun_task(self):
        return self._shotgun_task
    @shotgun_task.setter
    def shotgun_task(self, value):
        self._shotgun_task = value
        
    @property
    def comment(self):
        return self._ui.comments_edit.toPlainText().strip()
    @comment.setter
    def comment(self, value):
        self._ui.comments_edit.setPlainText(value)

    @property
    def thumbnail(self):
        return self._ui.thumbnail_widget.thumbnail
    @thumbnail.setter
    def thumbnail(self, value):
        self._ui.thumbnail_widget.thumbnail = value
        
    def set_tasks(self, tasks):
        """
        Set the list of tasks to be displayed
        """
        pass
        
    def _on_publish(self):
        self.publish.emit()
        
    def _on_cancel(self):
        self.cancel.emit()