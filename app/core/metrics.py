from prometheus_client import (
    CollectorRegistry,
    Counter,
    Gauge,
    Histogram,
    Summary,
    disable_created_metrics,
)

# Tắt các metrics mặc định có hậu tố _created
disable_created_metrics()

# Khởi tạo custom registry
registry = CollectorRegistry()

http_requests_total = Counter(
    "http_requests_total",
    "Total number of HTTP requests received",
    ["status", "path", "method"],
    registry=registry,
)

active_requests_gauge = Gauge(
    "http_active_requests",
    "Number of active connections to the service",
    registry=registry,
)

latency_histogram = Histogram(
    "http_request_duration_seconds",
    "Duration of HTTP requests",
    ["status", "path", "method"],
    registry=registry,
)

posts_latency_summary = Summary(
    "post_request_duration_seconds",
    "Duration of requests to https://jsonplaceholder.typicode.com/posts",
    ["method"],
    registry=registry,
)