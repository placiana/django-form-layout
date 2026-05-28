#coding=UTF-8

from __future__ import unicode_literals, print_function, division

from django import template
from importlib import import_module

register = template.Library()


@register.tag(name="render_layout")
def parse_render_layout(parser, token):
    try:
        _, app_name, keys, form = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires three arguments" % token.contents.split()[0])
    return RenderLayoutNode(app_name, keys, form)


class RenderLayoutNode(template.Node):
    def __init__(self, app_name, keys, form):
        self.app_name = template.Variable(app_name)
        self.keys = template.Variable(keys)
        self.form = template.Variable(form)

    def render(self, context):
        app_name = self.app_name.resolve(context)
        app_layouts = import_module(app_name + '.' + 'layout').layouts
        keys = self.keys.resolve(context)
        layout = self.get_layout(app_layouts, keys)

        form = self.form.resolve(context)
        out = layout.render(form)
        for field in form.fields:
            if form[field].is_hidden:
                out += str(form[field])
        return out

    def get_layout(self, layouts, keys):
        keys = keys.split('.')
        value = layouts
        for key in keys:
            value = value[key]

        return value

@register.filter
def widget_name(field):
    if hasattr(field.field.widget, 'widget_name'):
        return field.field.widget.widget_name
    return field.field.widget.__class__.__name__


@register.simple_tag
def show_splitdatetime(field, widget_idx):
    value = field.value()
    name = field.name
    multiple_widget = field.field.widget
    rendered_widget = multiple_widget.widgets[widget_idx]

    if multiple_widget.is_localized:
        multiple_widget.widgets[widget_idx].is_localized = multiple_widget.is_localized
    # value is a list of values, each corresponding to a widget
    # in self.widgets.
    if not isinstance(value, list):
        value = multiple_widget.decompress(value)

    try:
        widget_value = value[widget_idx] or ''
    except IndexError:
        widget_value = ''
    return rendered_widget.format_value(widget_value)

