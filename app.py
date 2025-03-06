from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
import uuid
import platform
import subprocess
import requests
import re
import os
import io
import base64
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
from flask_session import Session
from math import *
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Helper functions from original application
def get_system_info():
    # In web context, we'll use session cookies or IP-based identification
    if not session.get('user_id'):
        session['user_id'] = str(uuid.uuid4())
    return session['user_id']

def check_license(license_code):
    # For demonstration, let's assume everyone is licensed
    # In a real application, you would implement proper licensing
    return True

# Routes
@app.route('/')
def index():
    return render_template('index.html')

# Convert data routes
@app.route('/convert')
def convert():
    return render_template('convert.html')

@app.route('/convert/ex', methods=['POST'])
def convert_ex():
    text = request.form.get('text', '')
    # Logic from mathpix_to_ex
    text = text.replace('frac','dfrac')
    text = text.replace('right.','rightcham')
    text = text.replace('BON','Câu')
    text = text.replace('DPAD','Câu')
    text = text.replace('Bài','Câu')
    text = text.replace('Ví dụ','Câu')
    text = re.sub(r'(d+)',"d", text)
    text = re.sub(r'(\^\{\\prime\})','\'', text)
    text = re.sub(r'(\n+)',r'\n', text)
    text = re.sub(r'([\^\_])\{([\da-z])\}',r'\1\2', text)
    text = re.sub(r'(\\int)(\\lim)(\\min)(\\max)(\_.{1,})',r'\1\2\3\4\\limits\5', text)
    text = re.sub(r'\\mathrm\{(.*?)\}',r'\1', text)
    text = re.sub(r'([A-D]\.\s.{1,})[.,]',r'\1', text)
    text = re.sub(r'([A-D]\.\s.{1,})',r'\1.', text)
    text = re.sub(r'([A-D]\.\s)(-?[\d]{1,}[.,]?[\d]{1,})\s?\.?',r'\1$\2$.', text)
    text = re.sub(r'([A-Z\']{1,}\s)\\cdot(\s[A-Z\']{1,})',r'\1.\2', text)
    text = re.sub(r'!\[\]\(.*?\)','%Hình vẽ', text)
    text = re.sub(r'(Câu\s[\d]{1,})([.:]?)\s+\[.*?\]',r'\1.', text)
    text = re.sub(r'(Câu)(\s[\d]{1,})([.:]?)',r'\1\2.', text)
    text = re.sub(r'(Giải[.:])',r'Lời giải.', text)
    text = re.sub(r'(Lời giải[.:])',r'Lời giải.', text)
    text = re.sub(r'(Câu\s[\d]{1,}[.:]\s.{1,})',r'ketthuc\n\1', text)
    text = re.sub(r'(Câu\s[\d]{1,}[.:]\s.{1,})',r'\\begin{ex}\n\1', text)
    text = text.replace('ketthuc','\\end{ex}\n')
    text = re.sub(r'[A]\.\s(.{1,})[.,]',r'\\choice\n{\1}', text)
    text = re.sub(r'[B-D]\.\s(.{1,})[.,]',r'{\1}', text)
    text = re.sub(r'(Câu\s[\d]{1,}[.:]\s)',r'', text)
    text = text.replace('rightcham','right.')
    text +="\n\\end{ex}"
    lines = text.splitlines()
    if len(lines) > 2:
        text = '\n'.join(lines[2:])
    else:
        text = ''  
    text = re.sub(r'Lời giải\.(.*?)\\end{ex}', r'\\loigiai{\t\1}\n\\end{ex}', text, flags=re.DOTALL)
    
    # Replace the specific patterns
    patterns = [
        (re.compile(r'\\left\\{\\begin\{array\}\{\w\}(.*?)\\end\{array\}\\right\.', re.DOTALL),
         r'\\heva{\&\1}'),
        (re.compile(r'\\left\[\\begin\{array\}\{\w\}(.*?)\\end\{array\}\\right\.', re.DOTALL),
         r'\\hoac{\&\1}')
    ]
    
    def replacement(match):
        content = match.group(1)
        content = content.replace('\\\\', '\\\\&')
        if match.re.pattern == patterns[0][0].pattern:
            return f'\\heva{{&{content}}}'
        else:
            return f'\\hoac{{&{content}}}'
    
    for pattern, _ in patterns:
        text = pattern.sub(replacement, text)
    
    return jsonify({'result': text})

# Similar routes for other conversion types
@app.route('/convert/extf', methods=['POST'])
def convert_extf():
    text = request.form.get('text', '')
    # Logic similar to mathpix_to_extf
    # (Implementation similar to convert_ex but with TF-specific changes)
    return jsonify({'result': text})

@app.route('/convert/bt', methods=['POST'])
def convert_bt():
    text = request.form.get('text', '')
    # Logic similar to mathpix_to_bt
    # (Implementation similar to convert_ex but with bt-specific changes)
    return jsonify({'result': text})

@app.route('/convert/vd', methods=['POST'])
def convert_vd():
    text = request.form.get('text', '')
    # Logic similar to mathpix_to_vd
    # (Implementation similar to convert_ex but with vd-specific changes)
    return jsonify({'result': text})

@app.route('/convert/true', methods=['GET', 'POST'])
def add_true():
    if request.method == 'GET':
        return render_template('add_true.html')
    
    # Logic for adding \True command
    text = request.form.get('text', '')
    answers = request.form.get('answers', '')
    
    # Process the text similar to the AddTrue class
    # Return the processed text
    return jsonify({'result': 'Processed text'})

