# Copyright (c) 2013 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.

import os
import shutil
import mari

import sgtk
from sgtk import Hook
from sgtk import TankError

class PublishHook(Hook):
    """
    Single hook that implements publish functionality for secondary tasks
    """    
    def execute(self, tasks, work_template, comment, thumbnail_path, sg_task, primary_task, primary_publish_path, progress_cb, **kwargs):
        """
        Main hook entry point
        :param tasks:                   List of secondary tasks to be published.  Each task is a 
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
                        
        :param work_template:           template
                                        This is the template defined in the config that
                                        represents the current work file
               
        :param comment:                 String
                                        The comment provided for the publish
                        
        :param thumbnail:               Path string
                                        The default thumbnail provided for the publish
                        
        :param sg_task:                 Dictionary (shotgun entity description)
                                        The shotgun task to use for the publish    
                        
        :param primary_publish_path:    Path string
                                        This is the path of the primary published file as returned
                                        by the primary publish hook
                        
        :param progress_cb:             Function
                                        A progress callback to log progress during pre-publish.  Call:
                                        
                                            progress_cb(percentage, msg)
                                             
                                        to report progress to the UI
                        
        :param primary_task:            The primary task that was published by the primary publish hook.  Passed
                                        in here for reference.  This is a dictionary in the same format as the
                                        secondary tasks above.
        
        :returns:                       A list of any tasks that had problems that need to be reported 
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
        self.__cached_publishes = None
        
        results = []
        
        # publish all tasks:
        for task in tasks:
            item = task["item"]
            output = task["output"]
            errors = []
        
            # report progress:
            progress_cb(0, "Publishing", task)
        
            # publish channel and layer outputs:
            if output["name"] in ["channel", "layer"]:
                # publish images for a layer or channel
                self.__publish_images(item, output, sg_task, comment, thumbnail_path, progress_cb)
            else:
                # don't know how to publish this output types!
                errors.append("Don't know how to publish this item!")    

            # if there is anything to report then add to result
            if len(errors) > 0:
                # add result:
                results.append({"task":task, "errors":errors})
             
            progress_cb(100)
             
        return results
    
    def __publish_images(self, item, output, sg_task, comment, thumbnail_path, progress_cb):
        """
        """
        params = item.get("other_params")
        geo_name = params["geo"]
        channel_name = params["channel"]
        layer_name = params.get("layer")
        
        # find the channel & geo to publish:
        geo = mari.geo.find(geo_name)
        if not geo:
            raise TankError("Failed to find geometry '%s'!" % geo_name)
        
        channel = geo.findChannel(channel_name)
        if not channel:
            raise TankError("Failed to find channel '%s' on '%s'!" % (channel_name, geo_name))
        
        layer = None
        if layer_name:
            layer = channel.findLayer(layer_name)
            if not layer:
                raise TankError("Failed to find layer '%s' in channel '%s' on '%s'!" % (layer_name, channel_name, geo_name))
        
        # determine the next publish version:
        publish_template = output["publish_template"]
        fields = {}
        
        # 1. Get fields from model publish path if possible
        geo_publish_path = None
        geo_version = geo.currentVersion()
        if geo_version.hasMetadata("tk_path"):
            geo_publish_path = geo_version.metadata("tk_path")
            
        if geo_publish_path:
            geo_publish_template = None
            try:
                geo_publish_template = self.parent.sgtk.template_from_path(geo_publish_path)
            except TankError:
                pass
            if geo_publish_template:
                fields = geo_publish_template.get_fields(geo_publish_path)
        
        # 2. Get context fields from current context
        ctx_fields = self.parent.context.as_template_fields(publish_template)
        fields.update(ctx_fields)
        
        # 3. Use the name from the model - this will be the name from the geo publish but
        # may also incorporate the mesh name if multiple objects were loaded from the same
        # publish
        fields["name"] = geo_name
        
        # 4. Add in channel and layer names:
        fields["channel"] = channel_name
        if layer:
            fields["layer"] = layer_name
        
        # 5. Find next version to use - note that version may be different across channels and/or layers
        found_versions = self.__find_matching_publish_versions(self.parent.context, publish_template, 
                                                               fields, ignore_keys = ["version", "UDIM"])
        
        next_publish_version = max([p["version"] for p in found_versions] or [0]) + 1
        fields["version"] = next_publish_version
        
        # use these fields to generate the publish path:
        publish_path = publish_template.apply_fields(fields)
        
        # and also generate the Mari output path:
        fields["UDIM"] = "$UDIM"
        fields["channel"] = "$CHANNEL"
        if layer:
            fields["layer"] = "$LAYER"
        output_path = publish_template.apply_fields(fields)
        
        # now publish the layer:
        if layer:
            layer.exportImages(output_path)
        else:
            flattened_layer = channel.flatten()
            flattened_layer.exportImages(output_path)

        # register the publish:
        progress_cb(75, "Registering the publish")        
        args = {
            "tk": self.parent.sgtk,
            "context": self.parent.context,
            "comment": comment,
            "path": publish_path,
            "name": geo_name,
            "version_number": fields["version"],
            "thumbnail_path": thumbnail_path,
            "task": sg_task,
            "published_file_type":output["tank_type"]
        }
        if geo_publish_path:
            args["dependency_paths"] = [geo_publish_path]
                    
        sgtk.util.register_publish(**args)

        
        
        
    def __find_matching_publish_versions(self, ctx, template, fields, ignore_keys = None):
        """
        """
        ignore_keys = ignore_keys or []
        
        if self.__cached_publishes == None:
            self.__cached_publishes = []
            
            # retrieve a list of all publishes for this context from Shotgun:
            pf_entity_type = sgtk.util.get_published_file_entity_type(self.parent.sgtk)
            filters = [["project", "is", ctx.project]]
            if ctx.entity:
                filters.append(["entity", "is", ctx.entity])
            if ctx.task:
                filters.append(["task", "is", ctx.task])
        
            sg_publishes = []
            try:
                sg_publishes = self.parent.shotgun.find(pf_entity_type, filters, fields=["path"])
            except Exception, e:
                raise TankError("Failed to find publishes for context %s: %s" % (ctx, e))
                
            # get the local paths for all publishes and add everything to the cache:
            publish_paths = self.get_publish_paths(sg_publishes)
            self.__cached_publishes = [{"publish":publish, "path":path} for publish, path in zip(sg_publishes, publish_paths)]
                
        fields = fields.copy()
        for ignore_key in ignore_keys:
            if ignore_key in fields:
                del(fields[ignore_key])
        
        found_versions = []
        for publish in self.__cached_publishes:
            path = publish["path"]
            
            # extract the fields for this path using the template:
            path_fields = template.validate_and_get_fields(path)
            if not path_fields:
                continue

            # check to see if the fields extracted from the path match the 
            # fields passed in, ignoring version:
            version = path_fields.get("version")

            for ignore_key in ignore_keys:
                if ignore_key in path_fields:
                    del(path_fields[ignore_key])


            if path_fields == fields:
                found_versions.append({"version":version, "path":path, "publish":publish["publish"]})

        return found_versions
                
            
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    
    
