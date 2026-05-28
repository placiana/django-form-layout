#coding=UTF-8

from __future__ import unicode_literals, print_function, division

from django.test import TestCase
from unittest import expectedFailure
from form_layout.tests.forms import TestForm
from form_layout.forms import Field, Holder, Label, ButtonHolder, Button, SubmitButton


class FieldTests(TestCase):
    def test_invalid_content(self):
        self.assertRaises(AttributeError, Field, 666)

    def test_render(self):
        form = TestForm()
        field = Field('text_input', width=66)
        self.assertEqual(field.render(form), 'START_HOLDER 66 TextInput text_input END_HOLDER ')


class HolderTests(TestCase):
    def test_init(self):
        holder = Holder(('text_input', Field('select'), Holder('checkbox1')))
        self.assertEqual(len(holder.content), 3)
        self.assertEqual(holder.content[2].content[0].__class__, Field)

    def test_render(self):
        holder = Holder( ('text_input', Holder('checkbox1', width=50), Field('select')) )
        self.assertEqual(holder.render(TestForm()), 'START_HOLDER 100 START_HOLDER 100 TextInput text_input END_HOLDER START_HOLDER 50 START_HOLDER 100 CheckboxInput checkbox1 END_HOLDER END_HOLDER START_HOLDER 100 Select select END_HOLDER END_HOLDER ')

    def test_children_width(self):
        holder1 = Holder( ( 'checkbox1', 'checkbox2', 'checkbox3' ), children_width=10 )
        holder2 = Holder( ( 'checkbox1', 'checkbox2', 'checkbox3' ), children_width=[20,40,40] )
        self.assertEqual(holder1.render(TestForm()), 'START_HOLDER 100 START_HOLDER 10 CheckboxInput checkbox1 END_HOLDER START_HOLDER 10 CheckboxInput checkbox2 END_HOLDER START_HOLDER 10 CheckboxInput checkbox3 END_HOLDER END_HOLDER ')
        self.assertEqual(holder2.render(TestForm()), 'START_HOLDER 100 START_HOLDER 20 CheckboxInput checkbox1 END_HOLDER START_HOLDER 40 CheckboxInput checkbox2 END_HOLDER START_HOLDER 40 CheckboxInput checkbox3 END_HOLDER END_HOLDER ')

    @expectedFailure
    def test_children_width_percentage(self):
        holder = Holder( ( 'checkbox1', 'checkbox2', 'checkbox3' ), children_width='%' )
        output = holder.render(TestForm())
        self.assertEqual(output2, 'START_HOLDER 100 START_HOLDER 33 CheckboxInput checkbox1 END_HOLDER START_HOLDER 33 CheckboxInput checkbox2 END_HOLDER START_HOLDER 34 CheckboxInput checkbox3 END_HOLDER END_HOLDER ')


class LabelTests(TestCase):
    def test_render(self):
        label = Label('Hola!')
        self.assertEquals(label.render(None), 'START_HOLDER 100 Hola! END_HOLDER ')
        #                              ^ Form not needed to render a Label


class ButtonTests(TestCase):
    def test_buttons(self):
        button = Button('Click Me')
        self.assertEqual(button.render(), 'button Click Me ')
        submit_button = SubmitButton('Click Me Again')
        self.assertEqual(submit_button.render(), 'submit Click Me Again ')

    def test_button_holder(self):
        button_holder1 = ButtonHolder(SubmitButton('Submit'), width=50)
        button_holder2 = ButtonHolder((SubmitButton('Submit'), Button('OtherAction')))
        self.assertEqual(button_holder1.render(None), 'START_HOLDER 50 submit Submit END_HOLDER ')
        self.assertEqual(button_holder2.render(None), 'START_HOLDER 100 submit Submit button OtherAction END_HOLDER ')

    def test_autocreate_button_holder(self):
        holder = Holder(SubmitButton('Hola'))
        self.assertEqual(holder.content[0].__class__, ButtonHolder)
