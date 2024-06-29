from datetime import datetime
import json
import os
from service.CaseTemplate import CaseTemplate
from service.CaseService import CaseService
from service.UserService import get_user_indentity
from flask_jwt_extended import jwt_required
from utils.CommonResponse import R
from flask import Blueprint, request, send_file, current_app
from werkzeug.datastructures import FileStorage

case_parse = Blueprint('case_parse', __name__)


@case.route('/download/case_template', methods=["GET"])
@jwt_required()
def download_case_template_file():
    '''
    # TODO<2024-06-26, @xcx> 接收前端传过来的一个type字段, 选择下载的excel类型
    '''
    cwd = os.getcwd()
    module_cwd = os.path.dirname(os.path.realpath(__file__))
    os.chdir(module_cwd) # flame-flask/api

    template_filepath: str = './static/func_case_template.xlsx'

    if template_filepath != '':
        try:
            return send_file(template_filepath, as_attachment=True, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        except FileNotFoundError as err:
            current_app.logger.error(f"Can not found file: {err}")
            return R.create(404, "File not found") 
        finally:
            os.chdir(cwd)
    else:
        return R.create(code=404, msg='typeError', data={})


def is_valid_file(file):
    return '.' in file and file.rsplit('.', 1)[1].lower() in ['xlsx', 'xls']


@case_parse.route('/upload', methods=['POST'])
@jwt_required()
def upload_file():
    # 检查是否提供了`type`和`project_id`和`file`必要的参数
    # TODO<2024-06-29, @xcx> caseId 相同覆盖用例, caseId 不同新增用例
    if 'file' not in request.files:
        return R.err('No file upload')
    if 'type' not in request.args:
        return R.err('Missing required parameter: type')
    if 'project_id' not in request.args:
        return R.err('Missing required parameter: project_id')
    if 'only_return_err' not in request.args:  # 1 : true,  0: false
        return R.err('Missing required parameter: all')

    case_type: str = request.args['type']
    project_id: str = request.args['project_id']
    user_id: int = get_user_indentity().user_id
    only_return_err = True if request.args['only_return_err'] == '1' else False
    file: FileStorage = request.files['file']
    if file.filename == '' or file.filename is None:
        return R.err('No selected file')
    if not is_valid_file(file.filename):
        return R.err('Invalid file type')

    case_template = CaseTemplate(file,
                                 user_id=user_id,
                                 case_type=case_type,
                                 project_id=int(project_id))
    # TODO<2024-06-26, @xcx> 不插入数据库, 只序列化数据, 查询全部用例的 api 展示不做,
    print(f'case_template.get_data(): {case_template.get_data()}')
    CaseService.insert_data_to_db(case_template.get_data(), case_template.user_id, case_template.project_id)

    folder = f'tmp_response/{datetime.now().strftime("%Y-%m-%d")}'
    if not os.path.exists(folder):
        os.makedirs(folder)

    case_data = case_template.get_data()
    if only_return_err:
        print("only err data")
        case_data = [row for row in case_data if row.get("dirty", False)]

    with open(
            f'tmp_response/{datetime.now().strftime("%Y-%m-%d")}/{case_template.user_id}.json',
            'w') as out_file:
        json.dump(case_data, out_file, indent=2)
        out_file.flush()
        # out_file.write(str(R.ok(case_template.get_data())))

    return R.ok(case_data)
