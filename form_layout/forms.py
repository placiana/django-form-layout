#coding=UTF-8

from __future__ import unicode_literals, print_function, division

import six

from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.forms.utils import flatatt


def is_text(obj):
    # Checking if obj is a string, compatible with python 2 and 3
    return isinstance(obj, six.string_types)


class BaseHolder(object):
    default_options = {
        'width': 100,
    }

    def __init__(self, *args, **kwargs):
        self.options = self.default_options.copy()
        self.holder_template = kwargs.pop('holder_template',
                                     'form_layout/holder.html')
        self.options.update(kwargs)

    def render(self, form, **kwargs):
        options = self.options
        options.update(kwargs)
        content = mark_safe(self.get_content(form, **options))
        return mark_safe(render_to_string(self.holder_template,
                dict(content=content, **options)))

    def get_content(self, form, **kwargs):
        raise NotImplementedError

class Holder(BaseHolder):
    def __init__(self, content, **kwargs):
        super(Holder, self).__init__(**kwargs)
        # Prepare content for processing
        if not hasattr(content, '__iter__') or is_text(content):
            content = (content, )

        self.content = []
        for element in content:
            if is_text(element):
                self.content.append(Field(element))
            elif isinstance(element, BaseHolder):
                self.content.append(element)
            elif isinstance(element, Button):
                self.content.append(ButtonHolder(element))
            else:
                raise AttributeError('Invalid content, recieved: %s' % element)

    def get_content(self, form, **kwargs):
        # TODO: check if kwargs are passed by reference or by value
        options = kwargs
        children_width_list = None
        if 'children_width' in options:
            children_width = options['children_width']
            if isinstance(children_width, int):
                options['width'] = children_width
            elif children_width == '%':
                options['width'] = 100 / len(self.content)
                # TODO: treat this as a list and distribute the module to the
                # last ones
            else:
                children_width_list = children_width
                del options['width']

            del options['children_width']
        else:
            del options['width']

        output = ''
        for element in self.content:
            if children_width_list:
                options['width'] = children_width_list.pop(0)
            output += element.render(form, **options)
        return output


class Field(BaseHolder):
    def __init__(self, field, **kwargs):
        super(Field, self).__init__(**kwargs)
        if not is_text(field):
            raise AttributeError('Invalid field.')
        self.field = field

    def get_content(self, form, **kwargs):
        form_field = form[self.field]
        attrs_rep = ''
        class_rep = ''
        if form_field.field.widget.attrs:
            class_rep = form_field.field.widget.attrs.pop('class', '')
            attrs_rep = flatatt(form_field.field.widget.attrs)

        widget_name = form[self.field].field.widget.__class__.__name__
        if hasattr(form[self.field].field.widget, 'widget_name'):
            widget_name = form[self.field].field.widget.widget_name

        return render_to_string('form_layout/widget.html', dict(
                field=form[self.field],
                attrs=attrs_rep,
                class_attr=class_rep,
                widget_name=widget_name,
                **kwargs))


class Label(BaseHolder):
    def __init__(self, label, **kwargs):
        super(Label, self).__init__(**kwargs)
        if not is_text(label):
            raise AttributeError('Invalid content.')
        self.label = label

    def get_content(self, form, **kwargs):
        return render_to_string('form_layout/label.html', dict(
                label=self.label, **kwargs))


class ButtonHolder(BaseHolder):
    def __init__(self, content, **kwargs):
        super(ButtonHolder, self).__init__(**kwargs)
        # Prepare content for processing
        if not hasattr(content, '__iter__'):
            content = (content, )

        self.content = []
        for element in content:
            if not isinstance(element, Button):
                raise AttributeError('Invalid content, recieved: %s' % element)
            self.content.append(element)

    def get_content(self, *args, **kwargs):
        output = ''
        for element in self.content:
            output += element.render(**kwargs)
        return output


class Button(object):
    type = 'button'

    def __init__(self, value, **kwargs):
        self.value = value
        self.options = kwargs

    def render(self, *args, **kwargs):
        options = self.options
        options.update(kwargs)
        return render_to_string('form_layout/button.html',
                dict(value=self.value, type=self.type, **options))

class SubmitButton(Button):
    type = 'submit'

class FormAttr(BaseHolder):
    def __init__(self, attr, label=None, **kwargs):
        super(FormAttr, self).__init__(**kwargs)
        if not is_text(attr):
            raise AttributeError('Invalid FormAttr.')
        self.attr = attr
        self.label = label

    def get_content(self, form, **kwargs):
        value = getattr(form, self.attr, None)
        return render_to_string('form_layout/form_attr.html', dict(
                value=value,
                label=self.label,
                **kwargs))
