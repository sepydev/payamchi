from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Div, Layout, Field, Submit, Row,
    Column, HTML

)
from django import forms
from django.contrib.auth import get_user_model

from ..forms import ERROR_MESSAGES_REQUIRED

User = get_user_model()


class LoginForm(forms.Form):
    mobile = forms.CharField(
        widget=forms.TextInput(),
        label='موبایل',
        error_messages=ERROR_MESSAGES_REQUIRED,
    )
    password = forms.CharField(
        widget=forms.PasswordInput(),
        label='کلمه عبور',
        error_messages=ERROR_MESSAGES_REQUIRED,
    )
    remember_me = forms.BooleanField(
        widget=forms.CheckboxInput(),
        label='من را به خاطر بسپار',
        required=False
    )
    helper = FormHelper()
    helper.layout = Layout(
        Div(
            Field('mobile'),
            Field('password'),
            Row(
                Column('remember_me', css_calss='form-group'),
                Column(
                    HTML(
                        "<a class='text-primary' href=\"{% url 'accounts:forget_password' %}\">"
                        "رمز عبور خود را فراموش کرده اید؟</a>"
                    ),
                    css_calss="form-group"
                ),
                css_class='form-row'
            ),

            css_class=''
        ),
        Div(
            Submit('submit', 'وارد شوید', css_class='col-3 btn btn-primary btn-block'),
            css_class='text-center mt-4'
        ),
    )
