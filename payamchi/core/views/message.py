import datetime
from contextlib import suppress

from django import views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q, F
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render

from ..forms.message import MessageFormPartially, MessageForm, MessageDetailForm
from ..models import Message, MessageStatusChoices, MessageDefineLabel, ContactDefineLabel, MessageReceiver, Contact


class MessageAddPartiallyView(LoginRequiredMixin, views.View):
    def get(self, request, pk=None):
        form = MessageFormPartially(request.user)
        if pk:
            message = Message.objects.filter(user=request.user, pk=pk).first()
            form = MessageFormPartially(request.user, initial=model_to_dict(message))
        return render(
            request,
            template_name='core/message/partials/message_add_partially.html',
            context={
                'form': form,
                'pk': pk,
            }
        )

    def post(self, request):
        form = MessageFormPartially(request.user, request.POST)
        if form.is_valid():
            message = Message.objects.create(
                **form.cleaned_data,
                user=request.user,
                send_date=datetime.datetime.now(),
                cost=0,
                effort=3,
            )
            message.save()
        return render(
            request,
            template_name='core/message/partials/message_add_partially.html',
            context={
                'form': form,
            }
        )


class MessageAddView(LoginRequiredMixin, views.View):
    def get(self, request, pk=None, message_type=None, campaign=None):
        form = MessageForm(request.user,
                           initial={
                               'message_type': message_type,
                               'campaign': campaign,
                           })
        if pk:
            message = Message.objects.filter(user=request.user, pk=pk).first()
            form = MessageForm(request.user, initial=model_to_dict(message))
        return render(
            request,
            template_name='core/message/partials/message_add.html',
            context={
                'form': form,
                'pk': pk,
            }
        )

    def post(self, request):
        form = MessageForm(request.user, request.POST)
        if form.is_valid():
            message = Message.objects.create(
                **form.cleaned_data,
                user=request.user,
                send_date=datetime.datetime.now(),
                cost=0,
                effort=3,
            )
            message.save()
        return render(
            request,
            template_name='core/message/partials/message_add.html',
            context={
                'form': form,
            }
        )


class MessageView(LoginRequiredMixin, views.View):

    def get(self, request):
        message = Message.objects.filter(
            user=request.user
        ).first()
        return render(
            request,
            template_name='core/message/message.html',
            context={
                'message': message
            }
        )


class MessageListView(LoginRequiredMixin, views.View):

    def get(self, request, upper):
        message_id = request.GET.get('message_id', None)
        if message_id:
            message = Message.objects.filter(
                user=request.user,
                pk=message_id,
            ).first()
            return render(
                request,
                template_name='core/message/partials/message_list_item.html',
                context={
                    'message': message,
                }
            )
        else:
            caption = request.GET['caption']
            lower = upper - 10
            messages = Message.objects.filter(
                caption__contains=caption,
                user=request.user,
            ).order_by('pk')[lower:upper]
            page_end = lower + messages.count()
            count = Message.objects.filter(
                caption__contains=caption,
                user=request.user,
            ).count()

            return render(
                request,
                template_name='core/message/partials/message_list.html',
                context={
                    'messages': messages,
                    'page_end': page_end,
                    'count': count,
                }
            )


def get_contact_types(user, message):
    message_length = 0
    with suppress(Exception):
        message_length = message.message_template.message_length

    mobile_statistic = Contact.objects.filter(
        messagereceiver__message=message,
        user=user,
        mobile__isnull=False
    ).count()
    tel_statistic = Contact.objects.filter(
        messagereceiver__message=message,
        user=user,
        tel__isnull=False
    ).count()

    return [
        {
            'title': 'موبایل',
            'count': mobile_statistic,
            'unit_price': 0,
            'message_length': message_length,
            'cost': 0,
        },
        {
            'title': 'تلفن',
            'count': tel_statistic,
            'unit_price': 0,
            'message_length': message_length,
            'cost': 0,
        }
    ]


