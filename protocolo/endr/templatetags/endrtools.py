# -*- coding: utf-8 -*-
from django import template
from django.template.loader import render_to_string

register = template.Library()
from saude.endr.forms import EndrSelectForm

@register.simple_tag
def endr_select_form():
    return render_to_string('endr/form.html', {
            "form": EndrSelectForm()
            })
