from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field, Submit, Div
from django import forms

from ..forms import ERROR_MESSAGES_REQUIRED, ERROR_MESSAGES_INVALID
from ..models import Campaign


class CampaignForm(forms.ModelForm):
    start_date_persian = forms.CharField(
        label='تاریخ شروع',
        error_messages=ERROR_MESSAGES_REQUIRED,
    )
    start_date = forms.CharField()
    end_date_persian = forms.CharField(
        label='تاریخ پایان',
        error_messages=ERROR_MESSAGES_REQUIRED,
    )
    end_date = forms.CharField()

    helper = FormHelper()

    helper.layout = Layout(
        Field('caption'),
        Field('start_date_persian', css_class='col-6'),
        Div(
            Field('start_date')
            , css_class='d-none'),
        Field('end_date_persian', css_class='col-6'),
        Div(
            Field('end_date', ''),
            css_class='d-none'),
        Field('description', rows=4),
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
        model = Campaign
        fields = (
            'caption',
            'start_date',
            'end_date',
            'description',
        )
        error_messages = {
            'caption': {**ERROR_MESSAGES_REQUIRED, **ERROR_MESSAGES_INVALID},
            'start_date': {**ERROR_MESSAGES_REQUIRED, **ERROR_MESSAGES_INVALID},
            'end_date': {**ERROR_MESSAGES_REQUIRED, **ERROR_MESSAGES_INVALID},
            'description': {**ERROR_MESSAGES_REQUIRED, **ERROR_MESSAGES_INVALID},
        }
