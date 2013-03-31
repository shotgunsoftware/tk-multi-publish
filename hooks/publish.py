"""
Copyright (c) 2013 Shotgun Software, Inc
----------------------------------------------------

"""
import os
import shutil
import tank
from tank import Hook

class PublishHook(Hook):
    """
    Single hook that implements publish functionality
    """
    def execute(self, engine_name, tasks, work_template, comment, thumbnail_path, sg_task, progress_cb, **kwargs):
        """
        Main hook entry point
        :engin_name: name of the currently running engine
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
        publisher = Publisher.create(engine_name, self.parent, comment, thumbnail_path, sg_task)
        if not publisher:
            raise Exception("Don't know how to publish tasks for engine: %s" % engine_name)
        return publisher.execute(tasks, work_template, progress_cb, **kwargs)
        
        
class Publisher(object):
    """
    Base class for engine specific publishers
    """
    @staticmethod
    def create(engine_name, parent, comment, thumbnail_path, sg_task):
        """
        Helper factory method to create a publisher instance for
        the given engine
        """
        publisher_classes = {"tk-maya":MayaPublisher, 
                             "tk-nuke":NukePublisher}
        cls = publisher_classes.get(engine_name, parent)
        if cls:
            return cls(parent, comment, thumbnail_path, sg_task)
        
    def __init__(self, parent, comment, thumbnail_path, sg_task):
        self._parent = parent
        self._comment = comment
        self._thumbnail_path = thumbnail_path
        self._sg_task = sg_task
        
    @property
    def parent(self):
        """
        Parent as passed in from the hook.  This will be the 
        thing that created the hook, e.g. the app
        """
        return self._parent

    def execute(self, tasks, work_template, progress_cb, **kwargs):
        """
        Does nothing
        """
        raise NotImplementedError("Publish not implemented")

    def _get_next_work_file_version(self, fields, work_template):
        """
        Find the next available version for the specified work_file
        """
        existing_versions = self.parent.tank.paths_from_template(work_template, fields, ["version"])
        version_numbers = [work_template.get_fields(v).get("version") for v in existing_versions]
        curr_v_no = fields["version"]
        max_v_no = max(version_numbers)
        return max(curr_v_no, max_v_no) + 1

    def _copy_file(self, source_path, target_path):
        """
        Copy file, ensuring target directory exists
        """
        
        # create the publish folder if it doesn't exist
        dirname = os.path.dirname(target_path)
        if not os.path.isdir(dirname):            
            old_umask = os.umask(0)
            os.makedirs(dirname, 0777)
            os.umask(old_umask)            
        
        shutil.copy(source_path, target_path) 
        
        # make it readonly
        os.chmod(target_path, 0444)

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
        




class NukePublisher(Publisher):
    """
    Engine specific publisher for Nuke
    """
    def execute(self, tasks, work_template, progress_cb, **kwargs):
        """
        Publish tasks for Nuke
        """
        import nuke
        
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
            published_script_path = self._publish_script(primary_task, work_template)
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
        self._version_up_script(work_template)

        return results

    def _publish_write_node_render(self, write_node, write_node_app, published_script_path):
        """
        Publish render output for write node
        """
        import nuke
 
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
                self._copy_file(rf, target_path)
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
        
    def _publish_script(self, task, work_template):
        """
        Publish the main Maya scene
        """
        import nuke
        
        # get scene path
        script_path = nuke.root().name().replace("/", os.path.sep)
        if script_path == "Root":
            script_path = ""
        script_path = os.path.abspath(script_path)
        
        if not work_template.validate(script_path):
            raise Exception("File '%s' is not a valid work path, unable to publish!" % script_path)
        
        # use templates to convert to publish path:
        output = task["output"]
        fields = work_template.get_fields(script_path)
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
            self._copy_file(script_path, publish_path)
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

    def _version_up_script(self, work_template):
        """
        Version up the script and ensure any associated write nodes 
        are also updated
        """
        import nuke
        
        original_path = nuke.root().name()
        script_path = os.path.abspath(original_path.replace("/", os.path.sep))
        fields = work_template.get_fields(script_path)
        next_version = self._get_next_work_file_version(fields, work_template)
        fields["version"] = next_version 
        new_path = work_template.apply_fields(fields)
        
        self.parent.log_debug("Version up work file %s --> %s..." % (script_path, new_path))
        try:
            # rename script:
            nuke.root()["name"].setValue(new_path)
    
            # reset all write nodes:
            # TODO: expose interface on tk-nuke-writenode to do this
            """
            for write_node in self._write_node_handler.get_nodes():
                self._write_node_handler.reset_render_path(write_node)
            """
            
            # save script:
            nuke.scriptSaveAs(new_path)
        except:
            nuke.root()["name"].setValue(original_path)
            raise


class MayaPublisher(Publisher):
    """
    Engine specific publisher for Maya
    """
    def execute(self, tasks, work_template, progress_cb, **kwargs):
        """
        Publish tasks for Maya
        """
        
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
                    self._publish_scene(task, work_template)
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
        self._version_up_scene(work_template)
             
        return results
        
    def _publish_scene(self, task, work_template):
        """
        Publish the main Maya scene
        """
        import maya.cmds as mc
        
        # get scene path
        scene_path = os.path.abspath(mc.file(query=True, sn=True))
        
        if not work_template.validate(scene_path):
            raise Exception("File '%s' is not a valid work path, unable to publish!" % scene_path)
        
        # use templates to convert to publish path:
        output = task["output"]
        fields = work_template.get_fields(scene_path)
        fields["TankType"] = output["tank_type"]
        publish_template = output["publish_template"]
        publish_path = publish_template.apply_fields(fields)
        
        if os.path.exists(publish_path):
            raise Exception("The published file named '%s' already exists!" % publish_path)
        
        # save the scene:
        self.parent.log_debug("Saving the scene...")
        mc.file(save=True, force=True)
        
        # copy the file:
        try:
            publish_folder = os.path.dirname(publish_path)
            self.parent.ensure_folder_exists(publish_folder)
            self.parent.log_debug("Copying %s --> %s..." % (scene_path, publish_path))
            self._copy_file(scene_path, publish_path)
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

    def _version_up_scene(self, work_template):
        """
        Version up the current Maya scene to the new version.
        """
  
        import maya.cmds as mc
  
        scene_path = os.path.abspath(mc.file(query=True, sn=True))
        fields = work_template.get_fields(scene_path)
        next_version = self._get_next_work_file_version(fields, work_template)
        fields["version"] = next_version 
        new_scene_path = work_template.apply_fields(fields)
        
        self.parent.log_debug("Version up work file %s --> %s..." % (scene_path, new_scene_path))
        
        # save the file
        mc.file(rename=new_scene_path)
        mc.file(save=True)
        




