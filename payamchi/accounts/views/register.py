import json

from django import views
from django.shortcuts import render, redirect

from ..forms.register import RegisterForm, RegisterConfirmForm


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
            request.session['birth_date'] = clean_data['birth_date'].strftime("%m/%d/%Y")
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
        return render(
            request,
            template_name=self.template_name,
            context={
                'register_user': register_user,
                'form': self.form
            }
        )
