import os
from flask_jwt_extended import jwt_required
from utils.CommonResponse import R
from flask import Blueprint, request, send_file


case = Blueprint('case', __name__)


@case.route('/download/case_template', methods=["GET"])
# @jwt_required()
def download_case_template_file():
    cwd = os.getcwd()
    module_cwd = os.path.dirname(os.path.realpath(__file__))
    os.chdir(module_cwd)
    template_filepath = './static/case_template.xlsx'
    try:
        return send_file(template_filepath, as_attachment=True)
    except FileNotFoundError as err:
        print(f"File not found: {err}")
        return R.create(1234, "File not found") 
    finally:
        os.chdir(cwd)

@case.route('/upload', methods=['POST'])
@jwt_required()
def upload_file():
    if 'file' not in request.files:
        return R.err('No file upload')
    file = request.files['file']
    if file.filename == '' or file.filename is None:
        return R.err('No selected file')
    if file:
        file.save(os.path.join('.', file.filename))
        # TODO<2024-06-21, @xcx> 添加解析模版的代码
        return R.ok('File uploaded successfully')
