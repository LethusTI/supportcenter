# -*- coding: utf-8 -*-
from django import template
register = template.Library()

from lethusbox.bootstrapmenu import MenuManager
from django.utils.safestring import mark_safe

class MenuCategoryNode(template.Node):
    def __init__(self, nodelist, category):
        self.nodelist = nodelist
        self.category = category
        self.menu_manager = MenuManager()

    def render(self, context, forced=False):
        
        if self.menu_manager.allow_category(
            context['user'], self.category):
            return self.nodelist.render(context)
        
        return u''

class MenuNode(template.Node):
    def __init__(self, name, onlycontent=False):
        self.name = name
        self.menu_manager = MenuManager()
        self.onlycontent = onlycontent
        
    def render(self, context, forced=False):
        return self.menu_manager.render(
            context['user'], submenu=self.name,
            onlycontent=self.onlycontent)

@register.tag
def menu(parser, token):
    args = token.split_contents()
    return MenuNode(args[1])

@register.tag
def menucontent(parser, token):
    args = token.split_contents()
    return MenuNode(args[1], onlycontent=True)

@register.tag
def menucategory(parser, token):
    nodelist = parser.parse(('endmenucategory',))
    parser.delete_first_token()

    args = token.split_contents()
    return MenuCategoryNode(nodelist, args[1])
