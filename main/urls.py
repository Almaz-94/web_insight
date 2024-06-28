from django.urls import path

from main.apps import MainConfig
from main.views import SummaryCreateView, SummaryListView, SummaryDetailView, SummaryDownloadView, FAQView, \
    SummaryCreateAsyncView

app_name = MainConfig.name
urlpatterns = [
    path('', SummaryCreateAsyncView.as_view(), name='request_summary'),
    path('list/', SummaryListView.as_view(), name='summary_list'),
    path('summary/<int:pk>/', SummaryDetailView.as_view(), name='summary_read'),
    path('summary/<int:pk>/download/', SummaryDownloadView.as_view(), name='summary_download'),
    path('FAQ/', FAQView.as_view(), name='faq'),

]