import logging
import uuid

from asgiref.sync import sync_to_async
from django.conf import settings
from django.core.exceptions import ValidationError
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView

from main.forms import SummaryForm
from main.models import Summary
from main.services import get_youtube_video_duration, get_audio_duration, start_task_from_youtube, get_s3_client, \
    start_task_from_storage

logger = logging.getLogger(__name__)


class Home(TemplateView):
    template_name = 'main/index.html'


class Home2generic(TemplateView):
    template_name = 'main/generic2.html'


class Home2elements(TemplateView):
    template_name = 'main/elements2.html'


class Home2(TemplateView):
    template_name = 'main/index2.html'


class SummaryCreateAsyncView(View):
    template_name = 'main/request_summary2.html'

    def get_context_data(self, **kwargs):
        context = kwargs
        context['ALLOWED_TIME_UNAUTH_USER'] = settings.ALLOWED_TIME_UNAUTH_USER
        return context

    async def render_async(self, request, context=None):
        if context is None:
            context = {}
        context = self.get_context_data(**context)
        return await sync_to_async(render)(request, self.template_name, context)

    async def get(self, request, *args, **kwargs):
        form = SummaryForm(user=request.user)
        context = {
            'form': form,
        }
        return await self.render_async(request, context)

    async def post(self, request, *args, **kwargs):
        if not request.session.session_key:
            await sync_to_async(request.session.create)()

        form = SummaryForm(request.POST, request.FILES, user=request.user)
        if await sync_to_async(form.is_valid)():
            summary = await self.save_form(form)
            s3_client = get_s3_client()

            if form.cleaned_data['youtube_link']:
                try:
                    await start_task_from_youtube(summary)
                except ValidationError:
                    # TODO: ERROR page
                    return redirect(reverse_lazy('main:request_summary'))

            elif form.cleaned_data['audio_file']:
                file_url = await self.handle_audio_file_upload(summary.audio_file, s3_client)
                summary.file_link_s3 = file_url
                await sync_to_async(summary.save)()
                await start_task_from_storage(summary)
            await self.update_user_time_left(request.user, form)

            return redirect(reverse_lazy('main:summary_read', kwargs={'pk': summary.pk}))
        else:
            context = {
                'form': form,
            }
            return await self.render_async(request, context)

    @sync_to_async
    def save_form(self, form):
        # summary = form.save(commit=False)
        if form.instance.pk is None:
            form.instance.unique_id = uuid.uuid4().hex
            if self.request.user.is_authenticated:
                form.instance.user = self.request.user
            else:
                form.instance.session_key = self.request.session.session_key
        # summary.save()
        # return summary
        return form.save()

    async def handle_audio_file_upload(self, audio_file, s3_client):
        temp_file_path = f'media/{audio_file.name}'

        async def upload_and_get_url():
            await s3_client.upload_file(temp_file_path)
            return await s3_client.generate_presigned_url(temp_file_path.split('/')[-1])

        return await upload_and_get_url()

    @sync_to_async
    def update_user_time_left(self, user, form):
        if not user.is_authenticated:
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
    ordering = ['-date']

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
    template_name = 'main/summary2.html'

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
    template_name = 'main/faq2.html'
