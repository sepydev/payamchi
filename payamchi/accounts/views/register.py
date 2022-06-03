from django import views
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from sms.send import send

from .helper import get_secret_code
from ..forms.otp_confirm import OTPConfirmForm
from ..forms.register import RegisterForm
from ..models import OTP

User = get_user_model()


class RegisterView(views.View):
    template_name = 'accounts/register.html'
    form = RegisterForm

    def get(self, request):
        form = self.form
        if request.session.get('first_name'):
            register_user = {
                'first_name': request.session['first_name'],
                'last_name': request.session['last_name'],
                'mobile': request.session['mobile'],
                'ir_code': request.session['ir_code'],
                'father': request.session['father'],
                'birth_date': request.session['birth_date'],
            }
            form = self.form(
                initial=register_user
            )

        return render(
            request,
            template_name=self.template_name,
            context={
                'form': form,
            }
        )

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data
            request.session['first_name'] = clean_data['first_name']
            request.session['last_name'] = clean_data['last_name']
            request.session['mobile'] = clean_data['mobile']
            request.session['ir_code'] = clean_data['ir_code']
            request.session['father'] = clean_data['father']
            request.session['birth_date'] = clean_data['birth_date']
            secret_code = get_secret_code()
            OTP.objects.create(secret_code=secret_code, mobile=clean_data['mobile'])
            bulk_id = send(secret_code, clean_data['mobile'])
            print(f" کد تایید  {secret_code}  -- {bulk_id}")
            return redirect('accounts:register_confirm')
        return render(
            request,
            template_name=self.template_name,
            context={
                'form': form,
            }
        )


class RegisterConfirmView(views.View):
    template_name = 'accounts/otp_confirm.html'
    form = OTPConfirmForm

    def get(self, request):
        register_user = {
            'first_name': request.session['first_name'],
            'last_name': request.session['last_name'],
            'mobile': request.session['mobile'],
            'ir_code': request.session['ir_code'],
            'father': request.session['father'],
            'birth_date': request.session['birth_date'],
        }
        form = self.form(
            initial={'mobile': request.session['mobile'],
                     'confirm_code': '',
                     'password': '',
                     'password_confirm': '',

                     }
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
            return redirect('accounts:register')
        form = self.form(request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data
            password = clean_data['password']
            mobile = request.session['mobile']
            User.objects.create_user(
                mobile=mobile,
                username=mobile,
                password=password,
                first_name=request.session['first_name'],
                last_name=request.session['last_name'],
                ir_code=request.session['ir_code'],
                father=request.session['father'],
                birth_date=request.session['birth_date'],
            )
            return redirect('core:home')
        return render(
            request,
            self.template_name,
            {
                'form': form
            }
        )
