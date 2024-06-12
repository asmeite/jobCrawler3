# jobs/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('crawl/', views.crawl_jobs_view, name='trigger_crawler'),
     path('all/', views.get_all_jobs, name='get_all_jobs'),
]
