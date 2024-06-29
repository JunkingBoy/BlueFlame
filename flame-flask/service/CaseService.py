from typing import Any, List, Dict
from model.User import User
from model import db
from model.Case import Case, FuncCase, CaseState
from service.CaseTemplate import CaseTemplate
from flask import current_app
from sqlalchemy.exc import SQLAlchemyError


class CaseService:
    
    # TODO::UNDER_DISCUSSION<2024-06-26> 是否 FuncCase 是否循环 commit, 不满足的 Case 单次回退, 返回用户失败的数据, 返回形式待定(返回解析出错的样例)
    @staticmethod
    def insert_data_to_db(data: List[Dict[str, Any]], user_id: str, project_id: int) -> List[Dict[str, Any]] | None:
        try:
            print("In insert_data_to_db")
            if not data:
                return []
            else:
                print("Input data:", data)
                for item in data:
                    # Validate input data
                    if not all(key in item for key in ['case_name', 'module', 'steps', 'expected_result']):
                        raise ValueError("Missing required case information in input data")
                    
                    # Check if the case already exists
                    existing_case = Case.query.filter_by(user_id=user_id, project_id=project_id).first()
                    
                    if existing_case:
                        # Update existing case
                        existing_case.user_id = user_id
                        existing_case.project_id = project_id
                        db.session.commit()  # Commit to generate case.id
                        
                        # Update existing FuncCase
                        func_case = FuncCase.query.filter_by(case_id=existing_case.id).first()
                        if func_case:
                            func_case.case_name = item['case_name']
                            func_case.case_belong_module = item.get('module')
                            func_case.case_step = item.get('steps')
                            func_case.case_except_result = item.get('expected_result')
                            func_case.case_state = CaseState.UNKNOWN  # Adjust based on actual status if needed
                            func_case.case_comment = None  # Add comment if available
                            db.session.commit()
                    else:
                        # Create and add new Case
                        case = Case(user_id=user_id, project_id=project_id)
                        db.session.add(case)
                        db.session.commit()  # Commit to generate case.id
                        
                        # Create and add new FuncCase
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
