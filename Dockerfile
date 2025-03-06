FROM python:3.10-slim

# Cài đặt pdflatex và các gói LaTeX cần thiết
RUN apt-get update && apt-get install -y \
    texlive-latex-base \
    texlive-fonts-recommended \
    texlive-lang-vietnamese \
    texlive-latex-extra \
    texlive-science

# Thư mục làm việc
WORKDIR /app

# Sao chép các file requirement
COPY requirements.txt .

# Cài đặt các gói Python
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép mã nguồn ứng dụng
COPY . .

# Tạo thư mục output
RUN mkdir -p static/output && chmod 777 static/output

# Cổng ứng dụng
EXPOSE 5000

# Cài đặt biến môi trường
ENV FLASK_APP=app.py
ENV PYTHONUNBUFFERED=1
ENV PORT=5000

# Khởi chạy ứng dụng sử dụng Gunicorn
CMD gunicorn --bind 0.0.0.0:$PORT app:app
