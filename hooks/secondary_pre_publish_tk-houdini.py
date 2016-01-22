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

from tank import Hook

class PrePublishHook(Hook):
    """
    Single hook that implements pre-publish functionality
    """
    def execute(self, tasks, work_template, progress_cb, user_data, **kwargs):
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
        :param user_data:       A dictionary containing any data shared by other hooks run prior to
                                this hook. Additional data may be added to this dictionary that will
                                then be accessible from user_data in any hooks run after this one.
                        
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

            # pre-publish alembic_cache output
            if output["name"] == "alembic_cache":
                errors.extend(self.__validate_item_for_alembic_cache_publish(item))
            elif output["name"] == "rendered_image":
                errors.extend(self.__validate_item_for_rendered_image_publish(item))
            else:
                # don't know how to publish this output types!
                errors.append("Don't know how to publish this item!")

            # if there is anything to report then add to result
            if len(errors) > 0:
                # add result:
                results.append({"task": task, "errors": errors})

            progress_cb(100)

        return results

    def __validate_item_for_alembic_cache_publish(self, item):
        """
        Validate that the item is valid to be exported to an alembic cache.
        
        :param item:    The item to validate
        :returns:       A list of any errors found during validation that should be reported
                        to the artist
        """
    
        # validate the exported alembic cache and add any errors found here
        errors = []

        node = item["other_params"]["node"]
        path = item["other_params"]["path"]
        if not os.path.exists(path):
            errors.append(
                "No alembic cache has been written to disk for this node.")
        
        # finally return any errors
        return errors    
    
    def __validate_item_for_rendered_image_publish(self, item):
        """
        Validate that the item is valid to be exported as rendered images.
        
        :param item:    The item to validate
        :returns:       A list of any errors found during validation that should be reported
                        to the artist
        """
    
        # validate the exported rendered images and add any errors found here
        errors = []
        
        node = item["other_params"]["node"]
        paths = item["other_params"]["paths"]
        if not paths:
            errors.append(
                "No rendered images found for node '%s'." % (node.path(),)
            )   
        elif len(paths) > 1:
            errors.append(
                "Found multiple potential rendered image paths for node '%s'." 
                "Skipping these paths:\n  '%s'" %
                (node.path(), "\n  ".join(paths))
            )

        # finally return any errors
        return errors    

