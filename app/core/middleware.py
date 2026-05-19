import time
import random
from .metrics import (
    active_requests_gauge,
    http_requests_total,
    latency_histogram,
)

class PrometheusMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        delay = random.uniform(0.5, 2)
        time.sleep(delay)

        active_requests_gauge.inc()
        start_time = time.time()

        # Chuyển request tới View xử lý
        response = self.get_response(request)

        # --- Tương đương @app.after_request ---
        active_requests_gauge.dec()
        duration = time.time() - start_time

        # Ghi nhận các metrics
        status_code = str(response.status_code)
        
        http_requests_total.labels(
            status=status_code, path=request.path, method=request.method
        ).inc()

        latency_histogram.labels(
            status=status_code, path=request.path, method=request.method
        ).observe(duration)

        return response