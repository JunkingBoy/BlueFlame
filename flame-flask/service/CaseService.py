from model.User import User
from model import db
from model.Case import Case, FuncCase, CaseState
from service.CaseTemplate import CaseTemplate
from flask import current_app

class CaseService:
    @staticmethod
    def insert_cases_to_db(case_template: CaseTemplate, user_id: int, project_id: int):
        cases_data = case_template.get_data()

        if isinstance(cases_data, list) and all(isinstance(item, dict) for item in cases_data):
            for case_data in cases_data:
                # 创建 Case 对象
                case = Case(
                    user_id=user_id,
                    project_id=project_id
                )
                db.session.add(case)
                db.session.commit()  # 确保 Case 被分配了 ID

                # 创建 FuncCase 对象
                func_case = FuncCase(
                    case_id=case.id,
                    case_name=case_data.get('case_name'),
                    case_belong_module=case_data.get('module'),
                    case_step=case_data.get('steps'),
                    case_except_result=case_data.get('expected_result'),
                    case_state=CaseState.UNKNOWN,  # 根据需要设置初始状态
                    # case_comment=case_data.get('test_result')
                )
                db.session.add(func_case)
            db.session.commit()
        else:
            current_app.logger.error(f"Invalid data format: {cases_data}")
            raise ValueError("Invalid data format")

    @staticmethod
    def insert_case_with_func_cases(case_data: dict, func_case_data: dict) -> None:
        try:
            # 开启事务
            db.session.begin(nested=True)
            
            # 创建并插入Case实例
            case = Case(**case_data)
            db.session.add(case)
            db.session.flush()  # 立即执行SQL以获取case的ID
            
            # 创建并插入FuncCase实例
            func_case = FuncCase(case_id=case.id, **func_case_data)
            db.session.add(func_case)
            
            # 提交事务
            db.session.commit()
        except Exception as e:
            # 回滚事务
            db.session.rollback()
            raise e
