from flask_wtf import Form

from wtforms import SelectMultipleField, SelectField, RadioField, SubmitField, TextAreaField
from wtforms.validators import Required
from flask_wtf.html5 import IntegerRangeField
from wtforms.widgets.core import HTMLString, html_params, text_type, escape


class SelectPicker(SelectField):
    def pre_validate(self, form):
        return str(self.data)


class SelectPickerMultiWidget(object):
    multiple = True
    optgroups = dict()

    def pre_validate(self, form):
        return str(self.data)

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        if self.multiple:
            kwargs['multiple'] = True
        html = ['<select %s multiple>' % html_params(name=field.name, **kwargs)]
        for val, label, selected in field.iter_choices():
            html.append(self.render_option(val, label, selected))
        html.append('</select>')
        return HTMLString(''.join(html))

    @classmethod
    def render_option(cls, value, label, selected, **kwargs):
        if value is True:
            # Handle the special case of a 'True' value.
            value = text_type(value)

        options = dict(kwargs, value=value)
        if selected:
            options['selected'] = True
        return HTMLString('<option %s>%s</option>' %
            (html_params(**options), escape(text_type(label), quote=False)))


class SelectPickerMulti(SelectMultipleField):
    widget = SelectPickerMultiWidget()

    def pre_validate(self, form):
        return str(self.data)


class UserSettingsForm(Form):
    distance_preference = IntegerRangeField('Please select distance radius in miles')
    gender_preference = RadioField('gender', validators=[Required("Please select gender")],
                        choices=[('female', 'Female'), ('male', 'Male')])
    age_preference = IntegerRangeField('Please select age range')
    purpose_preference = SelectPickerMulti('Please select your purpose for meeting up',
        choices=[('support', 'Support'), ('study', 'Study'), ('chill', 'Chill')])
    submit = SubmitField('Save Preferences')


class PostForm(Form):
    body = TextAreaField('Please post to find someone in your area', validators=[Required()])
    submit = SubmitField('Save Preferences')