"""
Copyright (c) 2013 Shotgun Software, Inc
----------------------------------------------------
"""
import tank
import os
import sys
import datetime
import threading 

from PySide import QtCore, QtGui

browser_widget = tank.platform.import_framework("tk-framework-widget", "browser_widget")

"""
from .custom_list_items import TickListItem
from .custom_list_items import NukeScriptItem
from .custom_list_items import DisabledItem
"""

class ItemBrowserWidget(browser_widget.BrowserWidget):
    
    def __init__(self, parent=None):
        browser_widget.BrowserWidget.__init__(self, parent)

    def get_data(self, data):
        return None

    def process_result(self, result):
        pass