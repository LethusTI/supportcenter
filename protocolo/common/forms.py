# -*- coding: utf-8 -*-

__all__ = ('FilterForm',)

import datetime
from django import forms

class FilterForm(forms.Form):
    from_date = forms.DateField(label="De",
                                required=False,
                                initial=datetime.date.today,
                                widget=forms.TextInput(attrs={'size':'15'}))
    to_date = forms.DateField(label="Até",
                              required=False,
                              widget=forms.TextInput(attrs={'size':'15'}))
