"""
Copyright (c) 2012 Shotgun Software, Inc
----------------------------------------------------
"""
from tank.platform.qt import QtCore

class Task(QtCore.QObject):
    """
    Encapsulates a task for use internally within 
    the app - this is converted and passed as a
    dictionary to any hooks.
    """
    modified = QtCore.Signal()
    
    def __init__(self, item, output):
        QtCore.QObject.__init__(self)
        self._item = item
        self._output = output
        self._pre_publish_errors = []
        self._publish_errors = []
        
    @property
    def item(self):
        return self._item
    
    @property
    def output(self):
        return self._output
    
    @property
    def pre_publish_errors(self):
        return self._pre_publish_errors
    @pre_publish_errors.setter
    def pre_publish_errors(self, value):
        self._pre_publish_errors = value
        # emit modified signal
        self.modified.emit()
        
    @property
    def publish_errors(self):
        return self._publish_errors
    @publish_errors.setter
    def publish_errors(self, value):
        self._publish_errors = value
        # emit modified signal
        self.modified.emit()
    
    
    def as_dictionary(self):
        """
        Return the task as a dictionary ready for passing 
        to the pre-publish and publish hooks
        """
        return {"item":self._item.raw_fields,
                "output":{"name":self._output.name, 
                          "publish_template":self._output.publish_template,
                          "tank_type":self._output.tank_type,
                          }
                }