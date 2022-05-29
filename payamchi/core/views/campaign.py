from django import views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import model_to_dict
from django.shortcuts import render

from ..forms.campaign import CampaignForm
from ..models import Campaign


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
            template_name='core/campaign/partials/campaign_list.html',
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

        form = CampaignForm(initial=model_to_dict(campaign))
        return render(
            request,
            template_name=self.template_name,
            context={
                'campaign': campaign,
                'form': form,
            }
        )
