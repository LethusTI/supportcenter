# -*- coding: utf-8 -*
from django.forms.forms import Form, BoundField
from django.forms.fields import Field
from django.forms.widgets import Widget
from django.forms.formsets import BaseFormSet, formset_factory
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from django.template import loader, Context
from django.conf import settings

class AutoBaseFormSet(BaseFormSet):
    def total_form_count(self):
        if self.initial_form_count() > 0:
            self.extra = 0
        
        return super(AutoBaseFormSet, self).total_form_count()

class FormsetWidget(Widget):
    field = None
    
    def value_from_datadict(self, data, files, name):
        return self.get_formset(data, prefix=name)
    
    def get_formset(self, *args, **kwargs):
        return self.field.formset_class(*args, **kwargs)

    def render(self, name, value, attrs=None):
        initial = value

        if value and isinstance(value, BaseFormSet):
            formset = value
        else:
            formset = self.get_formset(prefix=name, initial=value)

        t = loader.get_template(self.field.template_name)

        data = {'formset': formset,
                'class_name': self.field.class_name,
                'STATIC_URL': settings.STATIC_URL}

        return mark_safe(t.render(Context(data)))


class FormsetField(Field):
    widget = FormsetWidget
    formset_class = None
    class_name = "formset"
    template_name = 'lethusbox/formsetwidget.html'

    def __init__(self, form, formset=AutoBaseFormSet, extra=1,
                 max_num=None, class_name=None,
                 template_name=None,
                 validate=True, **kwargs):
        
        super(FormsetField, self).__init__(**kwargs)

        if class_name:
            self.class_name = class_name

        if template_name:
            self.template_name = template_name

        self.validate = validate
        self.set_formset(form, formset, extra, max_num=max_num)
        self.widget.field = self
        
    def set_formset(self, form, formset=AutoBaseFormSet, extra=1, max_num=None):
        self.formset_class = formset_factory(form, formset, extra, max_num=max_num)

    def save_fields(self, formset):
        return [i.save(commit=False) for i in formset.forms]

    def to_python(self, formset):
        if formset.forms and hasattr(formset.forms[0], "_meta"):
            return self.save_fields(formset)

        return formset.cleaned_data

    def clean(self, formset):
        if not self.validate:
            return formset

        if formset.is_valid():
            return self.to_python(formset)
        
        raise ValidationError("Formulário Inválido")
