# -*- coding: utf-8 -*-
from django import template
register = template.Library()

def get_radio_item(d, idx):
    widget = d.field.widget
    
    attrs = {}
    if d.auto_id:
        attrs = {'id': d.auto_id}
    
    if isinstance(idx, basestring):
        pos = 0
        found = False

        for key, l in d.field.choices:
            if key == idx:
                found=True
                break

            pos += 1

        if found:
            idx = pos
        else:
            return ""
            

    return widget.get_renderer(d.html_name, d.value(), attrs, ())[idx]

register.filter('get_radio_item', get_radio_item)
