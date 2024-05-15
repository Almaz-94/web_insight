from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponse
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, ListView, DetailView, TemplateView

from main.forms import SummaryForm
from main.models import Summary


class SummaryCreateView(LoginRequiredMixin, CreateView):
    model = Summary
    form_class = SummaryForm
    template_name = 'main/request_summary.html'

    def get_success_url(self):
        return reverse_lazy('main:summary_read', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


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


class FAQView(TemplateView):
    template_name = 'main/FAQ.html'