# Variation tables (BBT)
@app.route('/bbt')
def bbt_menu():
    return render_template('bbt_menu.html')

@app.route('/bbt/auto', methods=['GET', 'POST'])
def bbt_auto():
    if request.method == 'GET':
        return render_template('bbt_auto.html')
    
    # Process form data to generate BBT
    function_type = request.form.get('function_type')
    params = {}
    # Get parameters based on function type
    if function_type == 'linear':
        params['a'] = float(request.form.get('a', 1))
        params['b'] = float(request.form.get('b', 0))
    elif function_type == 'quadratic':
        params['a'] = float(request.form.get('a', 1))
        params['b'] = float(request.form.get('b', 0))
        params['c'] = float(request.form.get('c', 0))
    # ... other function types
    
    # Generate LaTeX code for the BBT
    latex_code = generate_bbt(function_type, params)
    
    return jsonify({'latex_code': latex_code})

def generate_bbt(function_type, params):
    # Implement BBT generation logic
    # This would be ported from the original BBT generation code
    return "\\begin{tikzpicture}\n\\tkzTabInit[nocadre,lgt=1.2,espcl=2.5]\n{$x$/0.7, $y$/2}\n{$-\\infty$, $+\\infty$}\n\\tkzTabLine{,+,}\n\\tkzTabVar{-/$-\\infty$,+/$+\\infty$}\n\\end{tikzpicture}"

@app.route('/bbt/manual', methods=['GET', 'POST'])
def bbt_manual():
    if request.method == 'GET':
        return render_template('bbt_manual.html')
    
    # Process form data to generate custom BBT
    # Return LaTeX code
    return jsonify({'latex_code': 'Custom BBT code'})

# Graph functions
@app.route('/graph')
def graph_menu():
    return render_template('graph_menu.html')

@app.route('/graph/common', methods=['GET', 'POST'])
def graph_common():
    if request.method == 'GET':
        return render_template('graph_common.html')
    
    # Process form data to generate graph
    function_type = request.form.get('function_type')
    params = {}
    # Get parameters based on function type
    
    # Generate LaTeX code for the graph
    latex_code = generate_graph(function_type, params)
    
    return jsonify({'latex_code': latex_code})

def generate_graph(function_type, params):
    # Implement graph generation logic
    return "\\begin{tikzpicture}[scale=1]\n\\draw[->] (-3,0)--(3,0) node[right]{$x$};\n\\draw[->] (0,-3)--(0,3) node[above]{$y$};\n\\draw[domain=-3:3] plot (\\x, {\\x});\n\\end{tikzpicture}"

@app.route('/graph/custom', methods=['GET', 'POST'])
def graph_custom():
    if request.method == 'GET':
        return render_template('graph_custom.html')
    
    if request.method == 'POST':
        # Get function expression
        expr = request.form.get('expr', 'x')
        xmin = float(request.form.get('xmin', -5))
        xmax = float(request.form.get('xmax', 5))
        
        # Create matplotlib plot
        plt.figure(figsize=(10, 6))
        x = np.linspace(xmin, xmax, 1000)
        try:
            # Safely evaluate the expression
            y = eval(expr, {"__builtins__": {}}, 
                    {"x": x, "sin": np.sin, "cos": np.cos, "tan": np.tan, 
                     "exp": np.exp, "log": np.log, "sqrt": np.sqrt, 
                     "pi": np.pi, "e": np.e})
            plt.plot(x, y)
            plt.grid(True)
            plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
            plt.axvline(x=0, color='k', linestyle='-', alpha=0.3)
            plt.xlabel('x')
            plt.ylabel('y')
            plt.title(f'y = {expr}')
            
            # Save plot to a bytes buffer
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            plt.close()
            
            # Encode the buffer to base64
            img_str = base64.b64encode(buf.read()).decode('utf-8')
            return jsonify({
                'success': True,
                'image': f'data:image/png;base64,{img_str}'
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            })

# Space figures
@app.route('/hkg')
def hkg_menu():
    return render_template('hkg_menu.html')

@app.route('/hkg/<figure_type>', methods=['GET', 'POST'])
def hkg_figure(figure_type):
    if request.method == 'GET':
        return render_template(f'hkg_{figure_type}.html')
    
    # Process form data to generate space figure
    params = request.form.to_dict()
    
    # Generate LaTeX code for the figure
    latex_code = generate_hkg(figure_type, params)
    
    return jsonify({'latex_code': latex_code})

def generate_hkg(figure_type, params):
    # Implement space figure generation logic based on the type
    if figure_type == 'tetrahedron':
        return "\\begin{tikzpicture}[scale=1,>=stealth]\n\\path (0,0) coordinate (A) (1,0) coordinate (B) (0.5,0.866) coordinate (C) (0.5,0.288) coordinate (D);\n\\draw (A)--(B)--(C)--cycle;\n\\draw (A)--(D)--(B);\n\\draw (C)--(D);\n\\end{tikzpicture}"
    # ... other figure types
    return "\\begin{tikzpicture}\\end{tikzpicture}"

# License verification
@app.route('/license')
def license_check():
    user_id = get_system_info()
    is_registered = check_license(user_id)
    return render_template('license.html', user_id=user_id, is_registered=is_registered)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
