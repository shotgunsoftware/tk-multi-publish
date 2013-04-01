"""
Copyright (c) 2012 Shotgun Software, Inc
----------------------------------------------------

"""

import os
import pprint

import tank
from tank.platform.qt import QtCore, QtGui

from .progress import ProgressReporter
from .publish_ui import PublishUI

from .output import PublishOutput
from .item import *
from .task import Task
    
class PublishHandler(object):
    """
    Main publish handler
    """
        
    def __init__(self, app):
        """
        Construction
        """
        self._app = app
        self._publish_ui = None

        self._work_template = self._app.get_template("template_work")

        # load outputs from configuration:
        self._primary_output = PublishOutput(self._app, self._app.get_setting("primary_output"), name="primary", selected=True, required=True, display_group="PRIMARY")
        self._secondary_outputs = [PublishOutput(self._app, output) for output in self._app.get_setting("secondary_outputs")]
        
        # make sure that the scene_item_type used for the primary output is 
        # not used for any of the secondary outputs
        for item_type in [output.scene_item_type for output in self._secondary_outputs]:
            if item_type == self._primary_output.scene_item_type:
                raise Exception("Secondary output is defined with the same scene_item_type (%s) as the primary output - this is not allowed"
                                % self._primary_output.scene_item_type)  
        
    def show_publish_dlg(self):
        """
        Displays the publish dialog
        """
        
        # create new multi-publish dialog instance
        from .publish_ui import PublishUI
        display_name = self._app.get_setting("display_name")
        self._publish_ui = self._app.engine.show_dialog(display_name, self._app, PublishUI, self._app, self)
        self._publish_ui.publish.connect(self._on_publish)
        
        # get the tasks and update the UI:
        items = self._scan_scene()
        tasks = self._build_task_list(items)
        self._publish_ui.set_tasks(tasks)
        
        # and any other info:
        thumbnail = None# TODO: run hook
        self._publish_ui.thumbnail = thumbnail
        
        # shotgun tasks:
        # TODO...
        
        
    """
    def get_tasks(self):
        items = self._scan_scene()
        tasks = self._build_task_list(items)
        return tasks
    """
    
    def _on_publish(self):
        """
        Slot called when publish signal is emitted from the UI
        """
        
        # get list of tasks from UI:
        selected_tasks = self._publish_ui.selected_tasks

        # stop if can't actually do the publish!
        if not selected_tasks:
            # TODO - replace with tank dialog
            QtGui.QMessageBox.information(self._publish_ui, "Publish", "Nothing selected to publish - unable to continue!")
            return
            
        # TODO - pull from UI
        sg_task = self._publish_ui.shotgun_task
        thumbnail = self._publish_ui.thumbnail
        comment = self._publish_ui.comment
        
        print "About to do publish using details:"
        print "  Shotgun task: %s" % sg_task
        print "  Thumbnail: %s" % thumbnail
        print "  Comment: %s" % comment
        print "  Tasks = %s" % selected_tasks
        
        # TODO - remove (obviously)
        raise Exception("Publish currently disabled whilst building UI!")
                
        # create progress reporter and connect to UI:
        progress = ProgressReporter()
        # TODO - create progress UI and connect to reporter
        
        # do pre-publish:
        QtGui.QMessageBox.information(self._publish_ui, "Pre-publish (debug)", "Doing pre-publish\n%s" % self._debug_format_tasks_str(selected_tasks))
        try:
            self._do_pre_publish(selected_tasks, progress.report)
        except Exception, e:
            # TODO - show tank dialog!
            QtGui.QMessageBox.information(self._publish_ui, "Pre-publish Failed", 
                                          "Pre-publish failed due to an unexpected exception:\n\n\t%s\n\nUnable to continue!" % e)
            raise
            #return
        
        # check that we can continue:
        num_errors = 0
        for task in selected_tasks:
            num_errors += len(task.pre_publish_errors)
        if num_errors > 0:
            # TODO: replace with Tank dialog
            res = QtGui.QMessageBox.warning(self._publish_ui, "Pre-publish Errors", 
                                             "Pre-publish returned %d errors\n\nWould you like to publish anyway?" % num_errors,
                                             QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
            if res != QtGui.QMessageBox.Yes:
                self._publish_ui.update_tasks()
                return
                
        # do the publish
        QtGui.QMessageBox.information(self._publish_ui, "Publish (debug)", "Doing publish\n%s" % self._debug_format_tasks_str(selected_tasks))
        try:
            self._do_publish(selected_tasks, sg_task, thumbnail, comment, progress.report)
        except Exception, e:
            # TODO: replace with tank dialog!
            QtGui.QMessageBox.critical(self._publish_ui, "Publish Failed", 
                                          "Publish failed due to an unexpected exception:\n\n\t%s\n\nUnable to continue!" % e)
            raise
            #return
        
        # check that everything was published:
        publish_errors = []
        for task in selected_tasks:
            for error in task.publish_errors:
                publish_errors.append("%s, %s:\n    %s" % (task.item.name, task.output.name, error))
        
        if not publish_errors:
            QtGui.QMessageBox.information(self._publish_ui, "Publish Succeeded", "Publish Succeeded - yay!")
            self._publish_ui.close()
        else:
            # TODO - return to dialog and upate with error information
            error_msg = "Published encountered the following errors:\n %s" % ("\n    - ".join(publish_errors))
            QtGui.QMessageBox.critical(self._publish_ui, "Publish Failed", error_msg)

    def _build_task_list(self, items):
        """
        Takes a list of items and builds a list of tasks containing
        each item and it's corresponding output
        """
        
        # create index from scene_item_type to output
        outputs_by_type = {}
        
        outputs_by_type[self._primary_output.scene_item_type] = [self._primary_output]
        for output in self._secondary_outputs:
            outputs_by_type.setdefault(output.scene_item_type, list()).append(output)
        
        # build tasks for each item and output:
        tasks = []
        for item in items:
            outputs = outputs_by_type.get(item.scene_item_type)
            if not outputs:
                raise Exception("Item %s found with unrecognised scene item type %s" % (item.name, item.scene_item_type))
                
            for output in outputs:
                tasks.append(Task(item, output))
                
        return tasks
    
    def _scan_scene(self):
        """
        Find the list of 'items' to publish
        """
        # find the items:
        items = [Item(item) for item in self._app.execute_hook("hook_scan_scene", 
                                                               engine_name = self._app.engine.name)]
    
        # validate that only one matches the primary type
        # and that all items are valid:
        primary_type = self._primary_output.scene_item_type
        secondary_types = [output.scene_item_type for output in self._secondary_outputs]
        primary_item = None
        for item in items:

            item.validate()
            item_type = item.scene_item_type
            
            if item_type == primary_type:
                if primary_item:
                    raise Exception("Scan scene returned multiple items for the primary output type '%s' which is not allowed" 
                                    % primary_type)
                else:
                    primary_item = item
                
        return items
        
    
    def _debug_format_tasks_str(self, tasks):
        tasks_str = "Tasks:"
        for ti, task in enumerate(tasks):
            tasks_str += "\n[%d]\tItem: %s" % (ti, task.item.name)
            tasks_str += "\n   \tOutput: %s" % task.output.display_name
        return tasks_str
        
    def _do_pre_publish(self, tasks, progress_cb):
        """
        Do pre-publish pass on tasks using the pre-publish hook
        """
        
        # get tasks in hook format (dictionaries rather than internal class instances):
        hook_tasks = [task.as_dictionary() for task in tasks]
        
        # do pre-publish using pre-publish hook:
        pp_results = self._app.execute_hook("hook_pre_publish", 
                                            engine_name=self._app.engine.name, 
                                            tasks=hook_tasks, 
                                            work_template = self._work_template,
                                            progress_cb=progress_cb)
        
        # push any errors back to tasks:
        result_index = {}
        for result in pp_results:
            try:
                errors = result.get("errors")
                if not errors:
                    continue
                
                item_name = result["task"]["item"]["name"]
                output_name = result["task"]["output"]["name"]
                result_index[(item_name, output_name)] = result
            except Exception, e:
                # TODO: better handle badly formed results being returned from the hook!
                pass
                
        for task in tasks:
            result = result_index.get((task.item.name, task.output.name))
            if result:
                task.pre_publish_errors = result["errors"]
            else:
                task.pre_publish_errors = []
        
        
    def _do_publish(self, tasks, sg_task, thumbnail, comment, progress_cb):
        """
        Do publish of tasks using the publish hook
        """
        
        # get tasks in hook format (dictionaries rather than internal class instances):
        hook_tasks = [task.as_dictionary() for task in tasks]
        
        # save the thumbnail to a temporary location:
        thumbnail_path = ""
        # TODO: save thumbnail...
        
        # do publish using publish hook:
        p_results = self._app.execute_hook("hook_publish", 
                                             engine_name=self._app.engine.name, 
                                             tasks=hook_tasks, 
                                             work_template = self._work_template,
                                             comment = comment,
                                             thumbnail_path = thumbnail_path,
                                             sg_task = sg_task,
                                             progress_cb=progress_cb)

        # TODO: delete temporary thumbnail:
        # ...

        # push any errors back to tasks:
        result_index = {}
        for result in p_results:
            try:
                errors = result.get("errors")
                if not errors:
                    continue
                
                item_name = result["task"]["item"]["name"]
                output_name = result["task"]["output"]["name"]
                result_index[(item_name, output_name)] = result
            except Exception, e:
                # TODO: better handle badly formed results being returned from the hook!
                pass
                
        for task in tasks:
            result = result_index.get((task.item.name, task.output.name))
            if result:
                task.publish_errors = result["errors"]
            else:
                task.publish_errors = []
                
                
    """
    # (AD) - old code but may be needed
    def __show_publish_dlg_ORIG(self):
        # create dialog and hook up signals:
        #
        # first try to get the current window - it seems that
        # keeping a handle isn't reliable as the underlying c++
        # QWidget can get deleted even though the python object
        # is still valid
        # (AD) - need to check if this is a Maya specific problem
        # and if it is then try to move to engine rather than have
        # the handling done here!
        win = None
        if self._publish_dlg:
            try:
                win = self._publish_dlg.window()
            except Exception, e:
                # supress exception!
                win = None
                self._publish_dlg = None
        
        if win:
            if not win.isVisible():
                # window was hidden/closed so clear, show and then reload:
                self._clear_ui()
                win.show()
                self._initialize_ui()
        else:
            # create new multi-publish dialog instance
            from .publish_ui import PublishUI
            display_name = self._app.get_setting("display_name")
            self._publish_ui = self._app.engine.show_dialog(display_name, self._app, PublishUI, self._app, self)
            self._publish_ui.publish.connect(self._on_publish)
            #self._publish_ui.closed.connect(self.__ui_on_closed)
            self._initialize_ui()

        # make sure it is active:
        self._publish_ui.activateWindow()
    """


    