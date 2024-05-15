from django.urls import path

from main.apps import MainConfig
from main.views import SummaryCreateView, SummaryListView, SummaryDetailView, FAQView

app_name = MainConfig.name
urlpatterns = [
    path('', SummaryCreateView.as_view(), name='request_summary'),
    path('list/', SummaryListView.as_view(), name='summary_list'),
    path('read/<int:pk>/', SummaryDetailView.as_view(), name='summary_read'),
    path('read/<int:pk>/', SummaryDetailView.as_view(), name='summary_read'),
    path('FAQ/', FAQView.as_view(), name='faq'),

]