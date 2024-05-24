# report_data/urls.py
from django.urls import path
from .views import generate_health_check_report

urlpatterns = [
    path('generate-report/', generate_health_check_report, name='generate_health_check_report'),
]
