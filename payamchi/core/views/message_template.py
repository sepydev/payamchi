import os.path
import uuid

from django import views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render

import mimetypes

mimetypes.init()


def get_extensions_for_type(general_type):
    for ext in mimetypes.types_map:
        if mimetypes.types_map[ext].split('/')[0] == general_type:
            yield ext


AUDIO = tuple(get_extensions_for_type('audio'))

from ..models import MessageTemplate, MessageTypeChoices


def handle_uploaded_file(f, user):
    if not os.path.exists(f'media/{user.id}/'):
        os.makedirs(f'media/{user.id}/')
    filename = str(uuid.uuid4())
    with open(f'media/{user.id}/' + filename, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return filename


class MessageTemplateUploadFileView(LoginRequiredMixin, views.View):
    def post(self, request):
        try:
            if request.FILES['file']:
                filename = request.POST['filename']
                file = request.FILES['file']
                ext = os.path.splitext(filename)[-1].lower()
                if ext not in AUDIO:
                    return JsonResponse(status=422, data={
                        'error': 'فایل اپلود شده بایستی از نوع صوتی باشد',
                    })
                file_name = handle_uploaded_file(file, request.user)
                request.session['file_name'] = file_name
                return JsonResponse(
                    data={
                        'url': f'/media/{request.user.id}/{file_name}',
                    }
                )

        except Exception as err:
            print(err)


class MessageTemplateView(LoginRequiredMixin, views.View):
    def post(self, request):
        file_name = request.session.get('file_name')
        caption = request.POST.get('caption')
        file_not_uploaded = False if file_name else True
        title_is_empty = False if caption else True
        if file_name and caption:
            caption = request.POST['caption']
            MessageTemplate.objects.create(
                caption=caption,
                message_type=MessageTypeChoices.VOICE.value,
                message_content=file_name,
                user_id=request.user.id
            )
        return render(
            request, 'core/message_template/message_template_add.html',
            context={
                'file_not_uploaded': file_not_uploaded,
                'title_is_empty': title_is_empty,
                'import_voice_is_loaded': True,
            }
        )

    def get(self, request):
        request.session['file_name'] = ''
        return render(request, 'core/message_template/message_template_add.html', {'import_voice_is_loaded': False})
