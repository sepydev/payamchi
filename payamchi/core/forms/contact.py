from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field, Submit
from django import forms

from ..forms import ERROR_MESSAGES_REQUIRED, ERROR_MESSAGES_INVALID
from ..models import Contact


class ContactForm(forms.ModelForm):
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
            css_class='form-row'
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
