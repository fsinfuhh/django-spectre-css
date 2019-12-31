from typing import List, Tuple, Optional, Union

from django.forms import Form
from django.forms.boundfield import BoundField
from django.forms.models import ModelChoiceIterator
from django.forms.widgets import Select, CheckboxInput
from django.template import Library

register = Library()


@register.filter
def is_checkbox(field):
    return isinstance(field.field.widget, CheckboxInput)


@register.filter
def is_select(field):
    return isinstance(field.field.widget, Select)


@register.inclusion_tag('spectre-css/generic-field.html')
def render_form_field(field: BoundField, *args, **kwargs):
    return {
        'field': field,
        'switch': kwargs.get('switch', False),
        'add_choices': kwargs.get('add_choices', None),
        'replace_choices': kwargs.get('replace_choices', None),
        'empty_option': kwargs.get('empty_option', None),
        'value': kwargs.get('value', None),
        # TODO: radio values?
    }


@register.inclusion_tag('spectre-css/render-form-field.html')
def render_form_field_default(field: BoundField, value: Union[str, int, None] = None):
    if value:
        field.initial = value
    return {
        'field': field,
        'field_class': 'form-input',
    }


@register.inclusion_tag('spectre-css/render-form-checkbox.html')
def render_form_checkbox(field: BoundField, switch: bool = False):
    return {'field': field, 'switch': switch}


choice_list_type = Optional[List[Tuple[Union[str, int, None], str]]]


@register.inclusion_tag('spectre-css/render-form-field.html')
def render_form_select(field: BoundField, add_choices: choice_list_type = None, replace_choices: choice_list_type = None, empty_option: str = None):
    if replace_choices:
        field.field.widget.choices = replace_choices
    if (add_choices or empty_option) and isinstance(field.field.widget.choices, ModelChoiceIterator):
        # the repacking into an list is necessary because the ModelChoiceIterator does not support inserting
        field.field.widget.choices = [x for x in field.field.widget.choices]
    if add_choices:
        field.field.widget.choices.extend(add_choices)
    if empty_option:
        field.field.widget.choices.insert(0, (None, empty_option))
    return {
        'field': field,
        'field_class': 'form-select',
    }


@register.inclusion_tag('spectre-css/render-form-radio.html')
def render_form_radio(field: BoundField):
    return {'field': field}


@register.inclusion_tag('spectre-css/form.html')
def render_form(form: Form):
    return {'form': form}
