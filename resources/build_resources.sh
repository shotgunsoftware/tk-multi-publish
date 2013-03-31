#!/usr/bin/env bash
# 
# Copyright (c) 2008 Shotgun Software, Inc
# ----------------------------------------------------

echo "building user interfaces..."
pyside-uic --from-imports publish_ui.ui > ../python/tk_multi_publish/ui/publish_ui.py

echo "building resources..."
pyside-rcc resources.qrc > ../python/tk_multi_publish/ui/resources_rc.py
