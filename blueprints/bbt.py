"""
Blueprint cho chức năng vẽ bảng biến thiên
"""
from flask import Blueprint, render_template, request, jsonify, current_app, send_from_directory
import os
import subprocess
import tempfile
import shutil
import time

bbt_bp = Blueprint('bbt', __name__)

@bbt_bp.route('/')
def index():
    """Trang chọn loại bảng biến thiên"""
    return render_template('features/bbt.html')

@bbt_bp.route('/auto', methods=['GET', 'POST'])
def auto():
    """Bảng biến thiên tự động"""
    if request.method == 'POST':
        try:
            # Lấy tham số từ form
            function_type = request.form.get('function_type', 'linear')
            
            params = {}
            if function_type == 'linear':  # Hàm bậc nhất
                params = {
                    'a': request.form.get('a', '1'),
                    'b': request.form.get('b', '0')
                }
            elif function_type == 'quadratic':  # Hàm bậc hai
                params = {
                    'a': request.form.get('a', '1'),
                    'b': request.form.get('b', '0'),
                    'c': request.form.get('c', '0')
                }
            elif function_type == 'cubic':  # Hàm bậc ba
                params = {
                    'a': request.form.get('a', '1'),
                    'b': request.form.get('b', '0'),
                    'c': request.form.get('c', '0'),
                    'd': request.form.get('d', '0')
                }
            elif function_type == 'quartic':  # Hàm trùng phương
                params = {
                    'a': request.form.get('a', '1'),
                    'b': request.form.get('b', '0'),
                    'c': request.form.get('c', '0')
                }
            elif function_type == 'rational1':  # Phân thức (ax+b)/(cx+d)
                params = {
                    'a': request.form.get('a', '1'),
                    'b': request.form.get('b', '0'),
                    'c': request.form.get('c', '1'),
                    'd': request.form.get('d', '0')
                }
            elif function_type == 'rational2':  # Phân thức (ax²+bx+c)/(mx+n)
                params = {
                    'a': request.form.get('a', '1'),
                    'b': request.form.get('b', '0'),
                    'c': request.form.get('c', '0'),
                    'm': request.form.get('m', '1'),
                    'n': request.form.get('n', '0')
                }
            
            # Tạo mã LaTeX dựa trên loại hàm và tham số
            latex_code = generate_bbt_code(function_type, params)
            
            # Render lại trang với mã LaTeX
            return render_template('features/bbt_auto.html', 
                                  function_type=function_type,
                                  params=params,
                                  latex_code=latex_code)
        
        except Exception as e:
            return render_template('features/bbt_auto.html', error=str(e))
    
    return render_template('features/bbt_auto.html')

@bbt_bp.route('/manual', methods=['GET', 'POST'])
def manual():
    """Bảng biến thiên thủ công"""
    if request.method == 'POST':
        try:
            # Xử lý dữ liệu từ form
            data = request.form.to_dict()
            latex_code = generate_manual_bbt(data)
            
            return render_template('features/bbt_manual.html', 
                                  data=data,
                                  latex_code=latex_code)
        
        except Exception as e:
            return render_template('features/bbt_manual.html', error=str(e))
    
    return render_template('features/bbt_manual.html')

@bbt_bp.route('/render', methods=['POST'])
def render_pdf():
    """Render mã LaTeX thành PDF"""
    try:
        latex_code = request.json.get('latex_code', '')
        if not latex_code:
            return jsonify({"error": "No LaTeX code provided"}), 400
        
        # Tạo file LaTeX tạm thời
        with tempfile.NamedTemporaryFile(suffix='.tex', delete=False) as f:
            temp_file = f.name
            full_latex = f"""\\documentclass{{standalone}}
\\usepackage{{amsmath,amssymb}}
\\usepackage{{tkz-tab}}
\\begin{{document}}
{latex_code}
\\end{{document}}
"""
            f.write(full_latex.encode('utf-8'))
        
        # Thư mục đầu ra
        output_dir = current_app.config['OUTPUT_DIR']
        file_name = f"bbt_{int(time.time())}"
        output_path = os.path.join(output_dir, file_name)
        
        # Chạy pdflatex
        try:
            subprocess.run([
                'pdflatex',
                '-interaction=nonstopmode',
                f'-output-directory={output_dir}',
                f'-jobname={file_name}',
                temp_file
            ], check=True)
            
            # Xóa các file tạm
            for ext in ['.aux', '.log']:
                try:
                    os.remove(os.path.join(output_dir, f"{file_name}{ext}"))
                except:
                    pass
            
            pdf_url = url_for('static', filename=f'output/{file_name}.pdf')
            return jsonify({"pdf_url": pdf_url})
            
        except subprocess.CalledProcessError as e:
            return jsonify({"error": f"PDFLaTeX error: {str(e)}"}), 500
        finally:
            # Dọn dẹp
            try:
                os.unlink(temp_file)
            except:
                pass
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def generate_bbt_code(function_type, params):
    """
    Hàm sinh mã LaTeX cho bảng biến thiên dựa trên loại hàm và tham số
    """
    # Placeholder - cần được triển khai đầy đủ
    if function_type == 'linear':
        a = float(params.get('a', 1))
        b = float(params.get('b', 0))
        
        if a == 0:
            return "Hàm số không đổi trên $\\mathbb{R}$."
        else:
            if a > 0:
                return """\\begin{tikzpicture}
\\tkzTabInit[nocadre,lgt=1.2,espcl=2.5,deltacl=0.6]
{$x$/0.6,$y'$/0.6,$y$/2}
{$-\\infty$,$+\\infty$}
\\tkzTabLine{,+,}
\\tkzTabVar{-/$-\\infty$,+/$+\\infty$}
\\end{tikzpicture}"""
            else:
                return """\\begin{tikzpicture}
\\tkzTabInit[nocadre,lgt=1.2,espcl=2.5,deltacl=0.6]
{$x$/0.6,$y'$/0.6,$y$/2}
{$-\\infty$,$+\\infty$}
\\tkzTabLine{,-,}
\\tkzTabVar{+/$+\\infty$,-/$-\\infty$}
\\end{tikzpicture}"""
    
    # Thêm code cho các loại hàm khác tương tự
    
    return "\\begin{tikzpicture}\n\\tkzTabInit[nocadre,lgt=1.2,espcl=2.5]\n{$x$/0.7, $y'$/0.7, $y$/2}\n{$-\\infty$, $0$, $+\\infty$}\n\\tkzTabLine{,+,0,-,}\n\\tkzTabVar{-/$-\\infty$,+/$y_max$,-/$-\\infty$}\n\\end{tikzpicture}"

def generate_manual_bbt(data):
    """
    Hàm sinh mã LaTeX cho bảng biến thiên thủ công dựa trên dữ liệu từ form
    """
    # Xử lý dữ liệu từ form để tạo bảng biến thiên
    # Placeholder - cần được triển khai đầy đủ
    return """\\begin{tikzpicture}
\\tkzTabInit[nocadre,lgt=1.2,espcl=2.5]
{$x$/0.7, $f'(x)$/0.7, $f(x)$/2}
{$-\\infty$, $0$, $+\\infty$}
\\tkzTabLine{,+,0,-,}
\\tkzTabVar{-/$-\\infty$,+/$0$,-/$-\\infty$}
\\end{tikzpicture}"""
