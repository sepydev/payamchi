import datetime
from django import views
from django import forms
from django.forms import model_to_dict
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from ..forms.message import MessageForm
from ..models import Message, Campaign, MessageTypeChoices


class MessageAddView(LoginRequiredMixin, views.View):
    def get(self, request, pk=None):
        form = MessageForm(request.user)
        if pk:
            message = Message.objects.filter(user=request.user, pk=pk).first()
            form = MessageForm(request.user, initial=model_to_dict(message))
        return render(
            request,
            template_name='core/messages/partials/message_add.html',
            context={
                'form': form,
                'pk': pk,
            }
        )

    def post(self, request):
        form = MessageForm(request.user, request.POST)
        if form.is_valid():
            message = Message.objects.create(**form.cleaned_data, user=request.user)
            message.save()
        return render(
            request,
            template_name='core/messages/partials/message_add.html',
            context={
                'form': form,
            }
        )
