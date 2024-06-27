from flask import Blueprint, Response, request
from model.User import UserIdentity
from flask_jwt_extended import get_jwt_identity, jwt_required
from service.UserService import get_user_indentity
from utils.CommonResponse import R

func_case = Blueprint("func_case", __name__)

@func_case.route("/case/func/create", methods=["POST"])
@jwt_required()
def create_case()-> Response:
    # 根据一个 type 类型, 决定创建那种类型的 case
    from service.CaseService import CaseService
    
    user: UserIdentity = get_user_indentity()
    case =  {
        "user_id": user.user_id,
        "project_id": 1, 
        "case_name": "case_name",
        "case_belong_module": "case_belong_module",
        "case_step": "case_step",
        "case_except_result": "case_except_result",
        "case_comment": "case_comment"
    }
    data = request.json
    if not data:
        return R.err({
            "error":
            "No data provided, `phone`, `password` are required"
        })

    # data的作用
    CaseService.insert_case_with_func_cases(case, case)
    return R.ok("创建成功")
