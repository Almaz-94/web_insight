import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
import requests
from django.views.generic import CreateView, ListView, DetailView, TemplateView


from main.forms import SummaryForm
from main.models import Summary


class SummaryCreateView(LoginRequiredMixin, CreateView):
    model = Summary
    form_class = SummaryForm
    template_name = 'main/request_summary.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('user/')  # Replace 'login' with the name of your login URL
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('main:summary_read', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)

        data = {
            'source': 'web_app',
            'type': 'youtube_link',
            'summary_id': self.object.id,
            'user_id': self.object.user.id,
            'date': self.object.date.strftime("%d/%m/%Y, %H:%M:%S"),
            'script': self.object.script,
            'data': self.object.link,
            'user_prompt': self.object.prompt,
        }
        data = json.dumps(data)
        print(data)
        api_url = 'https://api.example.com/endpoint'
        # api_response = requests.post(api_url, json=data)
        # if api_response.status_code == 200:
        #     print('Информация успешно отправлена воркеру')
        # else:
        #     print('Произошла ошибка')
        return response


class SummaryListView(LoginRequiredMixin, ListView):
    context_object_name = 'summary_requests'
    model = Summary
    template_name = 'main/summary_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset


class SummaryDetailView(LoginRequiredMixin, DetailView):
    context_object_name = 'summary'
    model = Summary
    template_name = 'main/summary.html'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.user != self.request.user:
            raise Http404
        return self.object


class SummaryDownloadView(DetailView):
    model = Summary

    def render_to_response(self, context, **response_kwargs):
        summary_instance = self.get_object()

        text_content = summary_instance.summary

        # Create an HTTP response with the text content as a text file attachment
        response = HttpResponse(text_content, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename="{summary_instance.pk}_summary.txt"'
        return response


class FAQView(TemplateView):
    template_name = 'main/FAQ.html'
