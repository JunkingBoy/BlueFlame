import os
from flask_jwt_extended import jwt_required
from utils.CommonResponse import R
from flask import Blueprint, send_file


case = Blueprint('case', __name__)


@case.route('/download/case_template', methods=["GET"])
@jwt_required()
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
