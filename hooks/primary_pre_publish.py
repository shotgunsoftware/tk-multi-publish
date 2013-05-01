"""
Copyright (c) 2013 Shotgun Software, Inc
----------------------------------------------------
"""
import os

import tank
from tank import Hook
from tank import TankError

class PrimaryPrePublishHook(Hook):
    """
    Single hook that implements pre-publish of the primary task
    """    
    def execute(self, task, work_template, progress_cb, **kwargs):
        """
        Main hook entry point
        :task:          Primary task to be pre-published.  This is a
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
                        
        :progress_cb:   Function
                        A progress callback to log progress during pre-publish.  Call:
                        
                            progress_cb(percentage, msg)
                             
                        to report progress to the UI

        :returns:       List 
                        A list of non-critical problems that should be 
                        reported to the user but not stop the publish.
                        
                        Hook should raise a TankError if the primary task
                        can't be published!
        """
        # get the engine name from the parent object (app/engine/etc.)
        engine_name = self.parent.engine.name
        
        # depending on engine:
        if engine_name == "tk-maya":
            return self._do_maya_pre_publish(task, work_template, progress_cb)
        elif engine_name == "tk-nuke":
            return self._do_nuke_pre_publish(task, work_template, progress_cb)
        elif engine_name == "tk-hiero":
            return self._do_hiero_pre_publish(task, work_template, progress_cb)
        else:
            raise TankError("Unable to perform pre-publish for unhandled engine %s" % engine_name)
        
    def _do_hiero_pre_publish(self, task, work_template, progress_cb):
        """
        Do Hiero primary pre-publish validation
        """
        import hiero

        progress_cb(0.0, "Validating current project", task)

        # get the current pproject file
        project = hiero.core.projects()[-1]
        project_file = project.path()

        # validate it:
        scene_errors = self._validate_work_file(project_file, work_template, task["output"], progress_cb)
        
        progress_cb(100)
          
        return scene_errors

    def _do_maya_pre_publish(self, task, work_template, progress_cb):
        """
        Do Maya primary pre-publish/scene validation
        """
        import maya.cmds as cmds
        
        progress_cb(0.0, "Validating current scene", task)
        
        # get the current scene file:
        scene_file = cmds.file(query=True, sn=True)
        if scene_file:
            scene_file = os.path.abspath(scene_file)
            
        # validate it:
        scene_errors = self._validate_work_file(scene_file, work_template, task["output"], progress_cb)
        
        progress_cb(100)
          
        return scene_errors
        
    def _do_nuke_pre_publish(self, task, work_template, progress_cb):
        """
        Do Nuke primary pre-publish/scene validation
        """
        import nuke
        
        progress_cb(0, "Validating current script", task)
        
        # get the current script file path:
        script_file = nuke.root().name().replace("/", os.path.sep)
        if script_file:
            script_file = os.path.abspath(script_file)
            
        # validate it
        script_errors = self._validate_work_file(script_file, work_template, task["output"], progress_cb)
        
        progress_cb(100)
        
        return script_errors
        
    def _validate_work_file(self, path, work_template, output, progress_cb):
        """
        Validate that the given path is a valid work file and that
        the published version of it doesn't already exist.
        
        Return the new version number that the scene should be
        up'd to after publish
        """
        errors = []
        
        progress_cb(25, "Validating work file")
        
        if not work_template.validate(path):
            raise TankError("File '%s' is not a valid work path, unable to publish!" % path)
        
        progress_cb(50, "Validating publish path")
        
        # find the publish path:
        fields = work_template.get_fields(path)
        fields["TankType"] = output["tank_type"]
        publish_template = output["publish_template"]
        publish_path = publish_template.apply_fields(fields) 
        
        if os.path.exists(publish_path):
            raise TankError("A published file named '%s' already exists!" % publish_path)
        
        progress_cb(75, "Validating current version")
        
        # check the version number against existing versions:
        # TODO: this check is from the original maya publish - should
        # it check against the existing published files as well? 
        # (Note: tk-nuke-publish version is practically the same atm)
        existing_versions = self.parent.tank.paths_from_template(work_template, fields, ["version"])
        version_numbers = [ work_template.get_fields(v).get("version") for v in existing_versions]
        curr_v_no = fields["version"]
        max_v_no = max(version_numbers)
        if max_v_no > curr_v_no:
            # there is a higher version number - this means that someone is working
            # on an old version of the file. Warn them about upgrading.
            errors.append("Your current work file is v%03d, however a more recent "
                   "version (v%03d) already exists. After publishing, your version "
                   "will become v%03d, thereby shadowing some previous work. " % (curr_v_no, max_v_no, max_v_no + 1))
        
        return errors
        