from sqlalchemy.exc import SQLAlchemyError
from flask import current_app
from model import db
from typing import List, Dict, Any
from model.Case import Case, FuncCase, CaseState

# TODO::UNDER_DISCUSSION<2024-06-26> 是否 FuncCase 是否循环 commit, 不满足的 Case 单次回退, 返回用户失败的数据, 返回形式待定(返回解析出错的样例)
class CaseService:

    @staticmethod
    def validate_input_data(item: Dict[str, Any]) -> None:
        # 验证输入数据, # TODO<2024-06-29, @xcx> case_id_by_user 是否需要验证(必填)
        required_keys = ['case_id_by_user', 'case_name', 'module', 'steps', 'expected_result']
                            
        if not all(key in item for key in required_keys):
            raise ValueError("Missing required case information in input data")
    
    # 检查case是否已经存在
    @staticmethod
    def get_existing_case(case_id_by_user: str, project_id: int) -> Case | None:
        return Case.query.filter_by(case_id_by_user=case_id_by_user, project_id=project_id).first()
    
    # 更新已存在的case_id_by_user
    @staticmethod
    def update_existing_case(existing_case: Case, user_id: str, project_id: int, item: Dict[str, Any]) -> None:
        existing_case.user_id = user_id
        existing_case.project_id = project_id
        existing_case.case_id_by_user = item['case_id_by_user']
        db.session.commit()
    
    # 更新对应的 func_case
    @staticmethod
    def update_existing_func_case(existing_case: Case, item: Dict[str, Any]) -> None:
        func_case = FuncCase.query.filter_by(case_id=existing_case.id).first()
        if func_case:
            func_case.case_name = item['case_name']
            func_case.case_belong_module = item.get('module')
            func_case.case_step = item.get('steps')
            func_case.case_except_result = item.get('expected_result')
            func_case.case_state = CaseState.WAITING   # 这里需要根据实际情况调整, 比如 0: PASS, 1: FAIL, 2: UNKNOWN...
            func_case.case_comment = None
            db.session.commit()
    
    # 创建新的 case
    @staticmethod
    def create_new_case(user_id: str, project_id: int, item: Dict[str, Any]) -> Case:
        case = Case(user_id=user_id, project_id=project_id, case_id_by_user=item['case_id_by_user'])
        db.session.add(case)
        db.session.commit()
        return case
    
    # 创建新的对应的 func_case
    @staticmethod
    def create_new_func_case(case: Case, item: Dict[str, Any]) -> None:
        func_case = FuncCase(
            case_id=case.id,
            case_name=item['case_name'],
            case_belong_module=item.get('module'),
            case_step=item.get('steps'),
            case_except_result=item.get('expected_result'),
            case_state=CaseState.UNKNOWN,  # Adjust based on actual status if needed
            case_comment=None  # Add comment if available
        )
        db.session.add(func_case)
        db.session.commit()
    
    # 将解析出的 case_list 插入数据库
    @staticmethod
    def insert_data_to_db(data: List[Dict[str, Any]], user_id: str, project_id: int) -> List[Dict[str, Any]] | None:
        try:
            print("In insert_data_to_db")
            if not data:
                return []
            else:
                for item in data:
                    CaseService.validate_input_data(item)
                    existing_case = CaseService.get_existing_case(item['case_id_by_user'], project_id)
                    print('-' * 80)
                    print(f'existing_case: {existing_case}')
                    print('-' * 80)

                    if existing_case:
                        CaseService.update_existing_case(existing_case, user_id, project_id, item)
                        CaseService.update_existing_func_case(existing_case, item)
                    else:
                        case = CaseService.create_new_case(user_id, project_id, item)
                        CaseService.create_new_func_case(case, item)

                current_app.logger.debug("Data inserted/updated successfully", exc_info=True)
                return data
        except SQLAlchemyError as e:
            db.session.rollback()
            current_app.logger.error(f"Database insert/update failed: {str(e)}", exc_info=True)
        except ValueError as e:
            current_app.logger.error(f"Validation error: {str(e)}", exc_info=True)
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        return None
