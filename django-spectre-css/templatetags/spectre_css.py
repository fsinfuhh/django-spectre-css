from typing import List, Tuple, Optional, Union

from django.forms import Form, MultiValueField
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


@register.filter
def is_multi_field(field: BoundField):
    return isinstance(field.field, MultiValueField)


field_value = Union[str, int, None]
choice_list_type = Optional[List[Tuple[field_value, str]]]


@register.inclusion_tag('spectre-css/generic-field.html')
def render_form_field(field: BoundField, switch: bool = False, add_choices: choice_list_type = None,
                      replace_choices: choice_list_type = None, empty_option: Optional[str] = None,
                      value: field_value = None):
    if value:
        field.initial = value
    return {
        'field': field,
        'switch': switch,
        'add_choices': add_choices,
        'replace_choices': replace_choices,
        'empty_option': empty_option,
        'value': value,
        # TODO: radio values?
    }



@register.inclusion_tag("spectre-css/render-form-field.html")
def render_form_field_default(field: BoundField):
    field_classes = "form-input"
    overriden_classes = field.field.widget.attrs.get("class", "")
    field_classes += " " + overriden_classes

    return {"field": field, "field_class": field_classes}


@register.inclusion_tag('spectre-css/render-form-checkbox.html')
def render_form_checkbox(field: BoundField, switch: bool = False):
    return {'field': field, 'switch': switch}


@register.inclusion_tag('spectre-css/render-form-field.html')
def render_form_select(field: BoundField, add_choices: choice_list_type = None,
                       replace_choices: choice_list_type = None, empty_option: str = None):
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


@register.inclusion_tag('spectre-css/form-header.html')
def render_form_header(form: Form):
    return {'form': form}


@register.inclusion_tag('spectre-css/render-multi-field-part.html')
def render_multi_field_part(field: BoundField, index: int, label_text: Optional[str] = None, bare: bool = False,
                            additional_class: str = ""):
    return {
        'field': field,
        'index': index,
        'label_text': label_text,
        'field_class': 'form-input',
        'field_id': "{}_{}".format(field.auto_id, index),
        'bare': bare,
        'additional_class': additional_class,
    }


@register.inclusion_tag('spectre-css/render-multi-field.html')
def render_multi_field(field: BoundField):
    return {
        'field': field,
        'count': range(0, len(field.field.fields))
    }
