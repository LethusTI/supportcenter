# -*- coding: utf-8 -*
from django.conf import settings
__all__ = ('MenuManager',)

MENUS_BY_ID = {}
MENUS_BY_CAT = {}

class Filter(object):
    def __init__(self, options):
        self.perm = options.get('perm', None)
        self.is_admin = options.get('is_admin', False)
        self.unid_tipo = options.get('unid_tipo', None)
        self.cargo_tipo = options.get('cargo_tipo', None)

    def allow(self, user):
        if self.is_admin and not getattr(user, 'is_superuser', False):
            return False

        if self.perm and not user.has_perm(self.perm):
            return False

        return True

class Button(object):
    def __init__(self, label, options={}, base_uri=None):
        uri = options.get('uri')

        if base_uri and uri:
            uri = '%s%s' % (base_uri, uri)

        if uri:
            item = u"<a href=\"%s\">%s</a>" % (uri, label)
        else:
            item = label
        
        self.item = u"<li>%s</li>" % item
        self.filter = Filter(options)
        self.enabled = True

    def render(self, user):
        if not self.filter.allow(user):
            return

        return self.item

class Menu(object):
    def __init__(self, label, options={}, itens=[]):
        self.options = options
        self.items = []
        self.enabled = True

        button_kwargs = {}
        base_uri = options.get('base_uri', None)

        if base_uri:
            button_kwargs['base_uri'] = base_uri

        for node in itens:
            if len(node) == 3:
                item = Menu(node[0], node[1], node[2])
            elif len(node) == 2:
                item = Button(node[0], node[1], **button_kwargs)
            
            if item.enabled:
                self.items.append(item)

        uri = options.get('uri')
        _id = options.get('id', None)
        category = options.get('category', None)

        self.item = u"<a tabindex=\"-1\" href=\"#\">%s</a>" % label
 
        
        self.filter = Filter(options)

        if _id:
            MENUS_BY_ID[_id] = self
        if category:
            if not MENUS_BY_CAT.has_key(category):
                MENUS_BY_CAT[category] = []

            MENUS_BY_CAT[category].append(self)

    def render(self, user, onlycontent=False):
        if not self.filter.allow(user):
            return

        data = []
        for item in self.items:
            html = item.render(user)

            if html:
                data.append(html)

        if not data:
            return

        if onlycontent:
            return ''.join(data)

        menu = '<ul class="dropdown-menu">%s</ul>' % ''.join(data)

        return (
            u"<li class=\"dropdown-submenu\">%s%s</li>" % (
                self.item, menu))

    def allow(self, user):
        if not self.filter.allow(user):
            return False

        for item in self.items:
            if item.filter.allow(user):
                return True

        return False

class MenuManager(object):
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(MenuManager, cls).__new__(
                cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        data = settings.LETHUS_MENU
        self.items = []

        for node in data:
            if len(node) == 3:
                item = Menu(node[0], node[1], node[2])
            elif len(node) == 2:
                item = Button(node[0], node[1])
            
            if item.enabled:
                self.items.append(item)

    def allow_category(self, user, category):
        for menu in MENUS_BY_CAT.get(category, []):
            if menu.allow(user):
                return True

        return False

    def render(self, user, submenu=None, onlycontent=False):

        if submenu:
            menu = MENUS_BY_ID.get(submenu)
            
            if menu:
                html = menu.render(user, onlycontent=onlycontent)
                return html or ''

        data = []
        for item in self.items:
            html = item.render(user)
            if html:
                data.append(html)

        return u''.join(data)
