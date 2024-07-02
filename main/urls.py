from django.urls import path

from main.apps import MainConfig
from main.views import SummaryCreateView, SummaryListView, SummaryDetailView, SummaryDownloadView, FAQView, \
    SummaryCreateAsyncView, Home, Home2, Home2generic, Home2elements

app_name = MainConfig.name
urlpatterns = [
    path('', SummaryCreateAsyncView.as_view(), name='request_summary'),
    path('list/', SummaryListView.as_view(), name='summary_list'),
    path('summary/<int:pk>/', SummaryDetailView.as_view(), name='summary_read'),
    path('summary/<int:pk>/download/', SummaryDownloadView.as_view(), name='summary_download'),
    path('FAQ/', FAQView.as_view(), name='faq'),
    path('home/', Home.as_view(), name='home'),
    path('home2/', Home2.as_view(), name='home2'),
    path('home2generic/', Home2generic.as_view(), name='home2generic'),
    path('home2elements/', Home2elements.as_view(), name='home2elements'),

]