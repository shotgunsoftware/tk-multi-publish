#!/usr/bin/env bash
# 
# Copyright (c) 2008 Shotgun Software, Inc
# ----------------------------------------------------

echo "building user interfaces..."
pyside-uic --from-imports publish_form.ui > ../python/tk_multi_publish/ui/publish_form.py
pyside-uic --from-imports publish_details_form.ui > ../python/tk_multi_publish/ui/publish_details_form.py
pyside-uic --from-imports publish_result_form.ui > ../python/tk_multi_publish/ui/publish_progress_form.py
pyside-uic --from-imports publish_result_form.ui > ../python/tk_multi_publish/ui/publish_result_form.py

pyside-uic --from-imports output_item.ui > ../python/tk_multi_publish/ui/output_item.py
pyside-uic --from-imports group_header.ui > ../python/tk_multi_publish/ui/group_header.py

pyside-uic --from-imports item_list.ui > ../python/tk_multi_publish/ui/item_list.py
pyside-uic --from-imports item.ui > ../python/tk_multi_publish/ui/item.py

pyside-uic --from-imports error_list.ui > ../python/tk_multi_publish/ui/error_list.py
pyside-uic --from-imports error_item.ui > ../python/tk_multi_publish/ui/error_item.py

echo "building resources..."
pyside-rcc resources.qrc > ../python/tk_multi_publish/ui/resources_rc.py
