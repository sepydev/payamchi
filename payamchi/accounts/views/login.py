from django import views
from django.contrib.auth import get_user_model, login, logout
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
            user = form.login(request)
            remember_me = form.cleaned_data['remember_me']
            if user:
                login(request, user)
                if not remember_me:
                    request.session.set_expiry(0)
                return redirect('core:home')
        return render(
            request,
            template_name=self.template_name,
            context={
                'form': form,
            }
        )


def logout_view(request):
    logout(request)
    return redirect('accounts:login')
