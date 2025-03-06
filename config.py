"""
Cấu hình cho ứng dụng H_Latex Web
"""
import os
from dotenv import load_dotenv

# Tải biến môi trường từ file .env nếu tồn tại
load_dotenv()

class Config:
    # Cấu hình cơ bản
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard-to-guess-string'
    DEBUG = os.environ.get('FLASK_ENV') == 'development'
    
    # Thư mục đầu ra cho tệp PDF
    OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'output')
    
    # URL cho kiểm tra giấy phép
    LICENSE_URL = "https://raw.githubusercontent.com/PhucRua/HLatex/main/funny"
    
    # Giới hạn upload file
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    
    # Khóa quản trị
    ADMIN_KEY = os.environ.get('ADMIN_KEY') or 'default_admin_key'
    
    # Cấu hình cho pdflatex (nếu có)
    PDFLATEX_PATH = os.environ.get('PDFLATEX_PATH') or 'pdflatex'
