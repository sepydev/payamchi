from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field, Submit, Div
from django import forms

from ..forms import ERROR_MESSAGES_REQUIRED, ERROR_MESSAGES_INVALID
from ..models import Message, MessageTypeChoices, Channel, Campaign


class MessageForm(forms.ModelForm):
    message_type = forms.ChoiceField(
        label="نوع پیام",
        error_messages=ERROR_MESSAGES_REQUIRED,
        choices=MessageTypeChoices.choices
    )
    channel = forms.ModelChoiceField(
        label='کانال',
        error_messages=ERROR_MESSAGES_REQUIRED,
        queryset=None,
        required=False,
    )
    campaign = forms.ModelChoiceField(
        label='کمپین',
        error_messages=ERROR_MESSAGES_REQUIRED,
        queryset=None,
        required=False,

    )
    helper = FormHelper()
    helper.layout = Layout(
        Field('message_type'),
        Field('channel'),
        Field('caption'),
        Field('campaign'),
        Row(
            Column(
                Submit('submit', 'ذخیره', css_class='col-10 btn btn-primary btn-block')
            ),
            Column(
                Submit('cancel', 'بستن', css_class='col-10 btn btn-primary btn-block',
                       data_dismiss="modal")

            ),
            css_class="form-submit-row"
        )
    )

    class Meta:
        model = Message
        fields = (
            'message_type',
            'channel',
            'caption',
            'campaign',
        )

    def __init__(self, user, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields['channel'].queryset = Channel.objects.filter(owner=user)
        self.fields['campaign'].queryset = Campaign.objects.filter(user=user)
