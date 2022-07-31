from django.urls import path

from .views.campaign import CampaignAddView, CampaignView, CampaignListView, CampaignDetailView, CampaignMessages
from .views.contact import ContactListView, ContactView, ContactDetailView, ContactLabelsView, ContactAddView, \
    contact_define_labels, ContactImport, ContactImportSelectColumn
from .views.contact_define_label import ContactDefineLabelAutocomplete
from .views.home import HomeView
from .views.inbox import InboxView
from .views.message import MessageAddPartiallyView, MessageAddView, MessageView, MessageListView, MessageDetailView, \
    MessageDetailChartView
from .views.message_define_label import MessageDefineLabelsView, message_define_labels
from .views.message_template import MessageTemplateView, MessageTemplateUploadFileView

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('inbox/', InboxView.as_view(), name='inbox'),

    # contact

    path('contact-add/', ContactAddView.as_view(), name='contact-add'),
    path('contact-add/<int:pk>/', ContactAddView.as_view(), name='contact-edit'),

    path('contacts/', ContactView.as_view(), name='contacts'),
    path('contacts/<int:label_id>/', ContactView.as_view(), name='contacts'),
    path('contact-list/<int:upper>/', ContactListView.as_view(), name="contact-list"),
    path('contact-detail/<int:pk>/', ContactDetailView.as_view(), name="contact-detail"),
    path('contact-import/', ContactImport.as_view(), name="contact-import"),
    path(
        'contact-import-select-columns/<str:file_name>/',
        ContactImportSelectColumn.as_view(),
        name="contact-import-select-columns"
    ),
    path(
        'contact-import-select-columns/',
        ContactImportSelectColumn.as_view(),
        name="contact-import-select-columns"
    ),

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
    path('campaign-messages/', CampaignMessages.as_view(), name="campaign-messages"),

    # message
    path('message-add-partially/', MessageAddPartiallyView.as_view(), name='message-add-partially'),
    path('message-add/<str:message_type>/<str:campaign>', MessageAddView.as_view(), name='message-add'),
    path('message-add/', MessageAddView.as_view(), name='message-add'),
    path('messages/', MessageView.as_view(), name='messages'),
    path('message-list/<int:upper>/', MessageListView.as_view(), name='message-list'),
    path('message-detail/<int:pk>/', MessageDetailView.as_view(), name='message-detail'),
    # path('message-detail/', MessageDetailView.as_view(), name='message-detail'),

    #message detail chart
    path('message-detail/chart/<int:pk>/', MessageDetailChartView.as_view(), name='message-chart-detail'),

    # message template
    path('message-template-add/', MessageTemplateView.as_view(), name='message-template-add'),
    path('message-template-upload/', MessageTemplateUploadFileView.as_view(), name='message-template-upload'),

    # message define labels
    path('message-define-labels/', message_define_labels, name="message-define-labels"),
    path('message-define-label/', MessageDefineLabelsView.as_view(), name="message-define-label"),



]
