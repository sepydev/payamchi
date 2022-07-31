from django import views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render

from ..models import MessageDefineLabel


class MessageDefineLabelsView(LoginRequiredMixin, views.View):
    def get(self, request):
        labels = list(
            MessageDefineLabel.objects.filter(
                user=self.request.user
            ).all()
        )
        return render(
            request,
            template_name='core/message/partials/message_defined_labels.html',
            context={
                'labels': labels,
            }
        )

    def post(self, request):
        caption = request.POST['caption']
        contact_define_label = MessageDefineLabel.objects.create(user=request.user, caption=caption)

        return JsonResponse(model_to_dict(contact_define_label))


def message_define_labels(request):
    data = {
        "results": [
        ],
        "pagination": {
            "more": False
        }
    }
    if 'q' in request.GET:
        modules = MessageDefineLabel.objects.filter(
            user=request.user,
            caption__contains=request.GET.get('q', default=' ')
        ).order_by(
            "caption")[0:5]
    else:
        modules = MessageDefineLabel.objects.filter(
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
