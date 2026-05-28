#coding=UTF-8

from __future__ import unicode_literals, print_function, division

from django import forms

class TestForm(forms.Form):
    choices = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
    )
    text_input = forms.CharField()
    select = forms.ChoiceField(choices=choices)
    text_area = forms.CharField(widget=forms.Textarea)
    checkbox1 = forms.BooleanField()
    checkbox2 = forms.BooleanField()
    checkbox3 = forms.BooleanField()
    multiple_checkboxes = forms.ChoiceField(choices=choices, widget=forms.CheckboxSelectMultiple)
    radio_options = forms.ChoiceField(choices=choices, widget=forms.RadioSelect)
    date_time_input = forms.DateTimeField(widget=forms.SplitDateTimeWidget)
    date_input = forms.DateField()
    filefield = forms.FileField()
