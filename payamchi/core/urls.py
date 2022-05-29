from django.urls import path

from .views.campaign import CampaignAddView, CampaignView, CampaignListView, CampaignDetailView
from .views.contact import ContactListView, ContactView, ContactDetailView, ContactLabelsView, ContactAddView, \
    contact_define_labels
from .views.contact_define_label import ContactDefineLabelAutocomplete
from .views.home import HomeView
from .views.inbox import InboxView

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('inbox/', InboxView.as_view(), name='inbox'),

    # contact

    path('contact-add/', ContactAddView.as_view(), name='contact-add'),
    path('contact-add/<int:pk>/', ContactAddView.as_view(), name='contact-edit'),

    path('contacts/', ContactView.as_view(), name='contacts'),
    path('contact-list/<int:upper>/', ContactListView.as_view(), name="contact-list"),
    path('contact-detail/<int:pk>/', ContactDetailView.as_view(), name="contact-detail"),

    path('contact-labels/', ContactLabelsView.as_view(), name="contact-labels"),
    path('contact-labels/<int:contact_id>/<int:label_id>/', ContactLabelsView.as_view(), name="contact-labels"),

    path('contact-define-label/', ContactDefineLabelAutocomplete.as_view(), name="contact-define-label"),
    path('contact-define-labels/', contact_define_labels, name='contanct-define-labels'),

    # campaign
    path('campaign-add/', CampaignAddView.as_view(), name='campaign-add'),
    path('campaign-add/<int:pk>/', CampaignAddView.as_view(), name='campaign-edit'),
    path('campaigns/', CampaignView.as_view(), name='campaigns'),
    path('campaign-list/<int:upper>/', CampaignListView.as_view(), name="campaign-list"),
    path('campaign-detail/<int:pk>/', CampaignDetailView.as_view(), name="campaign-detail"),

]
