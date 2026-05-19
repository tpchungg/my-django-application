from django.urls import path
from . import views

urlpatterns = [
    path('', views.healthcheck, name='healthcheck'), # Điểm cuối (Endpoint) khớp với đường dẫn gốc "/"
]