from django.urls import path

from .views.contact import ContactListView, ContactView, ContactDetailView, ContactLabelsView
from .views.contact_define_label import ContactDefineLabelAutocomplete
from .views.home import HomeView
from .views.inbox import InboxView

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('inbox/', InboxView.as_view(), name='inbox'),
    path('contacts/', ContactView.as_view(), name='contacts'),
    path('contact-list/<int:upper>/', ContactListView.as_view(), name="contact-list"),
    path('contact-detail/<int:pk>/', ContactDetailView.as_view(), name="contact-detail"),

    path('contact-labels/', ContactLabelsView.as_view(), name="contact-labels"),
    path('contact-labels/<int:contact_id>/<int:label_id>/', ContactLabelsView.as_view(), name="contact-labels"),
    path('contact-define-label/', ContactDefineLabelAutocomplete.as_view(), name="contact-define-label"),

]
