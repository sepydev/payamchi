from django import views
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect

from ..forms.login import LoginForm

User = get_user_model()


class LoginView(views.View):
    template_name = 'accounts/login.html'
    form = LoginForm

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
            mobile = clean_data['mobile']
            password = clean_data['password']
            user = authenticate(request, mobile=mobile, password=password)
            if user:
                login(request, user)
                # to do handel remember me
                return redirect('core:home')
            # to do if user pass invalid show error

        return render(
            request,
            template_name=self.template_name,
            context={
                'form': form,
            }
        )
