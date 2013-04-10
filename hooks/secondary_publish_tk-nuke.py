"""
Copyright (c) 2013 Shotgun Software, Inc
----------------------------------------------------

"""
import os
import shutil
import nuke

import tank
from tank import Hook
from tank import TankError

class PublishHook(Hook):
    """
    Single hook that implements publish functionality for secondary tasks
    """
            
    def execute(self, tasks, work_template, comment, thumbnail_path, sg_task, primary_publish_path, progress_cb, **kwargs):
        """
        Main hook entry point
        :tasks:         List of secondary tasks to be published.  Each task is a 
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
                     
        :primary_publish_path: Path string
                        This is the path of the primary published file as returned
                        by the primary publish hook                     
                        
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
        results = []
            
        # we will need the write node app if we have any render outputs to validate
        write_node_app = tank.platform.current_engine().apps.get("tk-nuke-writenode")
        
        # process tasks:
        for task in tasks:
            item = task["item"]
            output = task["output"]
            errors = []
            
            # report progress:
            progress_cb(0.0, "Publishing", task)
        
            # depending on output type:
            if output["name"] == "render":
                # publish write-node rendered sequence                
                try:
                    if not write_node_app:
                        raise TankError("Unable to validate write node without tk-nuke-writenode app!")
                    
                    write_node = item.get("other_params", dict()).get("node")
                    if not write_node:
                        raise TankError("Could not determined node for item '%s'!" % item["name"])
                    
                    self._publish_write_node_render(write_node, write_node_app, primary_publish_path, sg_task, comment, progress_cb)
                except Exception, e:
                    errors.append("Publish failed - %s" % e)
            else:
                # this should never happen!
                errors.append("Don't know how to publish this item!")
                
            # if there is anything to report then add to result
            if len(errors) > 0:
                # add result:
                results.append({"task":task, "errors":errors})

            progress_cb(100)

        return results

    def _publish_write_node_render(self, write_node, write_node_app, published_script_path, sg_task, comment, progress_cb):
        """
        Publish render output for write node
        """
 
        progress_cb(10, "Finding rendered files")
 
        # get info we need in order to do the publish:
        render_path = write_node_app.get_node_render_path(write_node)
        render_files = write_node_app.get_node_render_files(write_node)
        render_template = write_node_app.get_node_render_template(write_node)
        publish_template = write_node_app.get_node_publish_template(write_node)                        
        tank_type = write_node_app.get_node_tank_type(write_node)
        
        # publish (copy files):
        
        progress_cb(25, "Copying files")
        
        for fi, rf in enumerate(render_files):
            
            progress_cb(25 + (50*(len(render_files)/(fi+1))))
            
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
                raise TankError("Failed to copy file from %s to %s - %s" % (rf, target_path, e))
            
        progress_cb(80, "Registering Publish")
            
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
            
        # finally, register the publish:
        self._register_publish(publish_path, 
                               publish_name, 
                               sg_task, 
                               publish_version, 
                               tank_type,
                               comment,
                               thumbnail_path, 
                               [published_script_path])
        
        return publish_path        

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
        






