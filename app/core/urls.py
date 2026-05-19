from django.urls import path, include

urlpatterns = [
    path('', include('health.urls')), # Điều hướng tất cả request ở đường dẫn gốc vào app health
    path('', include('django_prometheus.urls')),
]