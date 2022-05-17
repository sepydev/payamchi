from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Column, Row, Submit
from django import forms
from django.contrib.auth import get_user_model

from ..forms import ERROR_MESSAGES_REQUIRED, ERROR_MESSAGES_INVALID

User = get_user_model()


class ForgetPasswordForm(forms.Form):
    mobile = forms.CharField(
        widget=forms.NumberInput(),
        label='موبایل',
        error_messages={**ERROR_MESSAGES_REQUIRED, **ERROR_MESSAGES_INVALID},
    )
    helper = FormHelper()
    helper.layout = Layout(
        Field('mobile', css_class='hide_arrow_number'),
        Row(
            Column(
                Submit('cancel', 'بازگشت', css_class='col-10 btn btn-light btn-block')
                ),
            Column(
                Submit('submit', 'مرحله بعد', css_class='col-10 btn btn-primary btn-block')
                ),
            css_class='form-row'
        ),

    )

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        _user = User.objects.filter(mobile=mobile).first()
        if not _user or not _user.is_active:
            raise forms.ValidationError("نام کاربری یا کلمه عبور صحیح نمی باشد.")
        return mobile
