from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Layout, Field, Row, Column, Submit
from django import forms
from django.contrib.auth import get_user_model
from jalali_date.fields import JalaliDateField
from jalali_date.widgets import AdminJalaliDateWidget

from ..forms import ERROR_MESSAGES_REQUIRED

User = get_user_model()


class RegisterForm(forms.ModelForm):
    birth_date = JalaliDateField(label='تاریخ تولد',
                                 widget=AdminJalaliDateWidget,
                                 error_messages=ERROR_MESSAGES_REQUIRED,
                                 )

    helper = FormHelper()
    helper.layout = Layout(
        Row(
            Column('first_name', css_calss='form-group'),
            Column('last_name', css_calss='form-group'),
            css_class='form-row'
        ),
        Row(
            Column(Field('mobile'), css_calss='form-group'),
            Column(Field('ir_code'), css_calss='form-group'),
            css_class='form-row'
        ),
        Row(
            Column(Field('birth_date'), css_calss='form-group'),
            Column(Field('father'), css_calss='form-group'),
            css_class='form-row'
        ),
        Div(
            Submit('submit', 'مرحله بعد', css_class='col-3 btn btn-primary btn-block'),
            css_class='text-center mt-4'
        ),
    )

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'mobile',
            'ir_code',
            'birth_date',
            'father',
        )
        error_messages = {
            'first_name': ERROR_MESSAGES_REQUIRED,
            'last_name': ERROR_MESSAGES_REQUIRED,
            'mobile': ERROR_MESSAGES_REQUIRED,
            'ir_code': ERROR_MESSAGES_REQUIRED,
            'birth_date': ERROR_MESSAGES_REQUIRED,
        }
