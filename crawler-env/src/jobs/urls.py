# jobs/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('crawl/', views.trigger_crawler, name='trigger_crawler'),
    path('', views.crawl_jobs_view, name='job_list'),
]
