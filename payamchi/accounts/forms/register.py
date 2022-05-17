from datetime import timedelta

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Layout, Field, Row, Column, Submit
from django import forms
from django.contrib.auth import get_user_model
from django.utils import timezone
from jalali_date.fields import JalaliDateField
from jalali_date.widgets import AdminJalaliDateWidget

from ..forms import ERROR_MESSAGES_REQUIRED
from ..models import OTP

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


class RegisterConfirmForm(forms.Form):
    mobile = forms.CharField(widget=forms.HiddenInput())
    confirm_code = forms.IntegerField(
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
    helper = FormHelper()
    helper.layout = Layout(
        Div(
            Field('mobile', type='hidden'),
            Div(Field('confirm_code'), css_class='col-6'),
            Div(Field('password'), css_class='col-6'),
            Div(Field('password_confirm'), css_class='col-6'),
            css_class=''),
        Div(
            Submit('submit', 'ثبت', css_class='col-3 btn btn-primary btn-block'),
            css_class='text-center mt-4'
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
