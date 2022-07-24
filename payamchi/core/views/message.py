import datetime

from django import views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import model_to_dict
from django.shortcuts import render

from ..forms.message import MessageFormPartially, MessageForm, MessageDetailForm
from ..models import Message, MessageStatusChoices


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
        return render(
            request,
            template_name='core/message/partials/message_detail.html',
            context={
                'message': message,
                'message_status': MessageStatusChoices.choices,
                'form': form,
            }
        )
