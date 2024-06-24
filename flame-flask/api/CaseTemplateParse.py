import os
from flask_jwt_extended import jwt_required
from utils.CommonResponse import R
from flask import Blueprint, send_file, request, Response


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

@case.route('/upload/case', methods=["POST"])
@jwt_required()
def upload_case_file() -> Response:
    type: str | None = request.args.get('type')
    file = request.files.get('file')

    if not file:
        return R.create(code=400, msg='File not found', data={})

    # 获取文件拓展名
    fileName: str | None = file.filename
    if fileName is not None:
        fileExtension: str = fileName.rsplit('.', 1)[1].lower()
        if fileExtension in ('xlsx', 'xls'):
            file.save(f'./static/test_template.{fileExtension}')
        else:
            return R.create(code=400, msg='File extension error', data={})
        
    return R.create(code=200, msg='Success', data={})