"""
Blueprint chính cho ứng dụng H_Latex Web
"""
from flask import Blueprint, render_template, redirect, url_for, current_app, request

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Trang chủ"""
    return render_template('index.html')

@main_bp.route('/about')
def about():
    """Trang giới thiệu"""
    return render_template('about.html')

@main_bp.route('/license')
def license():
    """Trang kiểm tra giấy phép"""
    return render_template('license.html')

@main_bp.route('/admin')
def admin():
    """Trang quản trị"""
    admin_key = request.args.get('key')
    if not admin_key or admin_key != current_app.config['ADMIN_KEY']:
        return redirect(url_for('main.index'))
    
    return render_template('admin.html')
