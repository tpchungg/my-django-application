import time
from django.http import JsonResponse

# Biến static lưu thời điểm container bắt đầu chạy
START_TIME = time.time()

def healthcheck(request):
    if request.method == 'GET':
        uptime = time.time() - START_TIME
        return JsonResponse({
            "uptime": uptime,
            "message": "OK",
            "timestamp": time.time()
        }, status=200)