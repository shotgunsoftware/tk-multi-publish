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
import mari

import tank
from tank import Hook
from tank import TankError

class PrePublishHook(Hook):
    """
    Single hook that implements pre-publish functionality
    """
    def execute(self, tasks, work_template, progress_cb, **kwargs):
        """
        Main hook entry point
        :param tasks:           List of tasks to be pre-published.  Each task is be a 
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
                        
        :param work_template:   template
                                This is the template defined in the config that
                                represents the current work file
               
        :param progress_cb:     Function
                                A progress callback to log progress during pre-publish.  Call:
                                
                                    progress_cb(percentage, msg)
                                     
                                to report progress to the UI
                        
        :returns:               A list of any tasks that were found which have problems that
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
        for task in tasks:
            item = task["item"]
            output = task["output"]
            errors = []
        
            # report progress:
            progress_cb(0, "Validating", task)
        
            if output["name"] in ["channel", "layer"]:
                # validate mari texture publish:
                validation_errors = self._validate_texture_publish(item, output)
                if validation_errors: 
                    errors.extend(validation_errors)
            else:        
                # don't know how to publish this output types!
                errors.append("Don't know how to publish this item!")            

            # if there is anything to report then add to result
            if len(errors) > 0:
                # add result:
                results.append({"task":task, "errors":errors})
                
            progress_cb(100)
            
        return results
    
    def _validate_texture_publish(self, item, output):
        """
        Validate the specified texture publish
        
        :param item:            The item to publish
        :param output:          The output definition for the item
        """
        # extract the geo, channel & layer from the other params - these
        # were determined in the scan scene hook.
        params = item.get("other_params")
        geo_name = params["geo"]
        channel_name = params["channel"]
        layer_name = params.get("layer")        

        errors = []

        # check that the geo, channel & layer are still valid:
        geo = mari.geo.find(geo_name)
        if not geo:
            errors.append("Failed to find geometry in the project!")
            return errors
        
        channel = geo.findChannel(channel_name)
        if not channel:
            errors.append("Failed to find channel on geometry!")
            return errors
        
        if layer_name:
            layer = channel.findLayer(layer_name)
            if not layer:
                errors.append("Failed to find layer for channel!")
                return errors

        return errors
        
        
        
    
    