class MessageDetailView(LoginRequiredMixin, views.View):
    def get(self, request, pk):
        message = Message.objects.filter(
            pk=pk,
            user=request.user
        ).first()
        form = MessageDetailForm(
            user=request.user,
            initial=model_to_dict(message)
        )
        contact_types = get_contact_types(request.user, message)
        return render(
            request,
            template_name='core/message/partials/message_detail.html',
            context={
                'message': message,
                'message_status': MessageStatusChoices.choices,
                'form': form,
                'message_labels': message.labels.all(),
                'contact_labels': message.contact_labels.all(),
                'contact_types': contact_types,
            }
        )

    def post(self, request, pk):
        form = MessageDetailForm(request.user, request.POST)
        message = Message.objects.filter(pk=pk, user=request.user)
        contact_labels = request.POST.get('contact_labels', '').split(',')
        message_labels = request.POST.get('message_labels', '').split(',')
        new_message_labels = request.POST.get('new_message_labels', '').split(',')

        if form.is_valid():
            self.save_message(form, message)
            self.save_message_labels(request, message, message_labels, new_message_labels)
            self.save_contact_labels(contact_labels, message)
            self.save_message_receivers(request, message)
            self.save_cost(message)

        contact_types = get_contact_types(request.user, message.first())
        return render(
            request,
            template_name='core/message/partials/message_detail.html',
            context={
                'message': message.first(),
                'message_status': MessageStatusChoices.choices,
                'form': form,
                'message_labels': message.first().labels.all(),
                'contact_labels': message.first().contact_labels.all(),
                'contact_types': contact_types,
            }
        )

    @staticmethod
    def save_cost(message):
        count_of_receivers = MessageReceiver.objects.filter(message=message.first()).count()
        message_length = message.first().message_template.message_length
        # Todo : cost is not completely calculated.
        cost = count_of_receivers * message_length
        message.update(cost=cost)

    @staticmethod
    def save_message_receivers(request, message):
        MessageReceiver.objects.filter(message=message.first(), user=request.user).delete()
        contacts = Contact.objects.filter(labels__message=message.first())
        for contact in contacts:
            MessageReceiver.objects.create(
                user=request.user,
                message=message.first(),
                contact=contact
            )

    @staticmethod
    def save_message(form, message):
        cleaned_data = form.cleaned_data
        cleaned_data.pop('send_date_persian')
        message.update(
            **form.cleaned_data,
        )

    @staticmethod
    def save_message_labels(request, message, message_labels, new_message_labels):
        message.first().labels.through.objects.all().delete()
        message.first().save()
        if message_labels:
            for message_label in message_labels:
                if message_label and int(message_label) > 0:
                    message_db = MessageDefineLabel.objects.filter(pk=message_label, user=request.user).first()
                    if message_db:
                        message.first().labels.add(message_db)
            message.first().save()
        if new_message_labels:
            for new_message_label in new_message_labels:
                if new_message_label:
                    message_db = MessageDefineLabel.objects.filter(caption=new_message_label.trim(),
                                                                   user=request.user).first()
                    if not message_db:
                        message_db = MessageDefineLabel.objects.create(caption=new_message_label.trim,
                                                                       user=request.user)
                        message.first().labels.add(message_db)
            message.first().save()

    @staticmethod
    def save_contact_labels(contact_labels, message):
        message.first().contact_labels.through.objects.all().delete()
        if contact_labels:
            for contact_label in contact_labels:
                if contact_label and int(contact_label) > 0:
                    contact_label_db = ContactDefineLabel.objects.filter(pk=contact_label).first()
                    if contact_label_db:
                        message.first().contact_labels.add(contact_label_db)
            message.first().save()


class MessageDetailChartView(LoginRequiredMixin, views.View):
    def get(self, request, pk):
        message = Message.objects.filter(
            pk=pk,
            user=request.user
        ).first()
        mobile_count = Contact.objects.filter(
            messagereceiver__message=message,
            user=request.user,
            mobile__isnull=False
        ).count()
        tel_count = Contact.objects.filter(
            messagereceiver__message=message,
            user=request.user,
            tel__isnull=False
        ).count()
        total = Contact.objects.filter(
            messagereceiver__message=message,
            user=request.user,
        ).count()
        valid_numbers = mobile_count + tel_count

        return JsonResponse(
            {
                'mobile_count': mobile_count,
                'tel_count': tel_count,
                'total': total,
                'valid_numbers': valid_numbers,
                'invalid_numbers': total - valid_numbers,

            }
        )
