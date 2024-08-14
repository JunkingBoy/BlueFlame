'''
Author: Lucifer
Data: Do not edit
LastEditors: Lucifer
LastEditTime: 2024-08-15 04:04:08
Description: 
'''
from flask_jwt_extended import jwt_required
from flask import Blueprint, request, send_file, current_app
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from typing import List

from utils.CommonResponse import R
from service.CaseService import CaseService
from service.UserService import get_user_id
from service.CaseProcessing import parse_process
from utils.ExcelExtract import parse_case_template_excel
from utils.CaseDb import CaseDbTemplate

bp = Blueprint('case_parse', __name__)


@bp.route('/download/case_template/<string:temp_type>', methods=["GET"])
@jwt_required()
def download_case_template_file(temp_type: str):
    if temp_type == 'func':
        file = './static/func_case_template.xlsx'
    elif temp_type == 'api':
        file = './static/api_case_template.xlsx'
    else:
        return R.err('Invalid template type')
    
    try:
        file_name: str = secure_filename(file)
        return send_file(
            file,
            as_attachment=True,
            mimetype=
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            download_name=f"{file_name}")
    except FileNotFoundError as err:
        current_app.logger.error(f"Can not found file: {err}", exc_info=True)
        return R.create(404, "File not found")
    except Exception as err:
        current_app.logger.error(f"Error occurred: {err}", exc_info=True)
        return R.create(500, "Internal server error")

def is_valid_file(file):
    return '.' in file and file.rsplit('.', 1)[1].lower() in ['xlsx', 'xls']


@bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_file():
    type: int = 0

    if 'file' not in request.files:
        return R.err(f'No file upload')
    if 'type' not in request.form:
        return R.err(f'Missing required parameter: type')
    if 'project_id' not in request.form:
        return R.err(f'Missing required parameter: project_id')

    case_type: str = request.form['type']
    project_id: str = request.form['project_id']
    user_id: str = get_user_id()
    file: FileStorage = request.files['file']
    if file.filename == '' or file.filename is None:
        return R.err('No selected file')
    if not is_valid_file(file.filename):
        return R.err('Invalid file type')
    
    if case_type == 'api_case':
        type = 1
    else:
        type = 0

    try:
        case_template = parse_case_template_excel(file, sheet_name='')
        data: List[CaseDbTemplate] = parse_process(case_template, type=type, pid=project_id)
        result = CaseService.create_init(data, user_id=user_id)
    except Exception as err:
        current_app.logger.error(f"Error occurred: {err}", exc_info=True)
        return R.create(500, "Internal server error")

    if result.ok:
        return R.ok(result.content)
    else:
        return R.err(result.content)


@bp.route('/current', methods=['GET'])
@jwt_required()
def get_all_case():
    result = CaseService.get_all_case(request.args['pid'], request.args['node'], get_user_id())

    if result.ok:
        return R.ok(result.content)
    else:
        return R.err(result.content)
    
# @bp.route('/test', methods=['POST'])
# @jwt_required()
# def upload():
#     CaseService.validate_input_data({})
#     return R.ok("")