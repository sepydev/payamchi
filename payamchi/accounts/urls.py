from django.urls import path

from .views.forget_password import ForgetPasswordView, ResetPasswordView
from .views.login import LoginView, logout_view
from .views.register import RegisterView, RegisterConfirmView

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('register-confirm/', RegisterConfirmView.as_view(), name='register_confirm'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('forget-password/', ForgetPasswordView.as_view(), name='forget_password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),

]
