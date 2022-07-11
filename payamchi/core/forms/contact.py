from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field, Submit, Div
from django import forms

from .form_field import MobileValidator, PhoneValidator
from ..forms import ERROR_MESSAGES_REQUIRED, ERROR_MESSAGES_INVALID, ERROR_MESSAGES_EMAIL_INVALID
from ..models import Contact


class ContactForm(forms.ModelForm):
    mobile = forms.CharField(
        label='موبایل',
        validators=[MobileValidator()],
        error_messages={
            **ERROR_MESSAGES_REQUIRED
        },
        required=False,
    )
    tel = forms.CharField(
        label='تلفن',
        validators=[PhoneValidator()],
        error_messages={
            **ERROR_MESSAGES_REQUIRED
        },
        required=False,
    )

    helper = FormHelper()
    helper.layout = Layout(
        Field('caption'),
        Field('mobile'),
        Field('tel'),
        Field('email'),
        Field('telegram_id'),
        Field('whatsapp_id'),
        Row(

            Column(
                Submit('submit', 'ذخیره', css_class='col-10 btn btn-primary btn-block')
            ),
            Column(
                Submit('cancel', 'بستن', css_class='col-10 btn btn-danger btn-block',
                       data_dismiss="modal")
            ),
            css_class='form-submit-row'
        ),
    )

    class Meta:
        model = Contact
        fields = (
            'caption',
            'mobile',
            'tel',
            'email',
            'telegram_id',
            'whatsapp_id',
        )
        error_messages = {
            'caption': {**ERROR_MESSAGES_REQUIRED, **ERROR_MESSAGES_INVALID},
            'mobile': {**ERROR_MESSAGES_REQUIRED, **ERROR_MESSAGES_INVALID},
            'tel': {**ERROR_MESSAGES_REQUIRED, **ERROR_MESSAGES_INVALID},
            'email': {**ERROR_MESSAGES_REQUIRED, **ERROR_MESSAGES_INVALID},
            'telegram_id': {**ERROR_MESSAGES_REQUIRED, **ERROR_MESSAGES_INVALID},
            'whatsapp_id': {**ERROR_MESSAGES_REQUIRED, **ERROR_MESSAGES_INVALID},
        }

    def clean(self):
        if (
                not self.cleaned_data.get('email', None) and
                not self.cleaned_data.get('mobile', None) and
                not self.cleaned_data.get('tel', None) and
                not self.cleaned_data.get('telegram_id', None) and
                not self.cleaned_data.get('whatsapp_id', None)
        ):
            raise forms.ValidationError(
                message='یکی از فیلد های (موبایل، تلفن، پست الکترونیک، تلگرام یا واتس اپ) بایستی پر شود',

            )
        return self.cleaned_data


class ContactImportForm(forms.Form):
    caption = forms.ChoiceField(
        label='عنوان',
        required=True,
        error_messages={
            **ERROR_MESSAGES_REQUIRED
        },
    )
    mobile = forms.ChoiceField(
        label='موبایل',
        required=False,
    )
    tel = forms.ChoiceField(
        label='تلفن',
        required=False,
    )
    email = forms.ChoiceField(
        label='ایمیل',
        required=False,
    )
    telegram_id = forms.ChoiceField(
        label='تلگرام',
        required=False,
    )
    whatsapp_id = forms.ChoiceField(
        label='واتس اپ',
        required=False,
    )
    file_name = forms.CharField(
        label='نام فایل',
        required=True,
    )
    tags = forms.CharField(
        label='برچسب ها',
        required=False,
    )

    helper = FormHelper()
    helper.layout = Layout(
        Field('caption', css_class='col-lg-4'),
        Field('mobile', css_class='col-lg-4'),
        Field('tel', css_class='col-lg-4'),
        Field('email', css_class='col-lg-4'),
        Field('telegram_id', css_class='col-lg-4'),
        Field('whatsapp_id', css_class='col-lg-4'),
        Field('tags',),
        Div(Field('file_name'), style='display: none;'),
        Row(

            Column(
                Submit('submit', 'ذخیره', css_class='col-10 btn btn-primary btn-block')
            ),
            Column(
                Submit('cancel', 'انصراف', css_class='col-10 btn btn-danger btn-block',
                       )
            ),
            css_class='form-submit-row col-lg-4'
        ),
    )

    def clean(self):
        if (
                not self.cleaned_data.get('email', None) and
                not self.cleaned_data.get('mobile', None) and
                not self.cleaned_data.get('tel', None) and
                not self.cleaned_data.get('telegram_id', None) and
                not self.cleaned_data.get('whatsapp_id', None)
        ):
            raise forms.ValidationError(
                message='یکی از فیلد های (موبایل، تلفن، پست الکترونیک، تلگرام یا واتس اپ) بایستی پر شود',

            )
        return self.cleaned_data
