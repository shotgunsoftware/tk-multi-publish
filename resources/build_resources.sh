#!/usr/bin/env bash
# 
# Copyright (c) 2008 Shotgun Software, Inc
# ----------------------------------------------------

echo "building user interfaces..."
pyside-uic --from-imports publish_ui.ui > ../python/tk_multi_publish/ui/publish_ui.py
#pyside-uic --from-imports progress.ui > ../python/tk_nuke_publish/ui/progress.py
#pyside-uic --from-imports snapshot_history.ui > ../python/tk_nuke_publish/ui/snapshot_history.py

echo "building resources..."
#pyside-rcc resources.qrc > ../python/tk_nuke_publish/ui/resources_rc.py
