import os
from service.ParseCaseTemplate import ParseCaseTemplate
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

def is_valid_file(file):
    return '.' in file and file.rsplit('.', 1)[1].lower() in ['xlsx', 'xls']

@case.route('/upload', methods=['POST'])
@jwt_required()
def upload_file():
    if 'file' not in request.files:
        return R.err('No file upload')
    file = request.files['file']
    if file.filename == '' or file.filename is None:
        return R.err('No selected file')
    if not is_valid_file(file.filename):
        return R.err('Invalid file type')

    data = ParseCaseTemplate(file).get_data()
    print(f'data: {data}')

    # file.save(os.path.join('.', file.filename))
    # TODO<2024-06-21, @xcx> 添加解析模版的代码
    return R.ok('File uploaded successfully')
