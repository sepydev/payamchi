from django import views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import TextField, Value, IntegerField, Count, Q
from django.http import JsonResponse
from django.shortcuts import render

from ..models import Contact, ContactDefineLabel


class ContactView(LoginRequiredMixin, views.View):

    def get(self, request):
        contact = Contact.objects.filter(
            user=request.user
        ).first()
        return render(
            request,
            template_name='core/contacts/contact.html',
            context={
                'contact': contact
            }
        )


class ContactListView(LoginRequiredMixin, views.View):

    def get(self, request, upper):
        caption = request.GET['caption']
        lower = upper - 20
        contacts = Contact.objects.filter(
            user=request.user,
            caption__contains=caption
        ).annotate(
            latest_send_date=Value('1399/12/28 23:58', TextField()),
            count_of_receive_message=Value('12', IntegerField()),
        ).order_by('pk')[lower:upper]
        return render(
            request,
            template_name='core/contacts/partials/contact_list.html',
            context={
                'contacts': contacts
            }
        )


class ContactDetailView(LoginRequiredMixin, views.View):
    form = None
    template_name = 'core/contacts/partials/contact_detail.html'

    def get(self, request, pk):
        contact = Contact.objects.filter(pk=pk, user=request.user).first()
        contact_labels = ContactDefineLabel.objects.filter(
            user=request.user
        ).annotate(selected=Count('contact', filter=Q(contact__id=pk))).order_by('pk')
        return render(
            request,
            template_name=self.template_name,
            context={
                'contact': contact,
                'form': self.form,
                'contact_labels': contact_labels,

            }
        )


class ContactLabelsView(LoginRequiredMixin, views.View):
    form = None
    template_name = 'core/contacts/partials/contact_detail.html'

    def post(self, request):
        contact_id = request.POST['contact_id']
        label_id = request.POST['label_id']
        contact = Contact.objects.filter(
            user=request.user,
            pk=contact_id
        ).first()
        if contact:
            contact.labels.add(
                ContactDefineLabel.objects.filter(
                    id=label_id,
                    user=request.user
                ).first()
            )
            contact.save()
            return JsonResponse({'detail': 'success'})
        return JsonResponse({'detail': 'contact_id is not valid'}, status=400)

    def delete(self, request, contact_id, label_id):
        # contact_id = request.DELETE['contact_id']
        # label_id = request.DELETE['label_id']
        contact = Contact.objects.filter(
            user=request.user,
            pk=contact_id
        ).first()
        if contact:
            contact.labels.remove(
                ContactDefineLabel.objects.filter(
                    id=label_id,
                    user=request.user
                ).first()
            )
            contact.save()
            return JsonResponse({'detail': 'success'})
        return JsonResponse({'detail': 'contact_id is not valid'}, status=400)
