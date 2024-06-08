import json
import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, TemplateView


from main.forms import SummaryForm
from main.models import Summary
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
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
            user = self.request.user
        else:
            form.instance.session_key = self.request.session.session_key
            user = None
        response = super().form_valid(form)

        if user and form.cleaned_data['audio_file']:
            video_length = get_audio_duration(form.cleaned_data['audio_file'])
            user.time_left -= video_length
            user.save()
        elif user and form.cleaned_data['youtube_link']:
            video_length = get_youtube_video_duration(form.cleaned_data['youtube_link'])
            user.time_left -= video_length
            user.save()
        return response


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
