from django import views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render

from ..models import ContactDefineLabel


class ContactDefineLabelAutocomplete(LoginRequiredMixin, views.View):
    def get(self, request):
        labels = list(
            ContactDefineLabel.objects.filter(
                user=self.request.user
            ).all()
        )
        return render(
            request,
            template_name='core/contacts/partials/contact_defined_labels.html',
            context={
                'labels': labels,
            }
        )

    def post(self, request):
        caption = request.POST['caption']
        contact_define_label = ContactDefineLabel.objects.create(user=request.user, caption=caption)

        return JsonResponse(model_to_dict(contact_define_label))
