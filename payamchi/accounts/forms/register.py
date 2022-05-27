from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Layout, Field, Row, Column, Submit
from django import forms
from django.contrib.auth import get_user_model

from core.forms import ERROR_MESSAGES_REQUIRED, ERROR_MESSAGES_INVALID
from core.forms.form_field import MobileValidator

User = get_user_model()


class RegisterForm(forms.ModelForm):
    birth_date_persian = forms.CharField(label='تاریخ تولد',
                                         error_messages=ERROR_MESSAGES_REQUIRED,
                                         )
    birth_date = forms.CharField()
    mobile = forms.CharField(
        label='موبایل',
        validators=[MobileValidator()],
        error_messages={**ERROR_MESSAGES_REQUIRED},
    )
    ir_code = forms.CharField(
        widget=forms.NumberInput(),
        label='کد ملی',
        error_messages={**ERROR_MESSAGES_REQUIRED, **ERROR_MESSAGES_INVALID},
    )

    helper = FormHelper()
    helper.layout = Layout(
        Row(
            Column('first_name'),
            Column('last_name'),
            css_class='form-row'
        ),
        Row(
            Column(Field('mobile', css_class='hide_arrow_number')),
            Column(Field('ir_code', css_class='hide_arrow_number')),
            css_class='form-row'
        ),
        Row(
            Column(Field('birth_date_persian')),
            Column(Field('father')),
            css_class='form-row'
        ),
        Field('birth_date', css_class='d-none'),
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
            'first_name': {**ERROR_MESSAGES_REQUIRED, **ERROR_MESSAGES_INVALID},
            'last_name': {**ERROR_MESSAGES_REQUIRED, **ERROR_MESSAGES_INVALID},
            'mobile': {**ERROR_MESSAGES_REQUIRED, **ERROR_MESSAGES_INVALID},
            'ir_code': {**ERROR_MESSAGES_REQUIRED, **ERROR_MESSAGES_INVALID},
            'birth_date': {**ERROR_MESSAGES_REQUIRED, **ERROR_MESSAGES_INVALID},
        }
