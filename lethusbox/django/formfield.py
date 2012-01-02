# -*- coding: utf-8 -*
from django.forms.fields import Field
from django.forms.widgets import Widget
from django.utils.safestring import mark_safe
from django.template import loader, Context
from django.forms import ValidationError, BaseForm
from django.conf import settings

class FormWidget(Widget):
    field = None
    
    def value_from_datadict(self, data, files, name):
        return self.get_form(data=data, prefix=name)
    
    def get_form(self, *args, **kwargs):
        
        if self.field.form_kwargs:
            kwargs.update(self.field.form_kwargs)

        return self.field.form_class(*args, **kwargs)

    def render(self, name, value, attrs=None):
        
        # in invalid form
        if isinstance(value, BaseForm):
            form = value

        elif hasattr(value, '_meta'):
            form = self.get_form(prefix=name, instance=value)

        elif value is None:
            form = self.get_form(prefix=name)

        else:
            form = self.get_form(prefix=name, initial=value)

        t = loader.get_template(self.field.template_name)
        
        data = {'form': form,
                'class_name': self.field.class_name,
                'STATIC_URL': settings.STATIC_URL}
                
        return mark_safe(t.render(Context(data)))


class FormField(Field):
    widget = FormWidget
    form_class = None
    class_name = "formfield"
    template_name = 'lethusbox/formfieldwidget.html'

    def __init__(self, form, class_name=None,
                 template_name=None,
                 validate=True,
                 form_kwargs=None,
                 **kwargs):
        
        super(FormField, self).__init__(**kwargs)

        if class_name:
            self.class_name = class_name

        if template_name:
            self.template_name = template_name

        self.validate = validate
        self.form_class = form
        self.form_kwargs = form_kwargs
        self.widget.field = self
    
    def to_python(self, form):
        if hasattr(form, 'save'):
            return form.save(commit=False)
        return form.cleaned_data

    def clean(self, form):
        if not self.validate:
            return form

        if form.is_valid():
            return self.to_python(form)
        else:
            raise ValidationError('Formulário Inválido')
