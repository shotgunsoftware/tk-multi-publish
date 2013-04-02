"""
Copyright (c) 2013 Shotgun Software, Inc
----------------------------------------------------

"""
import os
import shutil
import maya.cmds as cmds

import tank
from tank import Hook

class PublishHook(Hook):
    """
    Single hook that implements publish functionality
    """    
    def execute(self, tasks, work_template, comment, thumbnail_path, sg_task, progress_cb, **kwargs):
        """
        Main hook entry point
        :tasks: list of tasks to be published.  Each task is of the form:
        {
            # 'item' is the item returned by the scan hook
            "item":{   
                    "name":str
                    "description":str
                    "type":str
                    "other_params":dict()
                   }
                   
            # 'output' is defined in the configuration - the primary output will 
            # always be named 'primary'
            "output":{
                    "name":str
                    "publish_template":template
                    "tank_type":str                    
                     }
        }
        :work_template: this is the template defined in the config that
        represents the current work file
        :comment: the comment provided for the publish
        :thumbnail: the default thumbnail provided for the publish
        :sg_task: the shotgun task to use for the publish
        :progress_cb: a progress callback to log progress during the publish
        """
        # cache the args for easy access later
        self._work_template = work_template
        self._sg_task = sg_task
        self._comment = comment
        self._thumbnail_path = thumbnail_path
        
        results = []
        
        # publish all tasks:
        num_tasks = len(tasks)
        for ti, task in enumerate(tasks):
            item = task["item"]
            output = task["output"]
            errors = []
        
            # report progress:
            progress = (100.0/num_tasks) * ti
            msg = "Publishing %s" % item["name"]
            progress_cb(progress, msg)
        
            # depending on output type:
            if output["name"] == "primary":
                # publish the main scene                
                try:
                    self._publish_scene(task)
                except Exception, e:
                    errors.append("Publish failed - %s" % e)
            else:
                # this should never happen!
                errors.append("Don't know how to publish this item!")

            # if there is anything to report then add to result
            if len(errors) > 0:
                # add result:
                results.append({"task":task, "errors":errors})
            
        # finally, up-version the work file:
        self._version_up_scene()
             
        return results
        
    def _publish_scene(self, task):
        """
        Publish the main Maya scene
        """
        
        # get scene path
        scene_path = os.path.abspath(cmds.file(query=True, sn=True))
        
        if not self._work_template.validate(scene_path):
            raise Exception("File '%s' is not a valid work path, unable to publish!" % scene_path)
        
        # use templates to convert to publish path:
        output = task["output"]
        fields = self._work_template.get_fields(scene_path)
        fields["TankType"] = output["tank_type"]
        publish_template = output["publish_template"]
        publish_path = publish_template.apply_fields(fields)
        
        if os.path.exists(publish_path):
            raise Exception("The published file named '%s' already exists!" % publish_path)
        
        # save the scene:
        self.parent.log_debug("Saving the scene...")
        cmds.file(save=True, force=True)
        
        # copy the file:
        try:
            publish_folder = os.path.dirname(publish_path)
            self.parent.ensure_folder_exists(publish_folder)
            self.parent.log_debug("Copying %s --> %s..." % (scene_path, publish_path))
            self.parent.copy_file(scene_path, publish_path)
        except Exception, e:
            raise Exception("Failed to copy file from %s to %s - %s" % (scene_path, publish_path, e))

        # work out publish name:
        publish_name = fields.get("name").capitalize()
        if not publish_name:
            publish_name = os.path.basename(script_path)

        # finally, register the publish:
        self._register_publish(publish_path, publish_name, fields["version"], output["tank_type"], self._find_additional_scene_dependencies())
        
        return publish_path
        
    def _find_additional_scene_dependencies(self):
        """
        Find additional dependencies from the scene
        """
        # initial implementation does nothing!
        return []

    def _version_up_scene(self):
        """
        Version up the current Maya scene to the new version.
        """
  
        scene_path = os.path.abspath(cmds.file(query=True, sn=True))
        fields = self._work_template.get_fields(scene_path)
        next_version = self._get_next_work_file_version(fields)
        fields["version"] = next_version 
        new_scene_path = self._work_template.apply_fields(fields)
        
        self.parent.log_debug("Version up work file %s --> %s..." % (scene_path, new_scene_path))
        
        # save the file
        cmds.file(rename=new_scene_path)
        cmds.file(save=True)
        
    def _get_next_work_file_version(self, fields):
        """
        Find the next available version for the specified work_file
        """
        existing_versions = self.parent.tank.paths_from_template(self._work_template, fields, ["version"])
        version_numbers = [self._work_template.get_fields(v).get("version") for v in existing_versions]
        curr_v_no = fields["version"]
        max_v_no = max(version_numbers)
        return max(curr_v_no, max_v_no) + 1

    def _register_publish(self, path, name, publish_version, tank_type, dependency_paths=None, thumbnail_path=None):
        """
        Helper method to register publish using the 
        specified publish info.
        
        If optional arguments are not provided then
        it will attempt to use the default values
        provided during construction
        """
        
        # construct args:
        args = {
            "tk": self.parent.tank,
            "context": self.parent.context,
            "comment": self._comment,
            "path": path,
            "name": name,
            "version_number": publish_version,
            "thumbnail_path": self._thumbnail_path,
            "task": self._sg_task,
            "dependency_paths": dependency_paths,
            "tank_type":tank_type,
        }
        if thumbnail_path:
            args["thumbnail_path"] = thumbnail_path
        if tank_type:
            args["tank_type"] = tank_type
            
        # TODO: is there anything that needs to be
        # validated before trying to register the 
        # publish?
        
        # register publish;
        sg_data = tank.util.register_publish(**args)
        
        return sg_data
        




        




