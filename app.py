"""
H_Latex Web Application
Chuyển đổi từ ứng dụng desktop PyQt6 sang ứng dụng web Flask
"""
from flask import Flask, render_template, redirect, url_for
from flask_cors import CORS
import os
from blueprints.main import main_bp
from blueprints.api import api_bp
from blueprints.convert import convert_bp
from blueprints.bbt import bbt_bp
from blueprints.graph import graph_bp
from blueprints.hkg import hkg_bp
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Đăng ký các blueprint
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(convert_bp, url_prefix='/convert')
    app.register_blueprint(bbt_bp, url_prefix='/bbt')
    app.register_blueprint(graph_bp, url_prefix='/graph')
    app.register_blueprint(hkg_bp, url_prefix='/hkg')
    
    # Cấu hình CORS
    CORS(app)
    
    # Đảm bảo thư mục output tồn tại
    os.makedirs(app.config['OUTPUT_DIR'], exist_ok=True)
    
    # Cấu hình xử lý lỗi
    register_error_handlers(app)
    
    return app

def register_error_handlers(app):
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=app.config['DEBUG'])
