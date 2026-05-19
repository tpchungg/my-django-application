ARG PYTHON_VERSION=3.12

FROM python:${PYTHON_VERSION}-slim

WORKDIR /app

# Cài đặt thư viện dependencies trước để tối ưu hóa cache layer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ nội dung bên trong thư mục app vào WORKDIR
COPY app/ .

# Khai báo cổng lắng nghe
EXPOSE 7070

# Chạy Django Server lắng nghe ở mọi interface (0.0.0.0) trên cổng 8080
CMD ["python", "manage.py", "runserver", "0.0.0.0:7070"]