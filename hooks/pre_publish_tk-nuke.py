"""
Copyright (c) 2013 Shotgun Software, Inc
----------------------------------------------------

"""
import os
import nuke

import tank
from tank import Hook

class PrePublishHook(Hook):
    """
    Single hook that implements pre-publish functionality
    """
    def execute(self, tasks, work_template, progress_cb, **kwargs):
        """
        Pre-publish tasks for Nuke
        """
        results = []
        
        # we will need the write node app if we have any render outputs to validate
        write_node_app = tank.platform.current_engine().apps.get("tk-nuke-writenode")
        
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
                # primary output is the nuke script - validate that it
                # can be published:
                script_file = nuke.root().name().replace("/", os.path.sep)
                if script_file:
                    script_file = os.path.abspath(script_file)
                errors.extend(self._validate_work_file(script_file, work_template, output))
            elif output["name"] == "render":
                # validate that the write node has rendered images to publish:
                # ...
                if not write_node_app:
                    errors.append("Unable to validate write node '%s' without tk-nuke-writenode app!" % item["name"])
                else:
                    # get write node:
                    write_node = item.get("other_params", dict()).get("node")
                    if not write_node:
                        errors.append("Could not find nuke node for item '%s'!" % item["name"])
                    else:
                        # do pre-publish:              
                        errors = self._nuke_pre_publish_write_node_render(write_node, write_node_app)
            else:
                # other output types have no validation
                pass        

            # if there is anything to report then add to result
            if len(errors) > 0:
                # add result:
                results.append({"task":task, "errors":errors})
            
        return results
        
    def _nuke_pre_publish_write_node_render(self, write_node, write_node_app):
        """
        Pre-publish render output for write node
        """
        errors = []
        try:
            # get list of render files:
            render_files = write_node_app.get_node_render_files(write_node)
            if len(render_files) == 0:
                is_valid = False
                errors.append("No render files exist to be published!")
            else:
                # ensure that published files don't already exist
        
                # need the render template, publish template and tank type which are all 
                # defined per node (profile) in the tk-nuke-writenode app
                render_template = write_node_app.get_node_render_template(write_node)
                publish_template = write_node_app.get_node_publish_template(write_node)                        
                tank_type = write_node_app.get_node_tank_type(write_node)
                
                # check files:
                existing_files = []
                for rf in render_files:
                    # construct the publish path:
                    fields = render_template.get_fields(rf)
                    fields["TankType"] = tank_type
                    target_path = publish_template.apply_fields(fields)
                
                    if os.path.exists(target_path):
                        existing_files.append(target_path)
                        
                if existing_files:
                    # one or more published files already exist!
                    msg = "Published render file '%s'" % existing_files[0]
                    if len(existing_files) > 1:
                        msg += " (+%d others)" % (len(existing_files)-1)
                    msg += " already exists!"
                    errors.append(msg)
        except Exception, e:
            errors.append("Unhandled exception: %s" % e)

        return errors
    
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

    
    
    