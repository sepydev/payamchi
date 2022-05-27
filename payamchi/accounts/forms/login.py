from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Div, Layout, Field, Submit, Row,
    Column, HTML

)
from django import forms
from django.contrib.auth import get_user_model, authenticate

from core.forms import ERROR_MESSAGES_REQUIRED, ERROR_MESSAGES_INVALID
from core.forms.form_field import MobileValidator

User = get_user_model()


class LoginForm(forms.Form):
    mobile = forms.CharField(
        label='موبایل',
        validators=[MobileValidator()],
        error_messages={**ERROR_MESSAGES_REQUIRED},
    )
    password = forms.CharField(
        widget=forms.PasswordInput(),
        label='کلمه عبور',
        error_messages={**ERROR_MESSAGES_REQUIRED, **ERROR_MESSAGES_INVALID},
    )
    remember_me = forms.BooleanField(
        widget=forms.CheckboxInput(),
        label='من را به خاطر بسپار',
        required=False
    )
    helper = FormHelper()
    helper.layout = Layout(
        Div(
            Field('mobile', css_class='hide_arrow_number'),
            Field('password'),
            Row(
                Column('remember_me'),
                Column(
                    HTML(
                        "<a class='text-primary' href=\"{% url 'accounts:forget_password' %}\">"
                        "رمز عبور خود را فراموش کرده اید؟</a>"
                    ),
                    css_class="form-group"
                ),
                css_class='form-row'
            ),

            css_class=''
        ),
        Div(
            Submit('submit', 'وارد شوید', css_class='btn btn-primary btn-block'),
            css_class='text-center mt-4'
        ),
    )

    def clean_password(self):
        mobile = self.cleaned_data.get('mobile')
        password = self.cleaned_data.get('password')
        _user = authenticate(mobile=mobile, password=password)
        if not _user or not _user.is_active:
            raise forms.ValidationError("نام کاربری یا کلمه عبور صحیح نمی باشد.")
        return password

    def login(self, request):
        mobile = self.cleaned_data.get('mobile')
        password = self.cleaned_data.get('password')
        _user = authenticate(mobile=mobile, password=password)
        return _user
