"""
Copyright (c) 2013 Shotgun Software, Inc
----------------------------------------------------

"""
import os
import maya.cmds as cmds

import tank
from tank import Hook

class PrePublishHook(Hook):
    """
    Single hook that implements pre-publish functionality
    """
    def execute(self, tasks, work_template, progress_cb, **kwargs):
        """
        Main hook entry point
        :tasks:         List of tasks to be pre-published.  Each task is be a 
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
                        
        :returns:       A list of any tasks that were found which have problems that
                        need to be reported in the UI.  Each item in the list should
                        be a dictionary containing the following keys:
                        {
                            task:   Dictionary
                                    This is the task that was passed into the hook and
                                    should not be modified
                                    {
                                        item:...
                                        output:...
                                    }
                                    
                            errors: List
                                    A list of error messages (strings) to report    
                        }
        """       
        results = []
        
        # validate tasks:
        num_tasks = len(tasks)
        for ti, task in enumerate(tasks):
            item = task["item"]
            output = task["output"]
            errors = []
        
            # report progress:
            progress = (100.0/num_tasks) * ti
            msg = "Validating %s for output %s" % (item["name"], output["name"])
            progress_cb(progress, msg)
        
            # depending on output type, do some specific validation:
            if output["name"] == "primary":
                # primary output is the maya scene - validate 
                # that it can be published:
                scene_file = cmds.file(query=True, sn=True)
                if scene_file:
                    scene_file = os.path.abspath(scene_file)
                errors.extend(self._validate_work_file(scene_file, work_template, output))
            else:
                # don't know how to publish other output types!
                errors.append("Don't know how to publish this item!")        

            # if there is anything to report then add to result
            if len(errors) > 0:
                # add result:
                results.append({"task":task, "errors":errors})
            
        return results
    
    def _validate_work_file(self, path, work_template, output):
        """
        Validate that the given path is a valid work file and that
        the published version of it doesn't already exist.
        
        Return the new version number that the scene should be
        up'd to after publish
        """
        errors = []
        
        if not work_template.validate(path):
            work_template.get_fields(path)
            return ["File '%s' is not a valid work path, unable to publish!" % path]
        
        # find the publish path:
        fields = work_template.get_fields(path)
        fields["TankType"] = output["tank_type"]
        publish_template = output["publish_template"]
        publish_path = publish_template.apply_fields(fields) 
        
        if os.path.exists(publish_path):
            return ["A published file named '%s' already exists!" % publish_path]
        
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

    
    