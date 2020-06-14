# idea from https://github.com/treyhunner/django-widget-tweaks/commit/e89ba60899abfce2953bd3f5583645f5d73447a3
# adapted with snippets from widget_tweaks original code; modified by Nils Rokita

from django import template

from widget_tweaks.templatetags.widget_tweaks import ATTRIBUTE_RE

register = template.Library()


@register.tag
def render_multi_field(parser, token):
    """
    Takes form field as first argument, field number as second argument, and
    list of attribute-value pairs for all other arguments.
    Attribute-value pairs should be in the form of attribute=value OR
    attribute="a value"
    """
    error_msg = ('%r tag requires a form field and index followed by a list '
                 'of attributes and values in the form attr="value"'
                 % token.split_contents()[0])
    try:
        bits = token.split_contents()
        form_field = bits[1]
        field_index = bits[2]
        attr_list = bits[3:]
    except ValueError:
        raise template.TemplateSyntaxError(error_msg)

    field_index = parser.compile_filter(field_index)
    form_field = parser.compile_filter(form_field)

    set_attrs = []
    append_attrs = []
    for pair in attr_list:
        match = ATTRIBUTE_RE.match(pair)
        if not match:
            raise template.TemplateSyntaxError(error_msg + ": %s" % pair)
        dct = match.groupdict()
        attr, sign, value = \
            dct['attr'], dct['sign'], parser.compile_filter(dct['value'])
        if sign == "=":
            set_attrs.append((attr, value))
        else:
            append_attrs.append((attr, value))

    return MultiFieldAttributeNode(form_field, set_attrs,
                                   append_attrs, index=field_index)


class MultiFieldAttributeNode(template.Node):
    def __init__(self, field, assign_dict, concat_dict, index):
        self.field = field
        self.set_attrs = assign_dict
        self.append_attrs = concat_dict
        self.index = index

    def render(self, context):
        index = self.index.resolve(context)
        bounded_field = self.field.resolve(context)
        field = bounded_field.field.fields[index]
        widget = bounded_field.field.widget.widgets[index]

        attrs = widget.attrs.copy()
        print(attrs)
        for k, v in self.set_attrs:
            attrs[k] = v.resolve(context)
        for k, v in self.append_attrs:
            attrs[k] = attrs.get(k, '') + ' ' + v.resolve(context)
        if bounded_field.errors:
            attrs['class'] = attrs.get('class', '') + ' error'

        if not bounded_field.form.is_bound:
            data = bounded_field.form.initial.get(bounded_field.name,
                                                  field.initial)
            if callable(data):
                data = data()
            data = bounded_field.field.widget.decompress(data)[index]
        else:
            data = bounded_field.data[index]
        return widget.render('%s_%d' % (bounded_field.html_name, index),
                             data, attrs)
