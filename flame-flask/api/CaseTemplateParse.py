import os
from service.CaseTemplate import CaseTemplate
from flask_jwt_extended import jwt_required
from utils.CommonResponse import R
from flask import Blueprint,Response,  request, send_file, current_app
from werkzeug.datastructures import FileStorage


case = Blueprint('case', __name__)

@case.route('/download/case_template', methods=["GET"])
@jwt_required()
def download_case_template_file():
    '''
    接收前端传过来的一个type字段
    选择下载的excel类型
    '''
    cwd = os.getcwd()
    module_cwd = os.path.dirname(os.path.realpath(__file__))
    os.chdir(module_cwd) # flame-flask/api

    type: str | None = request.args.get('type')

    template_filepath: str = ''

    match type:
        case '1':
            template_filepath = './static/case_template.xlsx'
        case '2':
            pass
        case _:
            template_filepath = ''

    if template_filepath != '':
        try:
            return send_file(template_filepath, as_attachment=True)
        except FileNotFoundError as err:
            current_app.logger.error(f"Can not found file: {err}")
            return R.create(404, "File not found") 
        finally:
            os.chdir(cwd)
    else:
        return R.create(code=404, msg='typeError', data={})

def is_valid_file(file):
    return '.' in file and file.rsplit('.', 1)[1].lower() in ['xlsx', 'xls']

@case.route('/upload', methods=['POST'])
@jwt_required()
def upload_file():
    if 'file' not in request.files:
        return R.err('No file upload')
    case_type = request.args['type']
    file: FileStorage = request.files['file']
    if file.filename == '' or file.filename is None:
        return R.err('No selected file')
    if not is_valid_file(file.filename):
        return R.err('Invalid file type')

    # print(f'file: {type(file)}')
    data = CaseTemplate(file, case_type).get_data()
    # print(f'data: {data}')

        # data = CaseTemplate(str(file)).get_data()
        # # print(f'data: {data}')

        # # file.save(os.path.join('.', file.filename))
        # # TODO<2024-06-21, @xcx> 添加解析模版的代码
        # return R.ok(data)
