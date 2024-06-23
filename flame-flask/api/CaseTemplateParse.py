import os
from flask_jwt_extended import jwt_required
from utils.CommonResponse import R
from flask import Blueprint, send_file, request


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

    if template_filepath != '':
        try:
            return send_file(template_filepath, as_attachment=True)
        except FileNotFoundError as err:
            print(f"File not found: {err}")
            return R.create(1234, "File not found") 
        finally:
            os.chdir(cwd)
    else:
        return R.create(code=404, msg='type参数错误', data={})
