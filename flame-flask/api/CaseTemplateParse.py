'''
Author: Lucifer
Data: Do not edit
LastEditors: Lucifer
LastEditTime: 2024-07-25 22:33:39
Description: 
'''
from service.CaseService import CaseService
from service.UserService import get_user_id
from flask_jwt_extended import jwt_required
from utils.CommonResponse import R
from flask import Blueprint, request, send_file, current_app
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from typing import List, Optional
from pydantic import ValidationError

from service.CaseProcessing import parse_process
from utils.ExcelExtract import parse_case_template_excel
from utils.CaseDb import CaseDbTemplate
from dto.receive.CaseInitDto import ExcelFile

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
    case_type: str = ""
    type: int = 0

    try:
        if 'type' not in request.args:
            return R.err('Missing required parameter: type')
        
        case_type: str = request.args['type']

        match case_type:
            case 'func_case':
                type = 0
            case 'api_case':
                type = 1
            case _:
                return R.err(f'Invalid case type')

        if 'project_id' not in request.args:
            return R.err('Missing required parameter: project_id')
            
        # try:
        #     print("1111111111111111111111111111111111111")
        #     file: Optional[ExcelFile] = ExcelFile(**request.get_json()) # type: ignore
        #     project_id: str = request.args['project_id']
        #     user_id: str = get_user_id()
        #     case_template = parse_case_template_excel(file, sheet_name='') # type: ignore
        #     data: List[CaseDbTemplate] = parse_process(case_template, type=type, pid=project_id, uid=user_id)
        #     print(f'case_template.get_data(): {data[0].pid, data[0].uid, data[0].case_type, data[0].case_detail, data[0].case_row_hash}')
        #     result = CaseService.create_init(data, get_user_id())

        #     if result.ok:
        #         return R.ok(result.content)
        #     else:
        #         return R.err(result.content)
        # except ValidationError as e:
        #     current_app.logger.error(f"Error occurred: {e}", exc_info=True)
        #     return R.create(500, f"Internal server error")

    except Exception as err:
        current_app.logger.error(f"Error occurred: {err}", exc_info=True)
        return R.create(500, "Internal server error")
    # if 'file' not in request.files:
    #     return R.err('No file upload')
    # if 'type' not in request.args:
    #     return R.err('Missing required parameter: type')
    # if 'project_id' not in request.args:
    #     return R.err('Missing required parameter: project_id')
    # if 'only_return_err' not in request.args:  # 1 : true,  0: false
    #     return R.err('Missing required parameter: all')

    # case_type: str = request.args['type'] # 现阶段case_type字段对于插库而言无用
    # project_id: str = request.args['project_id']
    # user_id: str = get_user_id()
    # only_return_err = True if request.args['only_return_err'] == '1' else False
    # file: FileStorage = request.files['file']
    # if file.filename == '' or file.filename is None:
    #     return R.err('No selected file')
    # if not is_valid_file(file.filename):
    #     return R.err('Invalid file type')
    
    # type: int = 0
    
    # if case_type == 'func_case':
    #     type = 0
    # else:
    #     type = 1

    # case_template = parse_case_template_excel(file, sheet_name='')
    # data: List[CaseDbTemplate] = parse_process(case_template, type=type, pid=project_id, uid=user_id)
    # print(f'case_template.get_data(): {data[0].pid, data[0].uid, data[0].case_type, data[0].case_detail, data[0].case_row_hash}')
    # result = CaseService.create_init(data, get_user_id())

    # if result.ok:
    #     return R.ok(result.content)
    # else:
    #     return R.err(result.content)


@bp.route('/all', methods=['GET'])
@jwt_required()
def get_all_case():
    return R.ok(CaseService.get_all_case(request.args['pid'], get_user_id()))

# @bp.route('/test', methods=['POST'])
# @jwt_required()
# def upload():
#     CaseService.validate_input_data({})
#     return R.ok("")