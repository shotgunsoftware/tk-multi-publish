"""
Copyright (c) 2012 Shotgun Software, Inc
----------------------------------------------------
"""

import tank

class PublishOutput(object):
    """
    Encapsulate an output definition as 
    loaded from the configuration
    """
    
    def __init__(self, app, fields={}, name=None, selected=None, required=None, display_group=None):
        """
        Construction
        """
        self._raw_fields = fields

        # have to resolve publish template to an actual template:
        self._publish_template = app.get_template_by_name(self._raw_fields["publish_template"])
        
        # special case handling of some fields that can be provided either
        # as args or through the fields
        self._name = [name, fields.get("name", "")][name == None]
        self._required = [required, fields.get("required", False)][required == None]
        self._selected = self._required or [selected, fields.get("selected", True)][selected == None]
        self._display_group = [display_group, fields.get("display_group", "")][display_group == None]
    
    @property
    def name(self):
        return self._name    

    @property
    def scene_item_type(self):
        return self._raw_fields["scene_item_type"]
    
    @property
    def display_name(self):
        return self._raw_fields["display_name"]
    
    @property
    def display_group(self):
        return self._display_group
    
    @property
    def description(self):
        return self._raw_fields["description"]
    
    @property
    def icon_path(self):
        return self._raw_fields["icon"]
    
    @property
    def tank_type(self):
        return self._raw_fields["tank_type"]
    
    @property
    def publish_template(self):
        return self._publish_template
        
    @property
    def selected(self):
        return self._selected
    
    @property
    def required(self):
        return self._required
    
    