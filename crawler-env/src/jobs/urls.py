# jobs/urls.py

from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView

urlpatterns = [
    path('api/crawl/', views.crawl_jobs_view, name='trigger_crawler'),
    path('api/all/', views.get_all_jobs, name='get_all_jobs'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/user_jobs/', views.get_user_jobs, name='get_user_jobs'),
    path('api/user_jobs/create/', views.create_user_job, name='create_user_job'),
]