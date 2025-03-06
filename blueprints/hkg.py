"""
Blueprint cho chức năng hình không gian
"""
from flask import Blueprint, render_template, request, jsonify, current_app, send_from_directory
import os
import subprocess
import tempfile
import time
from utils.hkg_utils import (
    tu_dien_co_ban_func, chop_tam_giac_loai_mot_func, chop_tam_giac_loai_hai_func,
    chop_tam_giac_loai_ba_func, chop_tu_giac_loai_mot_func, chop_tu_giac_loai_hai_func,
    chop_tu_giac_loai_ba_func, lang_tru_dung_func, lang_tru_xien_func,
    hinh_hop_chu_nhat_func, hinh_hop_thuong_func, hinh_lap_phuong_func,
    khoi_non_func, khoi_tru_func, khoi_cau_func
)

hkg_bp = Blueprint('hkg', __name__)

@hkg_bp.route('/')
def index():
    """Trang chọn mẫu hình không gian"""
    return render_template('features/hkg.html')

@hkg_bp.route('/generate', methods=['POST'])
def generate():
    """Tạo mã hình không gian dựa trên loại hình và tham số"""
    try:
        hkg_type = request.form.get('hkg_type')
        params = {}
        
        # Thu thập các tham số dựa trên loại hình
        if hkg_type == 'tu_dien_co_ban':
            params = {
                'A': request.form.get('tda', 'A'),
                'B': request.form.get('tdb', 'B'),
                'C': request.form.get('tdc', 'C'),
                'D': request.form.get('tdd', 'D')
            }
            latex_code = tu_dien_co_ban_func(params['A'], params['B'], params['C'], params['D'])
            
        elif hkg_type == 'chop_tam_giac_1':
            params = {
                'S': request.form.get('tg1s', 'S'),
                'A': request.form.get('tg1a', 'A'),
                'B': request.form.get('tg1b', 'B'),
                'C': request.form.get('tg1c', 'C')
            }
            latex_code = chop_tam_giac_loai_mot_func(params['S'], params['A'], params['B'], params['C'])
            
        elif hkg_type == 'chop_tam_giac_2':
            params = {
                'S': request.form.get('tg2s', 'S'),
                'A': request.form.get('tg2a', 'A'),
                'B': request.form.get('tg2b', 'B'),
                'C': request.form.get('tg2c', 'C'),
                'G': request.form.get('tg2g', 'G'),
                'M': request.form.get('tg2m', 'M')
            }
            latex_code = chop_tam_giac_loai_hai_func(params['S'], params['A'], params['B'], params['C'], params['G'], params['M'])
            
        elif hkg_type == 'chop_tam_giac_3':
            params = {
                'S': request.form.get('tg3s', 'S'),
                'A': request.form.get('tg3a', 'A'),
                'B': request.form.get('tg3b', 'B'),
                'C': request.form.get('tg3c', 'C'),
                'H': request.form.get('tg3h', 'H')
            }
            latex_code = chop_tam_giac_loai_ba_func(params['S'], params['A'], params['B'], params['C'], params['H'])
            
        elif hkg_type == 'chop_tu_giac_1':
            params = {
                'S': request.form.get('tug1s', 'S'),
                'A': request.form.get('tug1a', 'A'),
                'B': request.form.get('tug1b', 'B'),
                'C': request.form.get('tug1c', 'C'),
                'D': request.form.get('tug1d', 'D')
            }
            latex_code = chop_tu_giac_loai_mot_func(params['S'], params['A'], params['B'], params['C'], params['D'])
            
        elif hkg_type == 'chop_tu_giac_2':
            params = {
                'S': request.form.get('tug2s', 'S'),
                'A': request.form.get('tug2a', 'A'),
                'B': request.form.get('tug2b', 'B'),
                'C': request.form.get('tug2c', 'C'),
                'D': request.form.get('tug2d', 'D'),
                'G': request.form.get('tug2g', 'G')
            }
            latex_code = chop_tu_giac_loai_hai_func(params['S'], params['A'], params['B'], params['C'], params['D'], params['G'])
            
        elif hkg_type == 'chop_tu_giac_3':
            params = {
                'S': request.form.get('tug3s', 'S'),
                'A': request.form.get('tug3a', 'A'),
                'B': request.form.get('tug3b', 'B'),
                'C': request.form.get('tug3c', 'C'),
                'D': request.form.get('tug3d', 'D'),
                'H': request.form.get('tug3h', 'H')
            }
            latex_code = chop_tu_giac_loai_ba_func(params['S'], params['A'], params['B'], params['C'], params['D'], params['H'])
            
        elif hkg_type == 'lang_tru_dung':
            params = {
                'M': request.form.get('lt1m', 'M'),
                'N': request.form.get('lt1n', 'N'),
                'P': request.form.get('lt1p', 'P'),
                'A': request.form.get('lt1a', 'A'),
                'B': request.form.get('lt1b', 'B'),
                'C': request.form.get('lt1c', 'C')
            }
            latex_code = lang_tru_dung_func(params['A'], params['B'], params['C'], params['M'], params['N'], params['P'])
            
        elif hkg_type == 'lang_tru_xien':
            params = {
                'M': request.form.get('lt2m', 'M'),
                'N': request.form.get('lt2n', 'N'),
                'P': request.form.get('lt2p', 'P'),
                'A': request.form.get('lt2a', 'A'),
                'B': request.form.get('lt2b', 'B'),
                'C': request.form.get('lt2c', 'C')
            }
            latex_code = lang_tru_xien_func(params['A'], params['B'], params['C'], params['M'], params['N'], params['P'])
            
        elif hkg_type == 'hinh_hop_chu_nhat':
            params = {
                'M': request.form.get('hh1m', 'M'),
                'N': request.form.get('hh1n', 'N'),
                'P': request.form.get('hh1p', 'P'),
                'Q': request.form.get('hh1q', 'Q'),
                'A': request.form.get('hh1a', 'A'),
                'B': request.form.get('hh1b', 'B'),
                'C': request.form.get('hh1c', 'C'),
                'D': request.form.get('hh1d', 'D')
            }
            latex_code = hinh_hop_chu_nhat_func(params['A'], params['B'], params['C'], params['D'], params['M'], params['N'], params['P'], params['Q'])
            
        elif hkg_type == 'hinh_hop_thuong':
            params = {
                'M': request.form.get('hh2m', 'M'),
                'N': request.form.get('hh2n', 'N'),
                'P': request.form.get('hh2p', 'P'),
                'Q': request.form.get('hh2q', 'Q'),
                'A': request.form.get('hh2a', 'A'),
                'B': request.form.get('hh2b', 'B'),
                'C': request.form.get('hh2c', 'C'),
                'D': request.form.get('hh2d', 'D')
            }
            latex_code = hinh_hop_thuong_func(params['A'], params['B'], params['C'], params['D'], params['M'], params['N'], params['P'], params['Q'])
            
        elif hkg_type == 'hinh_lap_phuong':
            params = {
                'M': request.form.get('hh3m', 'M'),
                'N': request.form.get('hh3n', 'N'),
                'P': request.form.get('hh3p', 'P'),
                'Q': request.form.get('hh3q', 'Q'),
                'A': request.form.get('hh3a', 'A'),
                'B': request.form.get('hh3b', 'B'),
                'C': request.form.get('hh3c', 'C'),
                'D': request.form.get('hh3d', 'D')
            }
            latex_code = hinh_lap_phuong_func(params['A'], params['B'], params['C'], params['D'], params['M'], params['N'], params['P'], params['Q'])
            
        elif hkg_type == 'khoi_non':
            params = {
                'R': request.form.get('hnr', '1'),
                'h': request.form.get('hnh', '3')
            }
            latex_code = khoi_non_func(params['R'], params['h'])
            
        elif hkg_type == 'khoi_tru':
            params = {
                'R': request.form.get('htr', '1'),
                'h': request.form.get('hth', '3')
            }
            latex_code = khoi_tru_func(params['R'], params['h'])
            
        elif hkg_type == 'khoi_cau':
            params = {
                'R': request.form.get('hcr', '1')
            }
            latex_code = khoi_cau_func(params['R'])
            
        else:
            return jsonify({"error": "Invalid type"}), 400
        
        return render_template('features/hkg_result.html', 
                               hkg_type=hkg_type, 
                               params=params, 
                               latex_code=latex_code)
        
    except Exception as e:
        return render_template('features/hkg.html', error=str(e))

@hkg_bp.route('/render', methods=['POST'])
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
\\usepackage{{tikz}}
\\usetikzlibrary{{shapes,arrows,calc}}
\\begin{{document}}
{latex_code}
\\end{{document}}
"""
            f.write(full_latex.encode('utf-8'))
        
        # Thư mục đầu ra
        output_dir = current_app.config['OUTPUT_DIR']
        file_name = f"hkg_{int(time.time())}"
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
