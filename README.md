# django-spectre-css

This Module uses spectre.css (https://picturepan2.github.io/spectre/) to style a Django application.


## Installation

Install:

    pip install django-spectre-css


To use include `static/css/lib/\*.css` in your base templates css files or in your CSS pipeline


add it to your installed apps:

    INSTALLED_APPS = [
        '...',
        'django_spectre_css',
        'widget_tweaks',
    ]

## Warning

The help_text from models is marked as save in the template and therefore it is possible to have html e.g. links in the help_text.
This means that help_text of an ModelField should **never be directly based on user input**.

## Examples:
This module defines the following tags to make displaying forms easier.

- render the form header (csrf-token and non-field errors) for the form 'form':


    {% load spectre_css %}
    <form method="POST">
    {% render_form_header form %}
    [...]
    </form>

- render a field user of the form 'form':


    {% extends base.html %}
    {% load spectre_css %}

    [...]
    {% render_form_field form.user %}

- render the whole form:


    {% extends base.html %}
    {% load spectre_css %}

    <form method="POST">
    {% render_form form %}
    <input type="submit" value="Save" class="btn btn-primary">
    </form>
    
- render the first two parts of a MultiValueField as independent Fields:


    {% extends base.html %}
    {% load spectre_css %}

    [...]
    {% render_form_field form.datetime 0 label_text="Date"%}
    {% render_form_field form.datetime 1 label_text="Time" %}


`render_form_field` takes the following keyword arguments:

- `switch=True|False` for checkboxes, if `True` renders the checkbox as switch
- `add_choices=[(value,text),...]` to add the choices of an select to the select
- `replace_choices=[(value,text),...]` to set the choices of an select manually
- `empty_option=value` to generate an empty option if None is selected with the text `value`  (only select widgets)
- `value=value` overwrites the initial value of the field (not Checkbox and Select) with `value` 

## Upgrades

### From < 0.3

`'django-spectre-css'` has to be changed into `'django_spectre_css'` in th `INSTALLED_APPS` in Django settings.py
