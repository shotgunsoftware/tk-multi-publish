"""
Copyright (c) 2013 Shotgun Software, Inc
----------------------------------------------------
"""

import os

from tank.platform.qt import QtCore, QtGui

class PublishForm(QtGui.QWidget):
    """
    Implementation of the main publish UI
    """

    # signals
    publish = QtCore.Signal()
    
    def __init__(self, app, handler, parent=None):
        """
        Construction
        """
        QtGui.QWidget.__init__(self, parent)
        self._app = app
        
        # TODO: shouldn't need the handler
        self._handler = handler
    
        self._primary_task = None
        self._tasks = []
        
        # set up the UI
        from .ui.publish_form import Ui_PublishForm
        self._ui = Ui_PublishForm() 
        self._ui.setupUi(self)
        
        self._ui.publish_details.publish.connect(self._on_publish)
        self._ui.publish_details.cancel.connect(self._on_close)
        self._ui.publish_result.close.connect(self._on_close)
        
        # always start with the details page:
        self.show_publish_details()
        
        #self._update_ui()
        
    @property
    def selected_tasks(self):
        """
        The currently selected tasks
        """
        return self._get_selected_tasks()
    
    @property
    def shotgun_task(self):
        """
        The shotgun task that the publish should be linked to
        """
        return self._ui.publish_details.shotgun_task
    @shotgun_task.setter
    def shotgun_task(self, value):
        self._ui.publish_details.shotgun_task = value
        
    @property
    def can_change_shotgun_task(self):
        """
        Control if the shotgun task can be changed or not
        """
        return self._ui.publish_details.can_change_shotgun_task
    @can_change_shotgun_task.setter
    def can_change_shotgun_task(self, value):
        self._ui.publish_details.can_change_shotgun_task = value
        
    @property
    def thumbnail(self):
        """
        The thumbnail to use for the publish
        """
        return self._ui.publish_details.thumbnail
    @thumbnail.setter
    def thumbnail(self, value):
        self._ui.publish_details.thumbnail = value
         
    @property
    def comment(self):
        """
        The comment to use for the publish
        """
        return self._ui.publish_details.comment
    @comment.setter
    def comment(self, value):
        self._ui.publish_details.comment = value
    
    def show_publish_details(self):
        self._ui.pages.setCurrentWidget(self._ui.publish_details)
        
    def show_publish_progress(self, stage):
        self._ui.pages.setCurrentWidget(self._ui.publish_progress)
        self._ui.publish_progress.title = stage
    
    def set_progress_reporter(self, reporter):
        self._ui.publish_progress.set_reporter(reporter)
        
    def show_publish_result(self, success, errors):
        """
        Show the result of the publish in the UI
        """
        # update UI with result:
        # TODO...
        
        # show page:
        self._ui.pages.setCurrentWidget(self._ui.publish_result)
        self._ui.publish_result.status = success
        self._ui.publish_result.errors = errors
        
    def initialize(self, tasks, sg_tasks):
        """
        Initialize UI with information provided
        """
        
        # split tasks into primary and secondary:
        primary_task = None
        secondary_tasks = []
        for task in tasks:
            if task.output.is_primary:
                if primary_task:
                    # should never get this far but just in case!
                    raise Exception("Found multiple primary tasks - don't know how to handle this!")
                primary_task = task
            else:
                secondary_tasks.append(task)
                
        # initialize primary task UI:
        self._set_primary_task(primary_task)

        # initialize publish details form:
        self._ui.publish_details.initialize(secondary_tasks, sg_tasks)

        
    def _get_selected_tasks(self):
        """
        Get a list of the selected tasks that 
        should be published
        """
        
        # always publish primary task:
        selected_tasks = [self._primary_task]
        
        # get secondary tasks from details form:
        selected_tasks.extend(self._ui.publish_details.selected_tasks)
        
        return selected_tasks
        
    def _set_primary_task(self, task):
        """
        Set the primary task and update the UI accordingly
        """
        self._primary_task = task
        
        # update UI for primary task:
        icon_path = task.output.icon_path
        if os.path.isfile(icon_path) and os.path.exists(icon_path):
            icon = QtGui.QPixmap(icon_path)
            if not icon.isNull():
                self._ui.primary_icon_label.setPixmap(icon)
                    
        lines = []
        
        lines.append("<span style='font-size: 16px'}><b>%s - %s</b></span><span style='font-size: 12px'}>" % (task.output.display_name, task.item.name))
        if task.output.description:
            lines.append("%s" % task.output.description)
        if task.item.description:
            lines.append("%s" % task.item.description)
        details_txt = "%s</span>" % "<br>".join(lines) 
        self._ui.primary_details_label.setText(details_txt)
        
    def _on_publish(self):
        """
        Slot called when the publish button in the dialog is clicked
        """
        self.publish.emit()
        
    def _on_close(self):
        """
        Slot called when the cancel or close signals in the dialog 
        are recieved
        """
        self.window().close()
        
        
        
        
        
        
        
        
        