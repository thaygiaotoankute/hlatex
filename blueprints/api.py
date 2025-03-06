"""
API Routes cho ứng dụng H_Latex Web
"""
from flask import Blueprint, jsonify, request, current_app
import requests
import platform
import uuid
import os
import subprocess
import re
import json
from utils.license import get_system_info, get_mac_address, get_cpu_info, check_license
from utils.converters import mathpix_to_ex_func, mathpix_to_extf_func, mathpix_to_bt_func, mathpix_to_vd_func

api_bp = Blueprint('api', __name__)

@api_bp.route('/system-info', methods=['GET'])
def system_info():
    """API lấy thông tin hệ thống"""
    return jsonify({
        "system_info": get_system_info(),
        "mac_address": get_mac_address(),
        "cpu_info": get_cpu_info(),
        "os": platform.system(),
        "os_version": platform.version()
    })

@api_bp.route('/check-license', methods=['GET', 'POST'])
def check_license_api():
    """API kiểm tra giấy phép"""
    if request.method == 'POST':
        data = request.json
        license_code = data.get('license_code')
    else:
        license_code = request.args.get('license_code')
    
    if license_code:
        result = check_license(license_code)
    else:
        system_info = get_system_info()
        result = check_license(system_info)
    
    return jsonify({
        "is_registered": result,
        "system_info": get_system_info() if not license_code else None
    })

@api_bp.route('/convert', methods=['POST'])
def convert_api():
    """API chuyển đổi dữ liệu"""
    data = request.json
    if not data or not data.get('text') or not data.get('type'):
        return jsonify({"error": "Thiếu dữ liệu đầu vào"}), 400
    
    text = data.get('text')
    convert_type = data.get('type')
    
    try:
        if convert_type == 'ex':
            result = mathpix_to_ex_func(text)
        elif convert_type == 'extf':
            result = mathpix_to_extf_func(text)
        elif convert_type == 'bt':
            result = mathpix_to_bt_func(text)
        elif convert_type == 'vd':
            result = mathpix_to_vd_func(text)
        else:
            return jsonify({"error": "Loại chuyển đổi không hợp lệ"}), 400
        
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('/bbt', methods=['POST'])
def bbt_api():
    """API tạo bảng biến thiên"""
    data = request.json
    if not data or not data.get('function'):
        return jsonify({"error": "Thiếu hàm số đầu vào"}), 400
    
    function = data.get('function')
    domain = data.get('domain')
    
    try:
        # Placeholder - cần thêm mã xử lý thực tế
        bbt_result = f"BBT for function {function} with domain {domain}"
        return jsonify({"result": bbt_result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('/graph', methods=['POST'])
def graph_api():
    """API tạo đồ thị hàm số"""
    data = request.json
    if not data or not data.get('function'):
        return jsonify({"error": "Thiếu hàm số đầu vào"}), 400
    
    function = data.get('function')
    
    try:
        # Placeholder - cần thêm mã xử lý thực tế
        result = {
            "latex": f"\\{function}(x)",
            "domain": "(-\\infty, \\infty)"
        }
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('/hkg', methods=['POST'])
def hkg_api():
    """API tạo mã hình không gian"""
    data = request.json
    if not data or not data.get('type'):
        return jsonify({"error": "Thiếu loại hình không gian"}), 400
    
    hkg_type = data.get('type')
    params = data.get('params', {})
    
    try:
        # Placeholder - cần thêm mã xử lý thực tế
        result = f"HKG code for type {hkg_type} with params {params}"
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
