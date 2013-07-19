# Copyright (c) 2013 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.


from tank.platform.qt import QtCore 

class ProgressReporter(QtCore.QObject):
    """
    Simple progress interface
    """
    progress = QtCore.Signal(float, object)
    
    def __init__(self, stage_count=1):
        """
        Construction
        """
        QtCore.QObject.__init__(self)

        self._stage_count = stage_count
        self._stages = []
        
        self._current_stage = None
        self._previous_percent = 0.0
        
    @property
    def stage_count(self):
        return self._stage_count   
    @stage_count.setter
    def stage_count(self, value):
        self._stage_count = max(1, value)

    def reset(self, new_stage_count=None):
        self._stages = []
        if new_stage_count != None:
            self._stage_count = max(1, new_stage_count)
        self._previous_percent = 0.0
        self._current_stage = None
        self.progress.emit(0.0, "")

    def report(self, percent, msg=None, stage=None):
        """
        Used to report progress.
        """
        if not stage:
            # progress is being reported for the previous stage:
            stage = self._current_stage
        else:
            # keep track of the stages that have been reported:
            found_stage = False
            for s in self._stages:
                if s == stage:
                    found_stage = True
                    break
            if not found_stage:
                self._stages.append(stage)
        
        # work out per-stage percentage based on the number of stages
        stage_num = len(self._stages)
        max_stage_count = max(self._stage_count, stage_num)
        
        # work out the current overall percentage.  This
        # will depend on the number of stages completed
        # so far
        current_percent = ((100.0 * (stage_num-1)) + percent)/max_stage_count
        
        # just in case, clamp to range:
        current_percent = min(max(current_percent, 0.0), 100.0)
       
        # don't want to allow progress to go backwards!
        if current_percent < self._previous_percent:
            current_percent = self._previous_percent
        
        # emit signal:
        try:
            self.progress.emit(current_percent, msg)
        finally:
            self._current_stage = stage
            self._previous_percent = current_percent
        
        #import time
        #time.sleep(1.0)
        
class TaskProgressReporter(ProgressReporter):
    def __init__(self, tasks):
        ProgressReporter.__init__(self, len(tasks))
        
        # build task index for tasks:
        self._task_index = {}
        for task in tasks:
            self._task_index[(task.item.name, task.output.name)] = task
        
    def report(self, percent, msg=None, stage=None):

        if not stage:
            # progress is being reported for the previous stage:
            stage = self._current_stage

        # if stage matches a task then we want to include
        # the task details at the start of the message:
        if msg != None:        
            try:
                item_name = stage["item"]["name"]
                output_name = stage["output"]["name"]
                
                # find task that matches:
                task = self._task_index.get((item_name, output_name))
                
                if task:
                    # update message to include task info:
                    msg = "%s - %s: %s" % (task.output.display_name, task.item.name, msg)
            except:
                pass
        
        # call base class:
        ProgressReporter.report(self, percent, msg, stage)
            
            
            
        
        
        