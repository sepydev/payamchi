from django.urls import path

from .views.home import HomeView
from .views.inbox import InboxView

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('inbox/', InboxView.as_view(), name='inbox'),

]
