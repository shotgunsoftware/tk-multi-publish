"""
Copyright (c) 2012 Shotgun Software, Inc
----------------------------------------------------
"""
import tank
import os
import sys
import threading

from PySide import QtCore, QtGui

browser_widget = tank.platform.import_framework("tk-framework-widget", "browser_widget")

class TaskBrowserWidget(browser_widget.BrowserWidget):
    
    def __init__(self, parent=None):
        browser_widget.BrowserWidget.__init__(self, parent)
        
        # only load this once!
        self._current_user = None
        self._current_user_loaded = False

    def get_data(self, data):
        pass
        """
        if not self._current_user_loaded:
            self._current_user = tank.util.get_shotgun_user(self._app.shotgun)
            self._current_user_loaded = True
        
        
        # start building output data structure        
        output = {}

        fields = ["content", "task_assignees", "image", "sg_status_list", "step"]

        if data["own_tasks_only"]:
            
            if self._current_user is None:
                output["tasks"] = []
                output["users"] = []
                
            else:
                # get my stuff
                output["users"] = [ self._current_user ]
                output["tasks"] = self._app.shotgun.find("Task", 
                                                    [ ["project", "is", self._app.context.project],
                                                      ["entity", "is", self._app.context.entity], 
                                                      ["task_assignees", "is", self._current_user ]], 
                                                    fields)
                         
        else:
            # get all tasks
            output["tasks"] = self._app.shotgun.find("Task", 
                                                [ ["project", "is", self._app.context.project],
                                                  ["entity", "is", self._app.context.entity ] ], 
                                                fields)
        
            # get all the users where tasks are assigned.
            user_ids = []
            for task in output["tasks"]:
                user_ids.extend( [ x["id"] for x in task.get("task_assignees", []) ] )
            
            if len(user_ids) > 0:
                # use super weird filter syntax....
                sg_filter = ["id", "in"]
                sg_filter.extend(user_ids)
                output["users"] = self._app.shotgun.find("HumanUser", [ sg_filter ], ["image"])
            else:
                output["users"] = []
        
        return output
        """
                 
    def process_result(self, result):
        pass
        """
        tasks = result["tasks"]

        if len(tasks) == 0:
            self.set_message("No Tasks found!")
            return

        # try to be smart about selecting the right task for the user.
        task_id_to_look_for = None
        step_to_look_for = None
        if self._app.context.task:
            # we got a task
            task_id_to_look_for = self._app.context.task.get("id")
        elif self._app.context.step: 
            step_to_look_for = self._app.context.step.get("id")
            
        for d in tasks:
            i = self.add_item(browser_widget.ListItem)
            
            details = []
            details.append("<b>Task: %s</b>" % d.get("content", ""))
            
            details.append("Status: %s" % d.get("sg_status_list"))
            
            names = [ x.get("name", "Unknown") for x in d.get("task_assignees", []) ]
            names_str = ", ".join(names)
            details.append("Assigned to: %s" % names_str)
            
            i.set_details("<br>".join(details))
            
            i.sg_data = d
            
            # finally look up the thumbnail for the first user assigned to the task
            task_assignees = d.get("task_assignees", [])
            if len(task_assignees) > 0:
                user_id = task_assignees[0]["id"]
                # is this user id in our users dict? In that case we have their thumb!
                for u in result["users"]:
                    if u["id"] == user_id:
                        # if they have a thumb, assign!
                        if u.get("image"):
                            i.set_thumbnail(u.get("image"))
                        break            
    
            # finally figure out if this should be selected
            if d["id"] == task_id_to_look_for:
                # exact match! 
                self.select(i)
            elif d.get("step") and d.get("step").get("id") == step_to_look_for:
                # found a matching step. Good enough
                self.select(i)
        """