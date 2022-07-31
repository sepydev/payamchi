from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field, Submit, Div, HTML
from django import forms

from ..forms import ERROR_MESSAGES_REQUIRED
from ..models import Message, MessageTypeChoices, Channel, Campaign, MessageTemplate


class MessageFormPartially(forms.ModelForm):
    message_type = forms.ChoiceField(
        label="نوع پیام",
        error_messages=ERROR_MESSAGES_REQUIRED,
        choices=MessageTypeChoices.choices
    )
    channel = forms.ModelChoiceField(
        label='کانال',
        queryset=None,
        required=False,
    )
    campaign = forms.ModelChoiceField(
        label='کمپین',
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
        error_messages = {
            'caption': {**ERROR_MESSAGES_REQUIRED},
        }

    def __init__(self, user, *args, **kwargs):
        super(MessageFormPartially, self).__init__(*args, **kwargs)
        self.fields['channel'].queryset = Channel.objects.filter(owner=user)
        self.fields['campaign'].queryset = Campaign.objects.filter(user=user)


class MessageForm(forms.ModelForm):
    message_type = forms.ChoiceField(
        label="نوع پیام",
        error_messages=ERROR_MESSAGES_REQUIRED,
        choices=MessageTypeChoices.choices
    )
    channel = forms.ModelChoiceField(
        label='کانال',
        queryset=None,
        required=False,
    )
    campaign = forms.ModelChoiceField(
        label='کمپین',
        queryset=None,
        required=False,
    )
    message_template = forms.ModelChoiceField(
        label='قالب پیام',
        error_messages=ERROR_MESSAGES_REQUIRED,
        queryset=None,
    )
    send_date_persian = forms.CharField(
        label='تاریخ ارسال',
        error_messages=ERROR_MESSAGES_REQUIRED,
    )
    send_date = forms.CharField()

    helper = FormHelper()
    helper.layout = Layout(
        Field('message_type'),
        Field('channel'),
        Field('campaign'),
        Field('caption'),
        Field('message_template'),
        Field('send_date_persian'),
        Field('effort', css_class='hide_arrow_number'),
        Field('send_effort_delay', css_class='hide_arrow_number'),
        Div(Field('send_date'), css_class='d-none'),
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
            'message_template',
            'send_date',
            'send_date_persian',
            'effort',
            'send_effort_delay',
        )

        error_messages = {
            'caption': {**ERROR_MESSAGES_REQUIRED},
            'effort': {**ERROR_MESSAGES_REQUIRED},
            'send_effort_delay': {**ERROR_MESSAGES_REQUIRED},
        }

    def __init__(self, user, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields['channel'].queryset = Channel.objects.filter(owner=user)
        self.fields['campaign'].queryset = Campaign.objects.filter(user=user)
        self.fields['message_template'].queryset = MessageTemplate.objects.filter(user=user)


class MessageDetailForm(forms.ModelForm):
    message_type = forms.ChoiceField(
        label="نوع پیام",
        error_messages=ERROR_MESSAGES_REQUIRED,
        choices=MessageTypeChoices.choices
    )
    channel = forms.ModelChoiceField(
        label='کانال',
        queryset=None,
        required=False,
    )
    campaign = forms.ModelChoiceField(
        label='کمپین',
        queryset=None,
        required=False,
    )
    message_template = forms.ModelChoiceField(
        label='قالب پیام',
        error_messages=ERROR_MESSAGES_REQUIRED,
        queryset=None,
    )
    send_date_persian = forms.CharField(
        label='تاریخ ارسال',
        error_messages=ERROR_MESSAGES_REQUIRED,
    )
    send_date = forms.CharField()

    helper = FormHelper()
    helper.layout = Layout(
        Field('message_type'),
        Field('channel'),
        Field('campaign'),
        Field('caption'),
        Row(
            Div(Field('message_template'), css_class='col-9'),
            Div(HTML('''<label class='p-2'> <span></span> </label>
            <div> <a href="javascript:void(0)"  >
                 <button class="btn btn-success p-2 m-0 btn-sm"
                    data-action="{% url 'core:message-template-add' %}"
                    data-title="قالب پیام جدید"
                    data-subtitle=""
                    data-icon="fa-keyboard-o"
                    data-button-save-label="ذخیره"
                    onclick="openMyModal(event,loadMessageDetail,{{ message.id }}); return false;">
                جدید
                </button>
                </a> </div>'''
                     ), css_class='col-3 center'),

        ),
        Field('send_date_persian'),
        Field('effort', css_class='hide_arrow_number'),
        Field('send_effort_delay', css_class='hide_arrow_number'),
        Div(Field('send_date'), css_class='d-none'),
        HTML('''
        <div  id = 'div_id_messageLabels'   class="form-group row col-12">
                <label class="col-4 center">برچسب های پیام</label>
                <select id="messageLabels" multiple="multiple" name="state">
                    {% for message_label in message_labels %}#}
                        <option class="test" id="{{ message_label.id }}"
                                selected="selected"
                                value="{{ message_label.id }}"
                        >
                            {{ message_label.caption }}
                        </option>
                    {% endfor %}
                </select>
            </div>
            <div id="div_id_contactLabels" class="form-group row col-12">
                <label class="col-4 center">انتخاب مخاطبان</label>
                <select id="contactLabels" multiple="multiple" name="state">
                    {% for contact_label in contact_labels %}#}
                        <option class="test" id="{{ contact_label.id }}"
                                selected="selected"
                          value="{{ contact_label.id }}"
                        >
                            {{ contact_label.caption }}
                        </option>
                    {% endfor %}
                </select>
            </div>
        '''
             ),
        # Submit('submit', 'ذخیره', css_class='col-3 btn btn-primary btn-block form-submit-row')

    )

    class Meta:
        model = Message
        fields = (
            'message_type',
            'channel',
            'caption',
            'campaign',
            'message_template',
            'send_date',
            'send_date_persian',
            'effort',
            'send_effort_delay',
        )

        error_messages = {
            'caption': {**ERROR_MESSAGES_REQUIRED},
            'effort': {**ERROR_MESSAGES_REQUIRED},
            'send_effort_delay': {**ERROR_MESSAGES_REQUIRED},
        }

    def __init__(self, user, *args, **kwargs):
        super(MessageDetailForm, self).__init__(*args, **kwargs)
        self.fields['channel'].queryset = Channel.objects.filter(owner=user)
        self.fields['campaign'].queryset = Campaign.objects.filter(user=user)
        self.fields['message_template'].queryset = MessageTemplate.objects.filter(user=user)
