"""
Copyright (c) 2012 Shotgun Software, Inc
----------------------------------------------------
"""

from tank.platform.qt import QtCore 

class ProgressReporter(QtCore.QObject):
    """
    Simple progress interface
    """
    
    progress = QtCore.Signal(float, str)
    
    def __init__(self):
        """
        Construction
        """
        QtCore.QObject.__init__(self)
        

    
    def report(self, percent, msg=None):
        self.progress.emit(percent, msg)
        #print "(%d%%) - %s" % (percent, msg)