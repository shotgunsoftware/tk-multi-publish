"""
Copyright (c) 2013 Shotgun Software, Inc
----------------------------------------------------
"""
import os

import tank
from tank import Hook
from tank import TankError

class PrimaryPublishHook(Hook):
    """
    Single hook that implements publish of the primary task
    """    
    def execute(self, task, work_template, comment, thumbnail_path, sg_task, progress_cb, **kwargs):
        """
        Main hook entry point
        :task:          Primary task to be published.  This is a
                        dictionary containing the following keys:
                        {   
                            item:   Dictionary
                                    This is the item returned by the scan hook 
                                    {   
                                        name:           String
                                        description:    String
                                        type:           String
                                        other_params:   Dictionary
                                    }
                                   
                            output: Dictionary
                                    This is the output as defined in the configuration - the 
                                    primary output will always be named 'primary' 
                                    {
                                        name:             String
                                        publish_template: template
                                        tank_type:        String
                                    }
                        }
                        
        :work_template: template
                        This is the template defined in the config that
                        represents the current work file
               
        :comment:       String
                        The comment provided for the publish
                        
        :thumbnail:     Path string
                        The default thumbnail provided for the publish
                        
        :sg_task:       Dictionary (shotgun entity description)
                        The shotgun task to use for the publish    
                        
        :progress_cb:   Function
                        A progress callback to log progress during pre-publish.  Call:
                        
                            progress_cb(percentage, msg)
                             
                        to report progress to the UI
        
        :returns:       Path String
                        Hook should return the path of the primary publish so that it
                        can be passed as a dependency to all secondary publishes
        
                        Hook should raise a TankError if publish of the 
                        primary task fails
        """
        # get the engine name from the parent object (app/engine/etc.)
        engine_name = self.parent.engine.name
        
        # depending on engine:
        if engine_name == "tk-maya":
            return self._do_maya_publish(task, work_template, comment, thumbnail_path, sg_task, progress_cb)
        elif engine_name == "tk-nuke":
            return self._do_nuke_publish(task, work_template, comment, thumbnail_path, sg_task, progress_cb)
        elif engine_name == "tk-houdini":
            return self._do_houdini_publish(task, work_template, comment, thumbnail_path, sg_task, progress_cb)
        else:
            raise TankError("Unable to perform publish for unhandled engine %s" % engine_name)
        
    def _do_maya_publish(self, task, work_template, comment, thumbnail_path, sg_task, progress_cb):
        """
        Publish the main Maya scene
        """
        import maya.cmds as cmds
        
        progress_cb(0.0, "Finding scene dependencies", task)
        dependencies = self._maya_find_additional_scene_dependencies()
        
        # get scene path
        scene_path = os.path.abspath(cmds.file(query=True, sn=True))
        
        if not work_template.validate(scene_path):
            raise TankError("File '%s' is not a valid work path, unable to publish!" % scene_path)
        
        # use templates to convert to publish path:
        output = task["output"]
        fields = work_template.get_fields(scene_path)
        fields["TankType"] = output["tank_type"]
        publish_template = output["publish_template"]
        publish_path = publish_template.apply_fields(fields)
        
        if os.path.exists(publish_path):
            raise TankError("The published file named '%s' already exists!" % publish_path)
        
        # save the scene:
        progress_cb(10.0, "Saving the scene")
        self.parent.log_debug("Saving the scene...")
        cmds.file(save=True, force=True)
        
        # copy the file:
        progress_cb(50.0, "Copying the file")
        try:
            publish_folder = os.path.dirname(publish_path)
            self.parent.ensure_folder_exists(publish_folder)
            self.parent.log_debug("Copying %s --> %s..." % (scene_path, publish_path))
            self.parent.copy_file(scene_path, publish_path, task)
        except Exception, e:
            raise TankError("Failed to copy file from %s to %s - %s" % (scene_path, publish_path, e))

        # work out publish name:
        publish_name = fields.get("name").capitalize()
        if not publish_name:
            publish_name = os.path.basename(script_path)

        # finally, register the publish:
        progress_cb(75.0, "Registering the publish")
        self._register_publish(publish_path, 
                               publish_name, 
                               sg_task, 
                               fields["version"], 
                               output["tank_type"],
                               comment,
                               thumbnail_path, 
                               dependencies)
        
        progress_cb(100)
        
        return publish_path
        
    def _maya_find_additional_scene_dependencies(self):
        """
        Find additional dependencies from the scene
        """
        # initial implementation does nothing!
        return []

    def _do_nuke_publish(self, task, work_template, comment, thumbnail_path, sg_task, progress_cb):
        """
        Publish the main Nuke script
        """
        import nuke
        
        progress_cb(0.0, "Finding dependencies", task)
        dependencies = self._nuke_find_script_dependencies()
        
        # get scene path
        script_path = nuke.root().name().replace("/", os.path.sep)
        if script_path == "Root":
            script_path = ""
        script_path = os.path.abspath(script_path)
        
        if not work_template.validate(script_path):
            raise TankError("File '%s' is not a valid work path, unable to publish!" % script_path)
        
        # use templates to convert to publish path:
        output = task["output"]
        fields = work_template.get_fields(script_path)
        fields["TankType"] = output["tank_type"]
        publish_template = output["publish_template"]
        publish_path = publish_template.apply_fields(fields)
        
        if os.path.exists(publish_path):
            raise TankError("The published file named '%s' already exists!" % publish_path)
        
        # save the scene:
        progress_cb(25.0, "Saving the script")
        self.parent.log_debug("Saving the Script...")
        nuke.scriptSave()
        
        # copy the file:
        progress_cb(50.0, "Copying the file")
        try:
            publish_folder = os.path.dirname(publish_path)
            self.parent.ensure_folder_exists(publish_folder)
            self.parent.log_debug("Copying %s --> %s..." % (script_path, publish_path))
            self.parent.copy_file(script_path, publish_path, task)
        except Exception, e:
            raise TankError("Failed to copy file from %s to %s - %s" % (script_path, publish_path, e))

        # work out name for publish:
        publish_name = fields.get("name").capitalize()
        if not publish_name:
            publish_name = os.path.basename(script_path)

        # finally, register the publish:
        progress_cb(75.0, "Registering the publish")
        self._register_publish(publish_path, 
                               publish_name, 
                               sg_task, 
                               fields["version"], 
                               output["tank_type"],
                               comment,
                               thumbnail_path, 
                               dependencies)
        
        progress_cb(100)
        
        return publish_path
        
    def _nuke_find_script_dependencies(self):
        """
        Find all dependencies for the current nuke script
        """
        import nuke
        
        # figure out all the inputs to the scene and pass them as dependency candidates
        dependency_paths = []
        for read_node in nuke.allNodes("Read"):
            # make sure we normalize file paths
            file_name = read_node.knob("file").evaluate().replace('/', os.path.sep)
            # validate against all our templates
            for template in self.parent.tank.templates.values():
                if template.validate(file_name):
                    fields = template.get_fields(file_name)
                    # translate into a form that represents the general
                    # tank write node path.
                    fields["SEQ"] = "FORMAT: %d"
                    fields["eye"] = "%V"
                    dependency_paths.append(template.apply_fields(fields))
                    break

        return dependency_paths

    def _do_houdini_publish(self, task, work_template, comment, thumbnail_path, sg_task, progress_cb):
        """
        Publish the main Houdini scene
        """
        import hou

        progress_cb(0.0, "Finding scene dependencies", task)
        dependencies = self._houdini_find_additional_scene_dependencies()

        # get scene path
        scene_path = os.path.abspath(hou.hipFile.name())

        if not work_template.validate(scene_path):
            raise TankError("File '%s' is not a valid work path, unable to publish!" % scene_path)

        # use templates to convert to publish path:
        output = task["output"]
        fields = work_template.get_fields(scene_path)
        fields["TankType"] = output["tank_type"]
        publish_template = output["publish_template"]
        publish_path = publish_template.apply_fields(fields)

        if os.path.exists(publish_path):
            raise TankError("The published file named '%s' already exists!" % publish_path)

        # save the scene:
        progress_cb(10.0, "Saving the scene")
        self.parent.log_debug("Saving the scene...")
        hou.hipFile.save()

        # copy the file:
        progress_cb(50.0, "Copying the file")
        try:
            publish_folder = os.path.dirname(publish_path)
            self.parent.ensure_folder_exists(publish_folder)
            self.parent.log_debug("Copying %s --> %s..." % (scene_path, publish_path))
            self.parent.copy_file(scene_path, publish_path, task)
        except Exception, e:
            raise TankError("Failed to copy file from %s to %s - %s" % (scene_path, publish_path, e))

        # work out publish name:
        publish_name = fields.get("name").capitalize()
        if not publish_name:
            publish_name = os.path.basename(script_path)

        # finally, register the publish:
        progress_cb(75.0, "Registering the publish")
        self._register_publish(publish_path,
                               publish_name,
                               sg_task,
                               fields["version"],
                               output["tank_type"],
                               comment,
                               thumbnail_path,
                               dependencies)

        progress_cb(100)

        return publish_path

    def _houdini_find_additional_scene_dependencies(self):
        """
        Find additional dependencies from the scene
        """
        # initial implementation does nothing!
        return []

    def _register_publish(self, path, name, sg_task, publish_version, tank_type, comment, thumbnail_path, dependency_paths=None):
        """
        Helper method to register publish using the 
        specified publish info.
        """
        # construct args:
        args = {
            "tk": self.parent.tank,
            "context": self.parent.context,
            "comment": comment,
            "path": path,
            "name": name,
            "version_number": publish_version,
            "thumbnail_path": thumbnail_path,
            "task": sg_task,
            "dependency_paths": dependency_paths,
            "tank_type":tank_type,
        }
        
        # register publish;
        sg_data = tank.util.register_publish(**args)
        
        return sg_data