# -*- coding: utf-8 -*-

from django.forms.widgets import Widget, Select, CheckboxInput
from django.utils.encoding import StrAndUnicode, force_unicode
from django.utils.datastructures import MultiValueDict, MergeDict
from django.utils.html import escape, conditional_escape
from django.utils.safestring import mark_safe
from itertools import chain
from django.forms.util import flatatt
from constants import PERMISSIONS, PERMISSIONS_HEADERS, PERMISSIONS_NAMES
from itertools import cycle

class PermissionSelect(Widget):
    """
    Widget tabela de Permissões
    """
    def __init__(self, attrs=None, choices=()):
        super(PermissionSelect, self).__init__(attrs)
        # choices can be any iterable, but we may need to render this widget
        # multiple times. Thus, collapse it into a list so it can be consumed
        # more than once.
        self.choices = list(choices)

    def value_from_datadict(self, data, files, name):
        if isinstance(data, (MultiValueDict, MergeDict)):
            return data.getlist(name)
        return data.get(name, None)

    def _has_changed(self, initial, data):
        if initial is None:
            initial = []
        if data is None:
            data = []
        if len(initial) != len(data):
            return True
        initial_set = set([force_unicode(value) for value in initial])
        data_set = set([force_unicode(value) for value in data])
        return data_set != initial_set

    def get_permissions(self):
        """
        Retorna a Lista de Permissoes Disponiveis
        """
        return PERMISSIONS.items()

    def render(self, name, value, attrs=None, choices=()):
        """
        Renderiza o Widget
        retorna o codigo html da selecao
        """

        if value is None: value = []
        final_attrs = self.build_attrs(attrs, name=name)
        # Normalize to strings
        str_values = set([force_unicode(v) for v in value])

        output = [u'<h4 class="cleantitle">Personalizando permissões</h4><table class="table table-bordered">',]
        headers = [u'<th>Módulo</th>']

        for header in PERMISSIONS_HEADERS:
            headers.append(u'<td class="final">%s</td>' % header)

        output.append(u'<thead><tr>%s</tr></thead>' % u'\n'.join(headers))
        classes = cycle(['lr', 'lt'])

        for label, perms in self.get_permissions():
            row = [u'<td>%s</td>' % label]
            mod = perms[0].split('.', 2)[0]

            for p in PERMISSIONS_NAMES:
                perm = '%s.%s' % (mod, p)

                if perm in perms:
                    final_attrs = dict(final_attrs, id='%s_%s' % (attrs['id'], perm))
                    cb = CheckboxInput(final_attrs, check_test=lambda value: value in str_values)
                    row.append(u'<td class="choice">%s</td>' % cb.render(name, perm))
                else:
                    row.append(u'<td> </td>')

            output.append(u'<tr class="{0}">{1}</tr>'.format(classes.next(),
                                                             u'\n'.join(row)))

        output.append(u'</table>')

        return mark_safe(u'\n'.join(output))

    def id_for_label(self, id_):
        # See the comment for RadioSelect.id_for_label()
        if id_:
            id_ += '_0'
        return id_
    id_for_label = classmethod(id_for_label)
    
    def render_option(self, selected_choices, option_value, option_label):
        option_value = force_unicode(option_value)
        selected_html = (option_value in selected_choices) and u' selected="selected"' or ''
        return u'<option value="%s"%s>%s</option>' % (
            escape(option_value), selected_html,
            conditional_escape(force_unicode(option_label)))

    def render_options(self, choices, selected_choices):
        # Normalize to strings.
        selected_choices = set([force_unicode(v) for v in selected_choices])
        output = []
        for option_value, option_label in chain(self.choices, choices):
            if isinstance(option_label, (list, tuple)):
                output.append(u'<optgroup label="%s">' % escape(force_unicode(option_value)))
                for option in option_label:
                    output.append(self.render_option(selected_choices, *option))
                output.append(u'</optgroup>')
            else:
                output.append(self.render_option(selected_choices, option_value, option_label))
        return u'\n'.join(output)

class ActionSelect(Select):
    """
    Widget especial para renderizar widget de ações
    """

    def __init__(self, filter_module, filter_action, *args, **kwargs):
        super(ActionSelect, self).__init__(*args, **kwargs)

        self.filter_module = filter_module
        self.filter_action = filter_action

    def render(self, name, value, attrs=None, choices=()):
        """
        Renderiza o Widget
        retorna o codigo html da selecao
        """
        final_attrs = self.build_attrs(attrs, name=name)
        output = [u'<select%s>' % flatatt(final_attrs)]

        output.append(u'</select>')
        return mark_safe(u'\n'.join(output))
