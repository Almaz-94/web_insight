import asyncio
import json
import logging
import os
import tempfile

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.http import Http404, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, TemplateView


from main.forms import SummaryForm
from main.models import Summary
from main.s3 import S3Client
from main.services import get_youtube_video_duration, get_audio_duration

logger = logging.getLogger(__name__)

class SummaryCreateView(CreateView):
    model = Summary
    form_class = SummaryForm
    template_name = 'main/request_summary.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        if not request.session.session_key:
            request.session.create()
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('main:summary_read', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        user = self.get_user(form)
        response = super().form_valid(form)

        s3_client = self.get_s3_client()

        if form.cleaned_data['audio_file']:
            file_url = self.handle_audio_file_upload(form.cleaned_data['audio_file'], s3_client)
            form.instance.file_link_s3 = file_url
            form.instance.save()

        self.update_user_time_left(user, form)

        return response

    def get_user(self, form):
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
            return self.request.user
        else:
            form.instance.session_key = self.request.session.session_key
            return None

    def get_s3_client(self):
        return S3Client(
            access_key=settings.S3_ACCESS_KEY,
            secret_key=settings.S3_SECRET_KEY,
            endpoint_url=settings.S3_ENDPOINT_URL,
            bucket_name=settings.S3_BUCKET_NAME,
        )

    def handle_audio_file_upload(self, audio_file, s3_client):
        with tempfile.NamedTemporaryFile(delete=False, dir=settings.FILE_UPLOAD_TEMP_DIR) as temp_file:
            for chunk in audio_file.chunks():
                temp_file.write(chunk)
            temp_file_path = temp_file.name

        async def upload_and_get_url():
            await s3_client.upload_file(temp_file_path)
            return await s3_client.generate_presigned_url(temp_file_path.split('/')[-1])

        return asyncio.run(upload_and_get_url())

    def update_user_time_left(self, user, form):
        if not user:
            return

        if form.cleaned_data['audio_file']:
            video_length = get_audio_duration(form.cleaned_data['audio_file'])
        elif form.cleaned_data['youtube_link']:
            video_length = get_youtube_video_duration(form.cleaned_data['youtube_link'])
        else:
            raise ValidationError('Введите либо ссылку на ютуб, либо загрузите файл')

        user.time_left -= video_length
        user.save()


class SummaryListView(ListView):
    context_object_name = 'summary_requests'
    model = Summary
    template_name = 'main/summary_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            queryset = queryset.filter(user=self.request.user)
        else:
            queryset = queryset.filter(session_key=self.request.session.session_key)
        return queryset


class SummaryDetailView(DetailView):
    context_object_name = 'summary'
    model = Summary
    template_name = 'main/summary.html'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if not self.object.user:
            return self.object
        if self.object.user != self.request.user:
            raise Http404

        return self.object


class SummaryDownloadView(DetailView):
    model = Summary

    def render_to_response(self, context, **response_kwargs):
        summary_instance = self.get_object()

        text_content = summary_instance.summary

        response = HttpResponse(text_content, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename="{summary_instance.pk}_summary.txt"'
        return response


class FAQView(TemplateView):
    template_name = 'main/FAQ.html'
