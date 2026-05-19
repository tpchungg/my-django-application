import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Bảo mật Key thông qua Environment Variable trong môi trường Production
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-dev-key-12345')

DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'

# Cho phép nhận request từ môi trường mạng của Cluster/Container
ALLOWED_HOSTS = ['*']

# Chỉ cài đặt các app tối thiểu cần thiết
INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'health', # Khai báo app xử lý logic
    'django_prometheus'
]

MIDDLEWARE = [
    'django_prometheus.middleware.PrometheusBeforeMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django_prometheus.middleware.PrometheusAfterMiddleware',
]

ROOT_URLCONF = 'core.urls'
WSGI_APPLICATION = 'core.wsgi.application'

# Không sử dụng Database để tối ưu hóa tài nguyên container
DATABASES = {}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_TZ = True