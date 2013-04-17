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
        
        try:
            # create new multi-publish dialog instance
            from .publish_form import PublishForm
            display_name = self._app.get_setting("display_name")
            form = self._app.engine.show_dialog(display_name, self._app, PublishForm, self._app, self)
            form.publish.connect(lambda f = form: self._on_publish(f))
        except TankError, e:
            QtGui.QMessageBox.information(None, "Unable To Publish!", "%s" % e)
            return
        except Exception, e:
            self._app.log_exception("Unable to publish")
    
    def get_publish_tasks(self):
        """
        Get the list of tasks that can be published
        """
        # scan scene for items
        items = self._scan_scene()

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
    
            
    def _on_publish(self, publish_form):
        """
        Slot called when publish signal is emitted from the UI
        """
        
        # get list of tasks from UI:
        selected_tasks = publish_form.selected_tasks

        # stop if can't actually do the publish!
        if not selected_tasks:
            # TODO - replace with tank dialog
            QtGui.QMessageBox.information(publish_form, "Publish", "Nothing selected to publish - unable to continue!")
            return
            
        # split tasks into primary and secondary:
        primary_task=None
        secondary_tasks=[]
        for ti, task in enumerate(selected_tasks):
            if task.output == self._primary_output:
                if primary_task:
                    raise TankError("Found multiple primary tasks to publish!")
                primary_task = task
                secondary_tasks = selected_tasks[:ti] + selected_tasks[(ti+1):]
        if not primary_task:
            raise TankError("Couldn't find primary task to publish!")
            
        # pull rest of info from UI
        sg_task = publish_form.shotgun_task
        thumbnail = publish_form.thumbnail
        comment = publish_form.comment
        
        # create progress reporter and connect to UI:
        progress = TaskProgressReporter(selected_tasks)
        publish_form.set_progress_reporter(progress)

        # show pre-publish progress:
        publish_form.show_publish_progress("Doing Pre-Publish...")
        progress.reset()
        
        # make dialog modal whilst we're doing work:
        """
        (AD) - whilst this almost works, returning from modal state seems to
        completely mess up the window parenting in Maya so may need to have another
        way to do this or (more likely) move it to a separate dialog!
        
        geom = publish_form.window().geometry() 
        publish_form.window().setWindowModality(QtCore.Qt.ApplicationModal)
        publish_form.window().hide()
        publish_form.window().show()
        publish_form.window().setGeometry(geom)
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
            self._do_pre_publish(primary_task, secondary_tasks, progress.report)
        except TankError, e:
            QtGui.QMessageBox.information(publish_form, "Pre-publish Failed", 
                                          "Pre-Publish Failed!\n\n%s" % e)
            publish_form.show_publish_details()
            return
        except Exception, e:
            self._app.log_exception("Pre-publish Failed")
            publish_form.show_publish_details()
            return
        finally:
            """
            # restore window to be modeless
            publish_form.window().setWindowModality(QtCore.Qt.NonModal)
            publish_form.window().hide()
            publish_form.window().show()  
            publish_form.window().setGeometry(geom)
            QtGui.QApplication.processEvents()
            """
            pass
        
        # check that we can continue:
        num_errors = 0
        for task in selected_tasks:
            num_errors += len(task.pre_publish_errors)
        if num_errors > 0:
            publish_form.show_publish_details()
            
            # TODO: replace with Tank dialog
            res = QtGui.QMessageBox.warning(publish_form, "Pre-publish Errors", 
                                             "Pre-publish returned %d errors\n\nWould you like to publish anyway?" % num_errors,
                                             QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
            if res != QtGui.QMessageBox.Yes:
                return
                
        # show publish progress:
        publish_form.show_publish_progress("Publishing...")
        progress.reset()

        # save the thumbnail to a temporary location:
        thumbnail_path = ""
        if thumbnail and not thumbnail.isNull():
            tmp_file = tempfile.NamedTemporaryFile(suffix=".png", prefix="tanktmp", delete=False)
            thumbnail_path = tmp_file.name
            tmp_file.close()
            thumbnail.save(thumbnail_path)
                
        # do the publish
        publish_errors = []
        do_post_publish = False
        try:            
            # do primary publish:
            primary_path = self._do_primary_publish(primary_task, sg_task, thumbnail_path, comment, progress.report)
            if not primary_path:
                raise TankError("Primary publish didn't return a path!")
            do_post_publish = True
            
            # do secondary publishes:
            self._do_secondary_publish(secondary_tasks, primary_path, sg_task, thumbnail_path, comment, progress.report)
            
        except TankError, e:
            publish_errors.append("%s" % e)
        except Exception, e:
            self._app.log_exception("Publish Failed")
            publish_errors.append("%s" % e)
        finally:
            # delete temporary thumbnail file:
            if thumbnail_path:
                os.remove(thumbnail_path)
        
        # check for any other publish errors:
        for task in secondary_tasks:
            for error in task.publish_errors:
                publish_errors.append("%s, %s: %s" % (task.output.display_name, task.item.name, error))
        
        # if publish didn't fail then do post publish:
        if do_post_publish:
            publish_form.show_publish_progress("Doing Post-Publish...")
            progress.reset(1)
            
            try:
                self._do_post_publish(progress.report)
            except TankError, e:
                publish_errors.append("Post-publish: %s" % e)
            except Exception, e:
                self._app.log_exception("Post-publish Failed")
                publish_errors.append("Post-publish: %s" % e)
        else:
            # inform that post-publish didn't run
            publish_errors.append("Post-publish was not run due to previous errors!")
            
        # show publish result:
        publish_form.show_publish_result(not publish_errors, publish_errors)

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
        
    def _do_pre_publish(self, primary_task, secondary_tasks, progress_cb):
        """
        Do pre-publish pass on tasks using the pre-publish hook
        """
        
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
                
        for task in secondary_tasks:
            result = result_index.get((task.item.name, task.output.name))
            if result:
                task.pre_publish_errors = result["errors"]
            else:
                task.pre_publish_errors = []
    
    
    def _do_primary_publish(self, primary_task, sg_task, thumbnail_path, comment, progress_cb):
        """
        Do publish of primary task with the primary publish hook
        """
        primary_path = self._app.execute_hook("hook_primary_publish",  
                                              task=primary_task.as_dictionary(), 
                                              work_template = self._work_template,
                                              comment = comment,
                                              thumbnail_path = thumbnail_path,
                                              sg_task = sg_task,
                                              progress_cb=progress_cb)
        return primary_path
        
        
    def _do_secondary_publish(self, secondary_tasks, primary_publish_path, sg_task, thumbnail_path, comment, progress_cb):
        """
        Do publish of secondary tasks using the secondary publish hook
        """
        # do publish of secondary tasks:            
        hook_tasks = [task.as_dictionary() for task in secondary_tasks]
        p_results = self._app.execute_hook("hook_secondary_publish",  
                                             tasks=hook_tasks, 
                                             work_template = self._work_template,
                                             comment = comment,
                                             thumbnail_path = thumbnail_path,
                                             sg_task = sg_task,
                                             primary_publish_path=primary_publish_path,
                                             progress_cb=progress_cb)
        
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
                
        for task in secondary_tasks:
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
    

    