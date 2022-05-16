from django.urls import path

from .views.register import RegisterView, RegisterConfirmView

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('register-confirm/', RegisterConfirmView.as_view(), name='register_confirm'),
    path('login/', RegisterView.as_view(), name='login'),
]
