"""
Copyright (c) 2012 Shotgun Software, Inc
----------------------------------------------------

"""

import os
import pprint
import tempfile

import tank
from tank import TankError
from tank.platform.qt import QtCore, QtGui

from .progress import TaskProgressReporter
from .publish_form import PublishForm

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
        self._primary_output = PublishOutput(self._app, self._app.get_setting("primary_output"), name=PublishOutput.PRIMARY_NAME, selected=True, required=True)
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
        from .publish_form import PublishForm
        display_name = self._app.get_setting("display_name")
        self._publish_ui = self._app.engine.show_dialog(display_name, self._app, PublishForm, self._app, self)
        self._publish_ui.publish.connect(self._on_publish)
    
    def get_publish_tasks(self):
        """
        Get the list of tasks that can be published
        """
        # scan scene for items
        items = []
        try:
            # build list of publish tasks:
            items = self._scan_scene()
        except TankError, e:
            # TODO: replace with tank dialog!
            QtGui.QMessageBox.critical(self._publish_ui, "Unable to publish!", 
                                          "Unable to publish:\n\n\t%s\n\n" % e)
            return

        # build task list:            
        tasks = self._build_task_list(items)
        
        return tasks
    
    def get_shotgun_tasks(self):
        """
        Pull a list of tasks from shotgun based on the current context
        """

        filters = [["entity", "is", self._app.context.entity]]
        if self._app.context.step:
            filters += [["step", "is", self._app.context.step]]
        order = [{"field_name":"step", "direction":"asc"}, {"field_name":"content", "direction":"asc"}]
        fields = ["step", "content"]
        
        sg_tasks = self._app.shotgun.find("Task", filters=filters, fields=fields, order=order)

        return sg_tasks

    def get_initial_thumbnail(self):
        """
        Get the initial thumbnail to use for the publish
        """
        return QtGui.QPixmap(self._app.execute_hook("hook_thumbnail"))
    
            
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
            
        # pull rest of info from UI
        sg_task = self._publish_ui.shotgun_task
        thumbnail = self._publish_ui.thumbnail
        comment = self._publish_ui.comment
        
        # create progress reporter and connect to UI:
        progress = TaskProgressReporter(selected_tasks)
        self._publish_ui.set_progress_reporter(progress)

        # show pre-publish progress:
        self._publish_ui.show_publish_progress("Doing Pre-Publish...")
        progress.reset()
        
        # make dialog modal whilst we're doing work:
        """
        (AD) - whilst this almost works, returning from modal state seems to
        completely mess up the window parenting in Maya so may need to have another
        way to do this or (more likely) move it to a separate dialog!
        
        geom = self._publish_ui.window().geometry() 
        self._publish_ui.window().setWindowModality(QtCore.Qt.ApplicationModal)
        self._publish_ui.window().hide()
        self._publish_ui.window().show()
        self._publish_ui.window().setGeometry(geom)
        """
        
        """
        # (AD) - do some dummy progress...
        import time
        for p in range(1, 11):
            progress.report(p * 10.0, "Doing something I guess - on %d of %d" % (p, 10))
            time.sleep(1.0)
        """
                    
        # do pre-publish:
        try:
            self._do_pre_publish(selected_tasks, progress.report)
        except TankError, e:
            # an exception means that we can't perform the publish so show
            # dialog and stop processing
            
            # TODO - show tank dialog!
            QtGui.QMessageBox.information(self._publish_ui, "Pre-publish Failed", 
                                          "Publish has been stopped for the following reason:\n\n%s\n\nUnable to continue!" % e)
            self._publish_ui.show_publish_details()
            return
        finally:
            """
            # restore window to be modeless
            self._publish_ui.window().setWindowModality(QtCore.Qt.NonModal)
            self._publish_ui.window().hide()
            self._publish_ui.window().show()  
            self._publish_ui.window().setGeometry(geom)
            QtGui.QApplication.processEvents()
            """
            pass
        
        # check that we can continue:
        num_errors = 0
        for task in selected_tasks:
            num_errors += len(task.pre_publish_errors)
        if num_errors > 0:
            self._publish_ui.show_publish_details()
            
            # TODO: replace with Tank dialog
            res = QtGui.QMessageBox.warning(self._publish_ui, "Pre-publish Errors", 
                                             "Pre-publish returned %d errors\n\nWould you like to publish anyway?" % num_errors,
                                             QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
            if res != QtGui.QMessageBox.Yes:
                return
                
        # show publish progress:
        self._publish_ui.show_publish_progress("Publishing...")
        progress.reset()
                
        # do the publish
        publish_errors = []
        publish_failed = False
        try:
            self._do_publish(selected_tasks, sg_task, thumbnail, comment, progress.report)
        except TankError, e:
            publish_errors.append("%s" % e)
            publish_failed = True
        
        # check for any other publish errors:
        for task in selected_tasks:
            for error in task.publish_errors:
                publish_errors.append("%s, %s: %s" % (task.output.display_name, task.item.name, error))
        
        # if publish didn't fail then do post publish:
        if publish_failed:
            # inform that post-publish didn't run
            publish_errors.append("Post-publish was not run due to previous errors!")
        else:
            self._publish_ui.show_publish_progress("Doing Post-Publish...")
            progress.reset(1)
            
            try:
                self._do_post_publish(progress.report)
            except TankError, e:
                publish_errors.append("Post-publish failed with the following error:\n\t%s" % e)
            
        # show publish result:
        self._publish_ui.show_publish_result(not publish_errors, publish_errors)

    def _build_task_list(self, items):
        """
        Takes a list of items and builds a list of tasks containing
        each item and it's corresponding output
        """
        
        #TODO: build list by looping through outputs to order by output
        
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
                raise TankError("Item %s found with unrecognised scene item type %s" % (item.name, item.scene_item_type))
                
            for output in outputs:
                tasks.append(Task(item, output))
                
        return tasks
    
    def _scan_scene(self):
        """
        Find the list of 'items' to publish
        """
        # find the items:
        items = [Item(item) for item in self._app.execute_hook("hook_scan_scene")]
    
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
                    raise TankError("Scan scene returned multiple items for the primary output type '%s' which is not allowed" 
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
        
        # split tasks into primary and secondary:
        primary_task=None
        secondary_tasks=[]
        for ti, task in enumerate(tasks):
            if task.output == self._primary_output:
                if primary_task:
                    raise TankError("Found multiple primary tasks to pre-publish!")
                primary_task = task
                secondary_tasks = tasks[:ti] + tasks[(ti+1):]
        if not primary_task:
            raise TankError("Couldn't find primary task to pre-publish!")
        
        # do pre-publish of primary task:
        primary_task.pre_publish_errors = self._app.execute_hook("hook_primary_pre_publish",  
                                                                task=primary_task.as_dictionary(), 
                                                                work_template = self._work_template,
                                                                progress_cb=progress_cb)

        # do pre-publish of secondary tasks:
        hook_tasks = [task.as_dictionary() for task in secondary_tasks]
        pp_results = self._app.execute_hook("hook_secondary_pre_publish",  
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
            except:
                raise TankError("Badly formed result returned from hook: %s" % result)
                
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
        # split tasks into primary and secondary:
        primary_task=None
        secondary_tasks=[]
        for ti, task in enumerate(tasks):
            if task.output == self._primary_output:
                if primary_task:
                    raise TankError("Found multiple primary tasks to publish!")
                primary_task = task
                secondary_tasks = tasks[:ti] + tasks[(ti+1):]
        if not primary_task:
            raise TankError("Couldn't find primary task to publish!")
        
        # save the thumbnail to a temporary location:
        thumbnail_path = ""
        if thumbnail and not thumbnail.isNull():
            tmp_file = tempfile.NamedTemporaryFile(suffix=".png", prefix="tanktmp", delete=False)
            thumbnail_path = tmp_file.name
            tmp_file.close()
            thumbnail.save(thumbnail_path)
        
        try:
            # do publish of primary task:
            primary_path = self._app.execute_hook("hook_primary_publish",  
                                                  task=primary_task.as_dictionary(), 
                                                  work_template = self._work_template,
                                                  comment = comment,
                                                  thumbnail_path = thumbnail_path,
                                                  sg_task = sg_task,
                                                  progress_cb=progress_cb)
                
            # do publish of secondary tasks:            
            hook_tasks = [task.as_dictionary() for task in secondary_tasks]
            p_results = self._app.execute_hook("hook_secondary_publish",  
                                                 tasks=hook_tasks, 
                                                 work_template = self._work_template,
                                                 comment = comment,
                                                 thumbnail_path = thumbnail_path,
                                                 sg_task = sg_task,
                                                 primary_publish_path=primary_path,
                                                 progress_cb=progress_cb)
        finally:
            # delete temporary thumbnail file:
            if thumbnail_path:
                os.remove(thumbnail_path)

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
            except:
                raise TankError("Badly formed result returned from hook: %s" % result)
                
        for task in tasks:
            result = result_index.get((task.item.name, task.output.name))
            if result:
                task.publish_errors = result["errors"]
            else:
                task.publish_errors = []
                
    def _do_post_publish(self, progress_cb):
        """
        Do post-publish using the post-publish hook
        """
        
        # do post-publish using post-publish hook:
        self._app.execute_hook( "hook_post_publish",  
                                work_template = self._work_template,
                                progress_cb=progress_cb)
    

    