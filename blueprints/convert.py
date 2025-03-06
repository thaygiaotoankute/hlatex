"""
Blueprint cho chức năng chuyển đổi dữ liệu
"""
from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from utils.converters import mathpix_to_ex_func, mathpix_to_extf_func, mathpix_to_bt_func, mathpix_to_vd_func

convert_bp = Blueprint('convert', __name__)

@convert_bp.route('/')
def index():
    """Trang chuyển đổi dữ liệu"""
    return render_template('features/convert.html')

@convert_bp.route('/ex', methods=['GET', 'POST'])
def ex():
    """Chuyển đổi sang dạng ex"""
    if request.method == 'POST':
        text = request.form.get('text', '')
        try:
            result = mathpix_to_ex_func(text)
            return render_template('features/convert.html', 
                                   text=text, 
                                   result=result, 
                                   convert_type='ex')
        except Exception as e:
            return render_template('features/convert.html', 
                                  text=text, 
                                  error=str(e), 
                                  convert_type='ex')
    
    return render_template('features/convert.html', convert_type='ex')

@convert_bp.route('/extf', methods=['GET', 'POST'])
def extf():
    """Chuyển đổi sang dạng extf (Đúng/Sai)"""
    if request.method == 'POST':
        text = request.form.get('text', '')
        try:
            result = mathpix_to_extf_func(text)
            return render_template('features/convert.html', 
                                   text=text, 
                                   result=result, 
                                   convert_type='extf')
        except Exception as e:
            return render_template('features/convert.html', 
                                  text=text, 
                                  error=str(e), 
                                  convert_type='extf')
    
    return render_template('features/convert.html', convert_type='extf')

@convert_bp.route('/bt', methods=['GET', 'POST'])
def bt():
    """Chuyển đổi sang dạng bt"""
    if request.method == 'POST':
        text = request.form.get('text', '')
        try:
            result = mathpix_to_bt_func(text)
            return render_template('features/convert.html', 
                                   text=text, 
                                   result=result, 
                                   convert_type='bt')
        except Exception as e:
            return render_template('features/convert.html', 
                                  text=text, 
                                  error=str(e), 
                                  convert_type='bt')
    
    return render_template('features/convert.html', convert_type='bt')

@convert_bp.route('/vd', methods=['GET', 'POST'])
def vd():
    """Chuyển đổi sang dạng vd"""
    if request.method == 'POST':
        text = request.form.get('text', '')
        try:
            result = mathpix_to_vd_func(text)
            return render_template('features/convert.html', 
                                   text=text, 
                                   result=result, 
                                   convert_type='vd')
        except Exception as e:
            return render_template('features/convert.html', 
                                  text=text, 
                                  error=str(e), 
                                  convert_type='vd')
    
    return render_template('features/convert.html', convert_type='vd')

@convert_bp.route('/addtrue', methods=['GET', 'POST'])
def addtrue():
    """Thêm lệnh True"""
    if request.method == 'POST':
        text = request.form.get('text', '')
        answers = request.form.get('answers', '')
        
        try:
            # Xử lý thêm lệnh True - cần được triển khai
            result = f"Added \\True to answers: {answers} in text: {text}"
            
            return render_template('features/addtrue.html', 
                                  text=text,
                                  answers=answers,
                                  result=result)
        except Exception as e:
            return render_template('features/addtrue.html', 
                                  text=text,
                                  answers=answers,
                                  error=str(e))
    
    return render_template('features/addtrue.html')
