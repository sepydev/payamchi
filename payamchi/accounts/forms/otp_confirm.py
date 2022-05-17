from datetime import timedelta

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Layout, Field, Submit, Row, Column
from django import forms
from django.contrib.auth import get_user_model
from django.utils import timezone
from captcha.fields import CaptchaField


from ..forms import ERROR_MESSAGES_REQUIRED
from ..models import OTP

User = get_user_model()

class OTPConfirmForm(forms.Form):
    mobile = forms.CharField(widget=forms.HiddenInput())
    confirm_code = forms.CharField(
        label='کد امنیتی',
        error_messages=ERROR_MESSAGES_REQUIRED,
    )
    password = forms.CharField(
        widget=forms.PasswordInput(),
        label='کلمه عبور',
        error_messages=ERROR_MESSAGES_REQUIRED,
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(),
        label='تکرار کلمه عبور',
        error_messages=ERROR_MESSAGES_REQUIRED,
    )
    captcha = CaptchaField(
        label='',
        error_messages=ERROR_MESSAGES_REQUIRED,
    )

    helper = FormHelper()
    helper.layout = Layout(
        Div(
            Field('mobile', type='hidden'),
            Div(Field('confirm_code'), css_class='col-6'),
            Div(Field('password'), css_class='col-6'),
            Div(Field('password_confirm'), css_class='col-6'),
            Div(Field('captcha'), css_class='col-3'),
            css_class=''),

        Row(
            Column(
                Submit('cancel', 'بازگشت', css_class='col-10 btn btn-light btn-block')
                , css_calss='form-group'),
            Column(
                Submit('submit', 'مرحله بعد', css_class='col-10 btn btn-primary btn-block')
                , css_calss='form-group'),
            css_class='form-row'
        ),
    )

    def clean_password_confirm(self):
        if self.cleaned_data['password'] != self.cleaned_data['password_confirm']:
            raise forms.ValidationError("کلمه عبور و تایید کلمه عبور یکسان نمی باشد")

    def clean_confirm_code(self):
        confirm_code_is_valid = OTP.objects.filter(
            mobile=self.cleaned_data['mobile'],
            secret_code=self.cleaned_data['confirm_code'],
            create_date__gte=(timezone.now() - timedelta(minutes=5))
        ).exists()
        if not confirm_code_is_valid:
            raise forms.ValidationError("کد امنیتی وارد شده صحیح نمی باشد")
