from django import views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import TextField, Value, IntegerField, Q
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render

from ..forms.contact import ContactForm
from ..models import Contact, ContactDefineLabel


class ContactAddView(LoginRequiredMixin, views.View):

    def get(self, request, pk=None):
        form = ContactForm
        if pk:
            contact = Contact.objects.filter(user=request.user, pk=pk).first()
            form = ContactForm(initial=model_to_dict(contact))
        return render(
            request,
            template_name='core/contacts/partials/contact_add.html',
            context={
                'form': form,
                'pk': pk
            }
        )

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            if request.POST['pk'] and request.POST['pk'] != 'None':
                contact = Contact.objects.get(pk=request.POST['pk'])
                contact.caption = form.cleaned_data['caption']
                contact.mobile = form.cleaned_data['mobile']
                contact.tel = form.cleaned_data['tel']
                contact.email = form.cleaned_data['email']
                contact.telegram_id = form.cleaned_data['telegram_id']
                contact.whatsapp_id = form.cleaned_data['whatsapp_id']
                contact.save()
            else:
                contact = Contact.objects.create(**form.cleaned_data, user=request.user)

            contact.save()
            # messages.info(request, "اطلاعات با موفقیت ذخیره شد" )
        return render(
            request,
            template_name='core/contacts/partials/contact_add.html',
            context={
                'form': form,
                # 'contact': contact
            }
        )


class ContactView(LoginRequiredMixin, views.View):

    def get(self, request, label_id: int = None):
        contact_filter = Q(
            user=request.user,
        )
        if label_id:
            contact_filter &= Q(
                labels__id=label_id
            )

        contact = Contact.objects.filter(
            contact_filter
        ).first()
        return render(
            request,
            template_name='core/contacts/contact.html',
            context={
                'contact': contact,
                'label_id': label_id,
            }
        )

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = Contact(**form.cleaned_data)
            contact.user = request.user
            contact.save()
            return render(
                request,
                template_name='core/contacts/contact.html',
                context={
                    'contact': contact
                }
            )


class ContactListView(LoginRequiredMixin, views.View):

    def get(self, request, upper):
        contact_id = request.GET.get('contact_id', None)
        if contact_id:
            contact = Contact.objects.filter(
                user=request.user,
                pk=contact_id
            ).annotate(
                latest_send_date=Value('1399/12/28 23:58', TextField()),
                count_of_receive_message=Value('12', IntegerField()),
            ).first()
            return render(
                request,
                template_name='core/contacts/partials/contact_list_item.html',
                context={
                    'contact': contact,
                }
            )
        else:
            caption = request.GET['caption']
            label_id = request.GET.get('label_id', None)
            label_id = label_id if label_id != 'None' else None
            lower = upper - 20
            contact_filter = Q(
                user=request.user,
                caption__contains=caption
            )
            if label_id:
                contact_filter &= Q(
                    labels__id=label_id
                )
            contacts = Contact.objects.filter(
                contact_filter
            ).annotate(
                latest_send_date=Value('1399/12/28 23:58', TextField()),
                count_of_receive_message=Value('12', IntegerField()),
            ).order_by('pk')[lower:upper]

            page_end = lower + contacts.count()
            count = Contact.objects.filter(
                user=request.user,
                caption__contains=caption
            ).count()

            return render(
                request,
                template_name='core/contacts/partials/contact_list.html',
                context={
                    'contacts': contacts,
                    'page_end': page_end,
                    'count': count,
                }
            )


class ContactDetailView(LoginRequiredMixin, views.View):
    template_name = 'core/contacts/partials/contact_detail.html'

    def get(self, request, pk):
        contact = Contact.objects.filter(pk=pk, user=request.user).first()
        contact_labels = contact.labels.all()
        #
        # contact_labels = ContactDefineLabel.objects.filter(
        #     user=request.user
        # ).annotate(selected=Count('contact', filter=Q(contact__id=pk))).order_by('pk')

        form = ContactForm(initial=model_to_dict(contact))
        return render(
            request,
            template_name=self.template_name,
            context={
                'contact': contact,
                'form': form,
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


def contact_define_labels(request):
    data = {
        "results": [
        ],
        "pagination": {
            "more": False
        }
    }
    if 'q' in request.GET:
        modules = ContactDefineLabel.objects.filter(
            user=request.user,
            caption__contains=request.GET.get('q', default=' ')
        ).order_by(
            "caption")[0:5]
    else:
        modules = ContactDefineLabel.objects.filter(
            user=request.user,
        ).order_by("caption")[0:5]

    if modules:
        finds = []
        if modules.count() > 5:
            data["pagination"]['more'] = True

        for item in modules:
            finds.append({
                'id': item.id,
                'text': item.caption
            })
        data["results"] = finds

    return JsonResponse(data=data)
