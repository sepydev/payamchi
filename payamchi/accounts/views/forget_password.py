from django import views
from django.shortcuts import render, redirect
from sms.send import send

from .helper import get_secret_code
from ..forms.forget_password import ForgetPasswordForm, User
from ..forms.otp_confirm import OTPConfirmForm
from ..models import OTP


class ForgetPasswordView(views.View):
    template_name = 'accounts/forget_password.html'
    form = ForgetPasswordForm

    def get(self, request):
        return render(
            request,
            template_name=self.template_name,
            context={'form': self.form}
        )

    def post(self, request):
        if 'cancel' in self.request.POST:
            return redirect('accounts:login')
        form = self.form(request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data
            mobile = clean_data['mobile']
            request.session['mobile'] = mobile
            secret_code = get_secret_code()
            OTP.objects.create(secret_code=secret_code, mobile=clean_data['mobile'])
            bulk_id = send(secret_code, clean_data['mobile'])
            print(f" کد تایید  {secret_code}  -- {bulk_id}")
            return redirect('accounts:reset_password')
        return render(
            request,
            template_name=self.template_name,
            context={
                'form': form,
            }
        )


class ResetPasswordView(views.View):
    template_name = 'accounts/otp_confirm.html'
    form = OTPConfirmForm

    def get(self, request):
        register_user = {
            'mobile': request.session['mobile'],
        }
        form = self.form(
            initial={'mobile': request.session['mobile']}
        )
        return render(
            request,
            template_name=self.template_name,
            context={
                'register_user': register_user,
                'form': form
            }
        )

    def post(self, request):
        if 'cancel' in self.request.POST:
            return redirect('accounts:forget_password')
        form = self.form(request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data
            password = clean_data['password']
            mobile = request.session['mobile']
            user = User.objects.filter(mobile=mobile).first()
            user.set_password(password)
            user.save()
            return redirect('accounts:login')
        return render(
            request,
            self.template_name,
            {
                'form': form
            }
        )
