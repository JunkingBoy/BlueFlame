from model import db
from typing import List, Optional
from flask import current_app
from typing import Dict, List, Optional, Any

from model.Project import Project, ProjectUser
from model.Case import Case
from service.ServiceResult import ServiceResult
from utils.CaseDb import CaseDbTemplate

# def data_to_dict_list(data: List[Case]) -> List[Dict[str, Any]]:
#     ret_data: List[Dict[str, Any]] = []

#     ret_data = [
#         {
#             'cid': cid,
#             'case_type': case_type,
#             'case_detail': case_detail,
#         }
#         for cid, case_type, case_detail in data
#     ]
    

class CaseService:
    @staticmethod
    def create(data: List[CaseDbTemplate], user_id: str) -> ServiceResult:
        project: Optional[Project] = None
        pid: str = data[0].pid
        uid: str = data[0].uid
        type: str = data[0].case_type
        inser_data: Case
        time: int = 0

        if uid != user_id:
            return ServiceResult.fail(f"you are not those case owner")

        try:
            project = db.session.query(Project).filter(
                Project.pid == pid, # type: ignore
                Project.creator == uid, # type: ignore
                Project.is_delete == False, # type: ignore
                Project.is_init == False # type: ignore
            ).first()

            if project is None:
                return ServiceResult.fail(f"can not found this project")
            else:
                for case in data:
                    inser_data = Case(init_data=case.case_detail, cid=f"{user_id}{time}" , case_type=type, project_id=pid, user_id=uid, row_hash=case.case_row_hash)
                    time += 1
                    db.session.add(inser_data)
                project.is_init = True
                db.session.commit()
                return ServiceResult.success(f"case upload success")
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"case insert failed: {str(e)}", exc_info=True)
            return ServiceResult.fail(f"case upload failed")
    
    @staticmethod
    def get_all_case(project_id: str, user_id: str) -> ServiceResult:
        '''
        用户属于项目
        项目没删除
        获取所有case信息返回
        '''
        project: Optional[Project] = None
        project_user: Optional[ProjectUser] = None
        data: List[Case] = []

        try:
            project_user = db.session.query(ProjectUser).filter(
                ProjectUser.pid == project_id, # type: ignore
                ProjectUser.uid == user_id, # type: ignore
            ).first()

            if project_user is None:
                return ServiceResult.fail(f"you can not get this project case info")

            project = db.session.query(Project).filter(
                Project.pid == project_id, # type: ignore
                Project.is_init == True, # type: ignore
                Project.is_delete == False # type: ignore
            ).first()

            if project is None:
                return ServiceResult.fail(f"project can not found")
            else:
                data = db.session.query( # type: ignore
                    Case.cid, # type: ignore
                    Case.case_type, # type: ignore
                    Case.case_detail # type: ignore
                ).filter(
                    Case.pid == project_id, # type: ignore
                ).all()
                print(data)
                return ServiceResult.success(f"get case info success")
        except Exception as e:
            current_app.logger.error(f"case get all failed: {str(e)}", exc_info=True)
            return ServiceResult.fail(f"case get all failed")


#     # 检查case是否已经存在
#     @staticmethod
#     def get_existing_case(case_id_by_user: str, project_id: int) -> Case | None:
#         return Case.query.filter_by(case_id_by_user=case_id_by_user, project_id=project_id).first()

#     # 更新已存在的case_id_by_user
#     @staticmethod
#     def update_existing_case(existing_case: Case, user_id: str, project_id: int, item: Dict[str, Any]) -> None:
#         existing_case.user_id = user_id
#         existing_case.project_id = project_id
#         existing_case.case_id_by_user = str(item['case_id_by_user'])
#         db.session.commit()
    
#     # 更新对应的 func_case
#     @staticmethod
#     def update_existing_func_case(existing_case: Case, item: Dict[str, Any]) -> None:
#         func_case = FuncCase.query.filter_by(case_id=existing_case.id).first()
#         if func_case:
#             func_case.case_name = item['case_name']
#             func_case.case_belong_module = item.get('module')
#             func_case.case_step = item.get('steps')
#             func_case.case_except_result = item.get('expected_result')
#             func_case.case_state = CaseState.WAITING   # 这里需要根据实际情况调整, 比如 0: PASS, 1: FAIL, 2: UNKNOWN...
#             func_case.case_comment = None
#             db.session.commit()
    
#     # 创建新的 case
#     @staticmethod
#     def create_new_case(user_id: str, project_id: int, item: Dict[str, Any]) -> Case:
#         case = Case(user_id=user_id, project_id=project_id, case_id_by_user=item['case_id_by_user'])
#         db.session.add(case)
#         db.session.commit()
#         return case
    
#     # 将解析出的 case_list 插入数据库
#     @staticmethod
#     def insert_data_to_db(data: List[Dict[str, Any]], user_id: str, project_id: str) -> List[Dict[str, Any]] | None:
#         try:
#             print("In insert_data_to_db")
#             if not data:
#                 return []
#             else:
#                 print("Input data:", data)
#                 for item in data:
#                     CaseService.validate_input_data(item)
#                     existing_case = CaseService.get_existing_case(item['case_id_by_user'], int(project_id))
#                     print('-' * 80)
#                     print(f'existing_case: {existing_case}')
#                     print('-' * 80)

#                     if existing_case:
#                         CaseService.update_existing_case(existing_case, user_id, int(project_id), item)
#                         CaseService.update_existing_func_case(existing_case, item)
#                     else:
#                         case = CaseService.create_new_case(user_id, int(project_id), item)
#                         CaseService.create_new_func_case(case, item)

#                 current_app.logger.debug("Data inserted/updated successfully", exc_info=True)
#                 return data
#         except SQLAlchemyError as e:
#             db.session.rollback()
#             current_app.logger.error(f"Database insert/update failed: {str(e)}", exc_info=True)
#         except ValueError as e:
#             db.session.rollback()
#             current_app.logger.error(f"Validation error: {str(e)}", exc_info=True)
#         except Exception as e:
#             db.session.rollback()
#             current_app.logger.error(f"Unexpected error: {str(e)}", exc_info=True)
#         return None
