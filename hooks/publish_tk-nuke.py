"""
Copyright (c) 2013 Shotgun Software, Inc
----------------------------------------------------

"""
import os
import shutil
import nuke

import tank
from tank import Hook

class PublishHook(Hook):
    """
    Single hook that implements publish functionality
    """
            
    def execute(self, tasks, work_template, comment, thumbnail_path, sg_task, progress_cb, **kwargs):
        """
        Main hook entry point
        :tasks:         List of tasks to be published.  Each task is be a dictionary 
                        containing the following keys:
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
        
        :returns:       A list of any tasks that had problems that need to be reported 
                        in the UI.  Each item in the list should be a dictionary containing 
                        the following keys:
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
        # cache the args for easy access later
        self._work_template = work_template
        self._sg_task = sg_task
        self._comment = comment
        self._thumbnail_path = thumbnail_path
        
        results = []
        
        # first, find and publish the primary task/script:
        primary_task = None
        for task in tasks:
            if task["output"]["name"] == "primary":
                primary_task = task
                break
        if not primary_task:
            raise Exception("Failed to find primary task to publish!")

        progress_cb(0.0, "Publishing %s" % primary_task["item"]["name"])

        published_script_path = None         
        try:
            published_script_path = self._publish_script(primary_task)
        except Exception, e:
            # can't do the publish without if the script publish fails!
            results.append({"task":primary_task, "errors":["Publish failed - %s" % e]})
            return results
            
        # we will need the write node app if we have any render outputs to validate
        write_node_app = tank.platform.current_engine().apps.get("tk-nuke-writenode")
        
        # process rest of tasks:
        num_tasks = len(tasks)
        for ti, task in enumerate(tasks):
            
            if task == primary_task:
                continue
            
            item = task["item"]
            output = task["output"]
            errors = []
            
            # report progress:
            progress_cb((100.0/num_tasks) * (ti+1), "Publishing %s" % item["name"])
        
            # depending on output type:
            if output["name"] == "render":
                # publish write-node rendered sequence                
                try:
                    if not write_node_app:
                        raise Exception("Unable to validate write node without tk-nuke-writenode app!")
                    
                    write_node = item.get("other_params", dict()).get("node")
                    if not write_node:
                        raise Exception("Could not determined node for item '%s'!" % item["name"])
                    
                    self._publish_write_node_render(write_node, write_node_app, published_script_path)
                except Exception, e:
                    errors.append("Publish failed - %s" % e)
            else:
                # this should never happen!
                errors.append("Don't know how to publish this item!")
                
            # if there is anything to report then add to result
            if len(errors) > 0:
                # add result:
                results.append({"task":task, "errors":errors})
                
        # finally, version up the script:
        self._version_up_script(write_node_app)

        return results

    def _publish_write_node_render(self, write_node, write_node_app, published_script_path):
        """
        Publish render output for write node
        """
 
        # get info we need in order to do the publish:
        render_path = write_node_app.get_node_render_path(write_node)
        render_files = write_node_app.get_node_render_files(write_node)
        render_template = write_node_app.get_node_render_template(write_node)
        publish_template = write_node_app.get_node_publish_template(write_node)                        
        tank_type = write_node_app.get_node_tank_type(write_node)
        
        # publish (copy files):
        for rf in render_files:
            # construct the publish path:
            fields = render_template.get_fields(rf)
            fields["TankType"] = tank_type
            target_path = publish_template.apply_fields(fields)

            # copy the file
            try:
                target_folder = os.path.dirname(target_path)
                self.parent.ensure_folder_exists(target_folder)
                self.parent.copy_file(rf, target_path)
            except Exception, e:
                raise Exception("Failed to copy file from %s to %s - %s" % (rf, target_path, e))
            
        # use the render path to work out the publish 'file' and name:
        render_path_fields = render_template.get_fields(render_path)
        render_path_fields["TankType"] = tank_type
        publish_path = publish_template.apply_fields(render_path_fields)
            
        # construct publish name:
        publish_name = ""
        rp_name = render_path_fields.get("name")
        rp_channel = render_path_fields.get("channel")
        if rp_name is None and rp_channel is None:
            publish_name = "Publish"
        elif rp_name is None:
            publish_name = "Channel %s" % rp_channel
        elif rp_channel is None:
            publish_name = rp_name
        else:
            publish_name = "%s, Channel %s" % (rp_name, rp_channel)
        
        publish_version = render_path_fields["version"]
            
        # get/generate thumbnail:
        thumbnail_path = write_node_app.generate_node_thumbnail(write_node)
            
        # register publish:
        self._register_publish(publish_path, publish_name, publish_version, tank_type, [published_script_path], thumbnail_path)
        
        return publish_path        
        
    def _publish_script(self, task):
        """
        Publish the main Maya scene
        """
        
        # get scene path
        script_path = nuke.root().name().replace("/", os.path.sep)
        if script_path == "Root":
            script_path = ""
        script_path = os.path.abspath(script_path)
        
        if not self._work_template.validate(script_path):
            raise Exception("File '%s' is not a valid work path, unable to publish!" % script_path)
        
        # use templates to convert to publish path:
        output = task["output"]
        fields = self._work_template.get_fields(script_path)
        fields["TankType"] = output["tank_type"]
        publish_template = output["publish_template"]
        publish_path = publish_template.apply_fields(fields)
        
        if os.path.exists(publish_path):
            raise Exception("The published file named '%s' already exists!" % publish_path)
        
        # save the scene:
        self.parent.log_debug("Saving the Script...")
        nuke.scriptSave()
        
        # copy the file:
        try:
            publish_folder = os.path.dirname(publish_path)
            self.parent.ensure_folder_exists(publish_folder)
            self.parent.log_debug("Copying %s --> %s..." % (script_path, publish_path))
            self.parent.copy_file(script_path, publish_path)
        except Exception, e:
            raise Exception("Failed to copy file from %s to %s - %s" % (script_path, publish_path, e))

        # work out name for publish:
        publish_name = fields.get("name").capitalize()
        if not publish_name:
            publish_name = os.path.basename(script_path)

        # finally, register the publish:
        self._register_publish(publish_path, publish_name, fields["version"], output["tank_type"], self._find_script_dependencies())
        
        return publish_path
        
    def _find_script_dependencies(self):
        """
        TODO: taken from tk-nuke-publish, not checked!
        """
        
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

    def _version_up_script(self, write_node_app):
        """
        Version up the script and ensure any associated write nodes 
        are also updated
        """
        
        # find the new version and path:
        original_path = nuke.root().name()
        script_path = os.path.abspath(original_path.replace("/", os.path.sep))
        fields = self._work_template.get_fields(script_path)
        next_version = self._get_next_work_file_version(fields)
        fields["version"] = next_version 
        new_path = self._work_template.apply_fields(fields)
        
        self.parent.log_debug("Version up work file %s --> %s..." % (script_path, new_path))

        # rename script:
        nuke.root()["name"].setValue(new_path)
    
        if write_node_app:
            self.parent.log_debug("Resetting render paths for all write nodes")
            # reset render paths for all write nodes:
            for wn in write_node_app.get_write_nodes():
                 write_node_app.reset_node_render_path(wn)
                        
        # save the script:
        nuke.scriptSaveAs(new_path)

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
        






