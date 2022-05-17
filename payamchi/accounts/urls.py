from django.urls import path

from .views.login import LoginView
from .views.register import RegisterView, RegisterConfirmView

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('register-confirm/', RegisterConfirmView.as_view(), name='register_confirm'),
    path('login/', LoginView.as_view(), name='login'),
    # to do create forget password form
    path('forget-password/', RegisterConfirmView.as_view(), name='forget_password'),

]
