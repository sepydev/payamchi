import contextlib

import pandas as pd
from django import forms
from django import views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import TextField, Value, IntegerField, Q
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render

from payamchi import settings
from ..forms.contact import ContactForm, ContactImportForm
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


def handle_uploaded_file(f, filename):
    with open('media/' + filename, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return filename


class ContactImport(LoginRequiredMixin, views.View):
    def post(self, request):
        try:
            if request.FILES['file']:
                file_name = handle_uploaded_file(request.FILES['file'], request.POST['filename'])
                return JsonResponse(data={
                    'file_name': file_name
                }
                )
                # return redirect('core:contact-import-select-columns', file_name=file_name)

        except Exception as identifier:
            print('error in import contact file')
            print(identifier)

    def get(self, request):
        return render(request, 'core/contacts/contact_import.html', {})


def clean_excel_cell(value: str) -> str:
    return None if str(value).lower() == 'nan' or str(value).lower() == 'None' or not str(value) else str(value)


def save_tags(contact_db, tags):
    pass


def get_cell(db_frame, cleaned_data, column):
    with contextlib.suppress(Exception):
        return clean_excel_cell(getattr(db_frame, cleaned_data[column]))
    return ''


def save_contact_item(db_frame, cleaned_data, user):
    caption = get_cell(db_frame, cleaned_data, 'caption')
    mobile = get_cell(db_frame, cleaned_data, 'mobile')
    mobile = '0' + mobile if mobile else None
    tel = get_cell(db_frame, cleaned_data, 'tel')
    tel = '0' + tel if tel else None
    email = get_cell(db_frame, cleaned_data, 'email')
    telegram_id = get_cell(db_frame, cleaned_data, 'telegram_id')
    whatsapp_id = get_cell(db_frame, cleaned_data, 'whatsapp_id')
    tags = clean_excel_cell(cleaned_data['tags'])
    if caption:
        if mobile or tel or email or telegram_id or whatsapp_id:
            contact_db = Contact.objects.filter(
                Q(user=user) &
                Q(
                    Q(caption=caption) |
                    Q(mobile=mobile)
                )
            )
            if not contact_db:
                contact_item_form = ContactForm(
                    data={
                        'caption': caption,
                        'tel': tel,
                        'mobile': mobile,
                        'email': email,
                        'telegram_id': telegram_id,
                        'whatsapp_id': whatsapp_id,
                    })
                if contact_item_form.is_valid():
                    contact_db = Contact.objects.create(
                        **contact_item_form.cleaned_data,
                        user_id=user.id
                    )

            save_tags(contact_db, tags)


class ContactImportSelectColumn(LoginRequiredMixin, views.View):
    def get(self, request, file_name):
        excel_data = pd.read_excel(
            str(settings.BASE_DIR) + '\\media\\' + file_name
        )
        columns = [('', '')]
        for col in excel_data.columns.values:
            columns.append((col, col))
        form = ContactImportForm()
        for field in form.fields:
            if type(form.fields[field]) == forms.ChoiceField:
                form.fields[field].choices = columns
        form.fields['file_name'].initial = file_name
        return render(
            request, 'core/contacts/contact_import_select_column.html',
            {
                'form': form,
            }
        )

    def post(self, request):
        form = ContactImportForm(request.POST)
        excel_data = pd.read_excel(
            str(settings.BASE_DIR) + '\\media\\' + request.POST['file_name']
        )
        columns = [('', '')]
        for col in excel_data.columns.values:
            columns.append((col, col))
        for field in form.fields:
            if type(form.fields[field]) == forms.ChoiceField:
                form.fields[field].choices = columns

        if form.is_valid():
            for db_frame in excel_data.itertuples():
                save_contact_item(db_frame, form.cleaned_data, request.user)

        return render(
            request, 'core/contacts/contact_import_select_column.html',
            {
                'form': form,
            }
        )
