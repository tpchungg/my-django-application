import time
import requests
from django.http import HttpResponse, JsonResponse
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from .metrics import registry, posts_latency_summary

def hello(request):
    return HttpResponse("Hello world!")

def get_posts(request):
    start_time = time.time()

    try:
        # Gọi external API
        resp = requests.get("https://jsonplaceholder.typicode.com/posts")
        resp.raise_for_status()
        data = resp.json()
    except requests.RequestException as e:
        return HttpResponse(str(e), status=500)
    finally:
        # Ghi nhận duration vào summary metric
        duration = time.time() - start_time
        posts_latency_summary.labels(method="GET").observe(duration)

    # safe=False vì API trả về một list (mảng), không phải dict (object)
    return JsonResponse(data, safe=False)

def metrics(request):
    # Xuất metrics cho Prometheus scrape
    data = generate_latest(registry)
    return HttpResponse(data, content_type=CONTENT_TYPE_LATEST)