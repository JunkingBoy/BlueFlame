from flask import Blueprint, Flask, request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import or_
from datetime import datetime
from typing import Any, Dict, List
from model import db
from model.Case import Case, CaseState, FuncCase
from utils.CommonResponse import R

# TODO<2024-06-29, @xcx> 暂时不注册这个 api 组, 未确定怎么搜索
case = Blueprint('case', __name__)


@case.route('/search_cases', methods=['GET'])
@jwt_required()
def search_cases():
    try:
        # 获取查询参数
        user_id = request.args.get('user_id')
        case_state = request.args.get('case_state')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        case_name = request.args.get('case_name')
        project_id = request.args.get('project_id')

        # 构建查询
        query = db.session.query(FuncCase).join(Case, FuncCase.case_id == Case.id)

        # 根据 user_id 过滤
        if user_id:
            query = query.filter(Case.user_id == user_id)

        # 根据 case_state 过滤
        if case_state:
            query = query.filter(FuncCase.case_state == CaseState(case_state))

        # 根据 project_id 过滤
        if project_id:
            query = query.filter(Case.project_id == project_id)

        # 根据时间范围过滤
        if start_date and end_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            query = query.filter(Case.update_time.between(start_date, end_date))

        # 根据 case_name 模糊搜索
        if case_name:
            query = query.filter(FuncCase.case_name.ilike(f'%{case_name}%'))

        # 按更新日期倒序排序
        query = query.order_by(Case.update_time.desc())

        # 执行查询
        results = query.all()

        # 构建返回数据
        cases = []
        for result in results:
            case_info = {
                'case_id': result.case_id,
                'case_name': result.case_name,
                'case_belong_module': result.case_belong_module,
                'case_step': result.case_step,
                'case_except_result': result.case_except_result,
                'case_state': result.case_state.value,
                'case_comment': result.case_comment,
                'create_time': result.create_time.isoformat(),
                'update_time': result.update_time.isoformat()
            }
            cases.caseend(case_info)

        return R.ok({'cases': cases})

    except Exception as e:
        print(e)
        return R.err({'error': str(e)})
