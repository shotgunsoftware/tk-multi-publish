#!/usr/bin/env bash
# 
# Copyright (c) 2008 Shotgun Software, Inc
# ----------------------------------------------------

echo "building user interfaces..."
pyside-uic --from-imports publish_ui.ui > ../python/tk_multi_publish/ui/publish_ui.py
pyside-uic --from-imports publish_details_ui.ui > ../python/tk_multi_publish/ui/publish_details_ui.py
pyside-uic --from-imports publish_result_ui.ui > ../python/tk_multi_publish/ui/publish_result_ui.py

pyside-uic --from-imports output_item_ui.ui > ../python/tk_multi_publish/ui/output_item_ui.py
pyside-uic --from-imports group_header_ui.ui > ../python/tk_multi_publish/ui/group_header_ui.py

pyside-uic --from-imports item_list_ui.ui > ../python/tk_multi_publish/ui/item_list_ui.py
pyside-uic --from-imports item_ui.ui > ../python/tk_multi_publish/ui/item_ui.py

pyside-uic --from-imports error_list_ui.ui > ../python/tk_multi_publish/ui/error_list_ui.py
pyside-uic --from-imports error_item_ui.ui > ../python/tk_multi_publish/ui/error_item_ui.py

echo "building resources..."
pyside-rcc resources.qrc > ../python/tk_multi_publish/ui/resources_rc.py
