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
        
        # TODO - temp selection mechanism - should be 
        # retrieved from task list in UI
        self._selected_tasks = []
        self._shotgun_task = None
        
        # set up the UI
        from .ui.publish_form import Ui_PublishForm
        self._ui = Ui_PublishForm() 
        self._ui.setupUi(self)
        
        self._ui.publish_details.publish.connect(self._on_publish)
        self._ui.publish_details.cancel.connect(self._on_close)
        self._ui.publish_result.close.connect(self._on_close)
        self._ui.pages.setCurrentWidget(self._ui.publish_details)
        
        self._update_ui()
        
    @property
    def selected_tasks(self):
        """
        The currently selected tasks
        """
        return self._selected_tasks
    
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
        
    def set_tasks(self, tasks):
        """
        Set the tasks to display in the UI.
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

        QtGui.QMessageBox.information(None, "", "")

        self._set_primary_task(primary_task)
        self._ui.publish_details.set_tasks(secondary_tasks)
        
        # (AD) TEMP
        self._selected_tasks = tasks
        
    def _set_primary_task(self, task):
        """
        Set the primary task and update the UI accordingly
        """
        self._primary_task = task
        print "EH?"
        # update UI for primary task:
        icon_path = task.output.icon_path
        print "ICON PATH: %s" % icon_path
        if not icon_path or not os.path.exists(icon_path):
            icon_path = ":/res/default_header.png"
        icon = QtGui.QPixmap(icon_path)
        
        lines = []
        lines.append("<b>%s - %s</b>" % (task.output.display_name, task.item.name))
        lines.append("%s" % task.output.description)
        lines.append("%s" % task.item.description)
        details_txt = "<br>".join(lines)
        
        self._ui.primary_icon_label.setPixmap(icon)
        self._ui.primary_details_label.setText(details_txt)
        
    """
    def reload(self):
        self._tasks = self._handler.get_tasks()
        
        for task in self._tasks:
            if task.output.selected:
                self._selected_tasks.append(task)
        
        self._update_ui()
    """
     
    def update_tasks(self):
        """
        Placeholder to update UI for all tasks without reloading
        - UI will ultimately update via a signal from the task
        itself
        """
        self._update_ui()
        
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
        
    """    
    # (AD) - temp for proxy UI
    def _on_select_all(self):
        self._selected_tasks = self._tasks
        self._update_ui()
        
    def _on_select_req_only(self):
        self._selected_tasks = []
        for task in self._tasks:
            if task.output.required:
                self._selected_tasks.append(task)
        self._update_ui()

    def _on_select_random(self):
        import random
        self._selected_tasks = []
        for task in self._tasks:
            if task.output.required:
                self._selected_tasks.append(task)
            else:
                if random.random() > 0.5:
                    self._selected_tasks.append(task)
        self._update_ui()
    """
    
    def _update_ui(self):
        """
        Update the UI following a change to the data
        """
        
        msg = ""
        
        if not self._tasks:
            msg = "Nothing to publish!"
        else:
            selected_char = [[" ", "X"], [" ", "R"]]
            error_char = ["", "(!)"]

            group_info = {}
            group_order = []
            for task in self._tasks:
                if task.output.display_group not in group_order:
                    group_order.append(task.output.display_group)
                    
                group_info.setdefault(task.output.display_group, dict())
                group_info[task.output.display_group].setdefault("outputs", set()).add(task.output)
                group_info[task.output.display_group].setdefault("selected_outputs", set())
                group_info[task.output.display_group].setdefault("error_outputs", set())
                group_info[task.output.display_group].setdefault("items", set()).add(task.item)
                group_info[task.output.display_group].setdefault("selected_items", set())
                group_info[task.output.display_group].setdefault("error_items", set())
                group_info[task.output.display_group].setdefault("errors", list())
                if task in self._selected_tasks:
                    group_info[task.output.display_group]["selected_outputs"].add(task.output)
                    group_info[task.output.display_group]["selected_items"].add(task.item)
                if task.pre_publish_errors:
                    group_info[task.output.display_group]["error_outputs"].add(task.output)
                    group_info[task.output.display_group]["error_items"].add(task.item)
                    group_info[task.output.display_group]["errors"].extend(task.pre_publish_errors)
                    
            msg = "Select things to publish...\n\n"
            for g in group_order:
                msg += "\n  %s" % g
                info = group_info[g]
                
                msg += "\n    Outputs:"
                any_output_is_required = False
                for output in info["outputs"]:
                    is_selected = output in info["selected_outputs"]
                    is_required = output.required
                    has_errors = output in info["error_outputs"]
                    if is_required:
                        any_output_is_required = True
                    msg += "\n      - [%s] %s %s" % (selected_char[is_required][is_selected], output.display_name, error_char[has_errors])
                    
                msg += "\n    Items:"
                for item in info["items"]:
                    is_selected = item in info["selected_items"]
                    has_errors = item in info["error_items"]
                    msg += "\n      - [%s] %s %s" % (selected_char[any_output_is_required][is_selected], item.name, error_char[has_errors])
                    
                errors = info["errors"]
                if errors:
                    msg += "\n    %d Errors:" % len(errors)
                    for ei, error in enumerate(errors):
                        msg += "\n      (%d) - %s" % (ei+1, error)
                    
            
        #self._ui.publish_details.setText(msg)
        
        
        
        
        
        
        
        
        
        
        
        
        