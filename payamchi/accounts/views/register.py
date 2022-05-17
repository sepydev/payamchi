import secrets
import string

from django import views
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from payamchi.settings import CONFIRM_CODE_LENGTH
from sms.send import send

from ..forms.register import RegisterForm, RegisterConfirmForm
from ..models import OTP

User = get_user_model()


class RegisterView(views.View):
    template_name = 'accounts/register.html'
    form = RegisterForm

    def get(self, request):
        return render(
            request,
            template_name=self.template_name,
            context={
                'form': self.form,
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
            request.session['birth_date'] = clean_data['birth_date'].strftime("%Y-%m-%d")
            secret_code = ''.join(secrets.choice(string.digits) for _ in range(CONFIRM_CODE_LENGTH))
            OTP.objects.create(secret_code=secret_code, mobile=clean_data['mobile'])
            bulk_id = send(f" کد تایید  {secret_code}", [clean_data['mobile']])
            print(f" کد تایید  {secret_code}")
            return redirect('accounts:register_confirm')
        return render(
            request,
            template_name=self.template_name,
            context={
                'form': form,
            }
        )


class RegisterConfirmView(views.View):
    template_name = 'accounts/register_confirm.html'
    form = RegisterConfirmForm

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
