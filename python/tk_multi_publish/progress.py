"""
Copyright (c) 2012 Shotgun Software, Inc
----------------------------------------------------
"""

class ProgressReporter(object):
    """
    Simple progress interface
    """
    def __init__(self):
        """
        Construction
        """
        pass
    
    def report(self, percent, msg):
        print "(%d%%) - %s" % (percent, msg)