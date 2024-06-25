from typing import Any
from typing import Any
from model.User import User
from model import db
from model.Case import Case, FuncCase, CaseState
from service.CaseTemplate import CaseTemplate
from flask import current_app

class CaseService:

    @staticmethod


    # TODO::UNDER_DISCUSSION<2024-06-26> 是否 FuncCase 是否循环 commit, 不满足的 Case 单次回退, 返回用户失败的数据, 返回形式待定(返回解析出错的样例)
    def insert_data_to_db(data: list[dict[str, Any]], user_id: int, project_id: int)-> list[dict[str, Any]]:
        try:
            if not data: 
                return []
            for item in data:
                case = Case(user_id=user_id, project_id=project_id)
                db.session.add(case)
                db.session.commit()  # 提交以生成 case.id
                func_case = FuncCase(
                    case_id=case.id,
                    case_name=item.get('case_name'),
                    case_belong_module=item.get('module'),
                    case_step=item.get('steps'),
                    case_except_result=item.get('expected_result'),
                    case_state=CaseState.UNKNOWN,  # 您可以根据实际情况设置状态
                    case_comment=None  # 如果有注释，可以添加
                )
                db.session.add(func_case)
            
            db.session.commit()
            print("数据插入成功")
        except Exception as e:
            db.session.rollback()
            print(f"数据插入失败: {str(e)}")
