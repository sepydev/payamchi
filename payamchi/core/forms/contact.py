from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field, Submit
from django import forms

from .form_field import MobileValidator
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
                message='یکی از فیلد های مخاطب بایستی پر شود',

            )
        return self.cleaned_data
