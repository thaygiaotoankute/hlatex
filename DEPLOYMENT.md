# Hướng dẫn triển khai H_Latex Web

Tài liệu này hướng dẫn cách triển khai ứng dụng H_Latex Web lên các nền tảng khác nhau.

## 1. Triển khai lên Render.com

### 1.1. Đăng ký tài khoản Render.com

1. Truy cập https://render.com/
2. Đăng ký tài khoản mới hoặc đăng nhập bằng GitHub

### 1.2. Tạo dịch vụ Web mới

1. Từ Dashboard, nhấn vào "New" và chọn "Web Service"
2. Kết nối với repository GitHub của bạn
3. Điền thông tin dịch vụ:
   - Tên: H_Latex-Web
   - Runtime: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
4. Chọn gói (Free hoặc trả phí)
5. Thiết lập các biến môi trường:
   - `SECRET_KEY`: Chuỗi bí mật để bảo mật ứng dụng
   - `ADMIN_KEY`: Khóa để truy cập trang quản trị
   - `FLASK_ENV`: development hoặc production
6. Nhấn "Create Web Service"

## 2. Triển khai bằng Docker

### 2.1. Build Docker Image

```bash
# Tại thư mục dự án
docker build -t hlatex-web .
```

### 2.2. Chạy Docker Container

```bash
docker run -p 5000:5000 -e SECRET_KEY="your_secret_key" -e ADMIN_KEY="your_admin_key" -d hlatex-web
```

### 2.3. Triển khai trên Docker Compose

Tạo file `docker-compose.yml`:

```yaml
version: '3'
services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - SECRET_KEY=your_secret_key
      - ADMIN_KEY=your_admin_key
      - FLASK_ENV=production
    volumes:
      - ./static/output:/app/static/output
```

Chạy Docker Compose:

```bash
docker-compose up -d
```

## 3. Triển khai trên VPS/Máy chủ riêng

### 3.1. Cài đặt các phụ thuộc

```bash
# Cài đặt Python và pip
sudo apt update
sudo apt install python3 python3-pip

# Cài đặt pdflatex và các gói LaTeX cần thiết
sudo apt install texlive-latex-base texlive-fonts-recommended texlive-lang-vietnamese texlive-latex-extra texlive-science

# Cài đặt các gói Python
pip install -r requirements.txt
```

### 3.2. Cấu hình Nginx (tùy chọn)

```bash
# Cài đặt Nginx
sudo apt install nginx

# Tạo file cấu hình Nginx
sudo nano /etc/nginx/sites-available/hlatex

# Thêm nội dung sau:
server {
    listen 80;
    server_name your_domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# Kích hoạt cấu hình
