# Copyright (c) 2013 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

import tank
from tank import Hook

class SuccessHook(Hook):
    """
    Hook that can be used to provide a custom successful completion message
    for publishing
    """
    def execute(self, **kwargs):
        """
        Main hook entry point
        :returns:       String
                        Hook should return the message
        """
        details = ("Your Publish has successfully completed. Your "
                "work has been shared, your scene has been "
                "versioned up and your mates have been notified!")

        return details


