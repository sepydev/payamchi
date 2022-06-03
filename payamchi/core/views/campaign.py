import datetime

from django import views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q, F, Sum
from django.forms.models import model_to_dict
from django.shortcuts import render

from ..forms.campaign import CampaignForm
from ..models import Campaign, MessageTypeChoices, Message
from ..models.message_receiver import MessageReceiverStatusChoices


class CampaignAddView(LoginRequiredMixin, views.View):

    def get(self, request, pk=None):
        form = CampaignForm
        if pk:
            campaign = Campaign.objects.filter(user=request.user, pk=pk).first()
            form = CampaignForm(initial=model_to_dict(campaign))
        return render(
            request,
            template_name='core/campaign/partials/campaign_add.html',
            context={
                'form': form,
                'pk': pk
            }
        )

    def post(self, request):
        form = CampaignForm(request.POST)
        if form.is_valid():
            if request.POST['pk'] and request.POST['pk'] != 'None':
                campaign = Campaign.objects.get(pk=request.POST['pk'])
                campaign.caption = form.cleaned_data['caption']
                campaign.start_date = form.cleaned_data['start_date']
                campaign.end_date = form.cleaned_data['end_date']
                campaign.description = form.cleaned_data['description']
                campaign.save()
            else:
                data = form.cleaned_data
                data.pop('start_date_persian')
                data.pop('end_date_persian')
                campaign = Campaign.objects.create(**form.cleaned_data, user=request.user)
                campaign.save()
        return render(
            request,
            template_name='core/campaign/partials/campaign_add.html',
            context={
                'form': form,
            }
        )


class CampaignView(LoginRequiredMixin, views.View):

    def get(self, request):
        campaign = Campaign.objects.filter(
            user=request.user
        ).first()
        return render(
            request,
            template_name='core/campaign/campaign.html',
            context={
                'campaign': campaign
            }
        )


class CampaignListView(LoginRequiredMixin, views.View):

    def get(self, request, upper):
        campaign_id = request.GET.get('campaign_id', None)
        if campaign_id:
            template_name = 'core/campaign/partials/campaign_list_item.html'
            campaign = Campaign.objects.filter(
                user=request.user,
                pk=campaign_id
            ).first()
            return render(
                request,
                template_name=template_name,
                context={
                    'campaign': campaign,
                }
            )
        else:
            template_name = 'core/campaign/partials/campaign_list.html'
            caption = request.GET['caption']
            lower = upper - 10
            campaigns = Campaign.objects.filter(
                user=request.user,
                caption__contains=caption
            ).order_by('pk')[lower:upper]

            page_end = lower + campaigns.count()
            count = Campaign.objects.filter(
                user=request.user,
                caption__contains=caption
            ).count()

            return render(
                request,
                template_name=template_name,
                context={
                    'campaigns': campaigns,
                    'page_end': page_end,
                    'count': count,
                }
            )


class CampaignDetailView(LoginRequiredMixin, views.View):
    template_name = 'core/campaign/partials/campaign_detail.html'

    def get(self, request, pk):
        campaign = Campaign.objects.filter(pk=pk, user=request.user).first()
        message_cost = Message.objects.filter(
            campaign_id=pk, campaign__user=request.user
        ).aggregate(
            cost=Sum('cost'),
        )
        messages_count = Message.objects.filter(
            campaign_id=pk, campaign__user=request.user
        ).aggregate(
            total=Count('messagereceiver'),
            successful=Count(
                expression='messagereceiver',
                filter=Q(
                    messagereceiver__status=MessageReceiverStatusChoices.SUCCESSFUL.value,
                )
            ),
            unsuccessful=Count(
                expression='messagereceiver',
                filter=Q(
                    messagereceiver__status=MessageReceiverStatusChoices.UNSUCCESSFUL.value,
                )
            ),
            undefined=Count(
                expression='messagereceiver',
                filter=Q(
                    messagereceiver__status=MessageReceiverStatusChoices.UNDEFINED.value,
                )
            ),

        )

        form = CampaignForm(initial=model_to_dict(campaign))
        return render(
            request,
            template_name=self.template_name,
            context={
                'campaign': campaign,
                'form': form,
                'message_types': MessageTypeChoices.choices,
                'messages_count': messages_count,
                'message_cost': message_cost
            }
        )


class CampaignMessages(LoginRequiredMixin, views.View):
    template_name = 'core/campaign/partials/campaign_messages.html'

    def get(self, request):
        campaign_id = request.GET['campaign_id']
        message_type = request.GET.get('message_type', '')
        from_date = request.GET.get('from_date', '')
        to_date = request.GET.get('to_date', '')
        _filter = Q(
            campaign__user=request.user,
            campaign_id=campaign_id,
        )
        if message_type:
            _filter &= Q(message_type=message_type)
        if from_date and to_date:
            _filter &= Q(send_date__gte=from_date, send_date__lte=to_date)

        messages = Message.objects.filter(
            _filter
        ).annotate(
            total=Count('messagereceiver'),
            successful=Count(
                expression='messagereceiver',
                filter=Q(
                    messagereceiver__status=MessageReceiverStatusChoices.SUCCESSFUL.value,
                )
            ),
            unsuccessful=Count(
                expression='messagereceiver',
                filter=Q(
                    messagereceiver__status=MessageReceiverStatusChoices.UNSUCCESSFUL.value,
                )
            ),
            undefined=Count(
                expression='messagereceiver',
                filter=Q(
                    messagereceiver__status=MessageReceiverStatusChoices.UNDEFINED.value,
                )
            ),
            send_date_only=F('send_date__date'),
        ).order_by('-pk')

        # messages = messages.values()

        # for message in messages:
        #     if message["send_date"].timestamp() < datetime.datetime.now().timestamp():
        #         message['text_class'] = 'danger'
        #     elif message["send_date"].date() == datetime.date.today():
        #         message['text_class'] = 'warning'
        #     else:
        #         message['text_class'] = 'success'

        return render(
            request,
            template_name=self.template_name,
            context={
                'messages': messages,
                'today': datetime.date.today(),

            }
        )
