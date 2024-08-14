from model import db
from typing import List, Optional
from flask import current_app
from typing import Dict, List, Optional, Any
from sqlalchemy import bindparam, func, cast
from sqlalchemy.dialects.postgresql import JSONB

from model.Project import Project, ProjectUser
from model.Case import Case, CasePointer
from service.ServiceResult import ServiceResult
from utils.CaseDb import CaseDbTemplate
from utils.DateUtil import now
from utils.StringUtil import sha256_str
from dto.response.CaseDto import CaseAllDataDTO

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
    def create_init(data: List[CaseDbTemplate], user_id: str) -> ServiceResult:
        project: Optional[Project] = None
        pid: str = data[0].pid
        type: int = data[0].case_type
        c_array: List[str] = []
        inser_data: Case
        pointer_date: CasePointer

        try:
            project = db.session.query(Project).filter(
                Project.pid == bindparam('pid_param'), # type: ignore
                Project.creator == bindparam('uid_param'), # type: ignore
                Project.is_delete == bindparam('is_delete_param'), # type: ignore
                Project.is_init == bindparam('is_init_param') # type: ignore
            ).params(
                pid_param=pid,
                uid_param=user_id,
                is_delete_param=False,
                is_init_param=False
            ).first()

            if project is None:
                return ServiceResult.fail(f"can not found this project or this project is init")
            else:
                for case in data:
                    inser_data = Case(cid=sha256_str(f"{pid}{user_id}{case.case_row_hash}{now()}"), project_id=pid, user_id=user_id, case_type=type, data=case.case_detail, state=case.case_state, row_hash=case.case_row_hash)
                    c_array.append(inser_data.cid)
                    db.session.add(inser_data)
                project.is_init = True
                pointer_date = CasePointer(pid=pid, p_pointer=None, c_pointer=sha256_str(f"{pid}{user_id}{now()}"), cid_array=c_array)
                db.session.add(pointer_date)
                db.session.commit()
                return ServiceResult.success(f"case upload success")
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"case insert failed: {str(e)}", exc_info=True)
            return ServiceResult.fail(f"case upload failed")

    # @staticmethod
    # def create_merge(data: List[CaseDbTemplate], project_id: str, user_id: str) -> ServiceResult:
    #     '''
    #     提交的用户是项目创建者
    #     case_type: 0: func_case, 1: api_case -> 确保cid的绝对唯一 -> uid+file+now进行hash结果在进行索引的新增
    #     merge以后的cid是uid+plan_id+now进行hash然后结果进行索引的新增
    #     新增case_log记录case的相关变更 -> 对于case_log只有add的操作 -> 对那一次的merge操作进行记录 -> 提供commit_hash字段.那一次的所有db的操作都打上该commit_hash
    #     '''


    @staticmethod
    def get_all_case(project_id: str, node: str | None, user_id: str) -> ServiceResult:
        '''
        用户属于项目
        项目没删除
        结果:
        根据当前节点的cid_array去到case表查询出case_detail
        '''
        project: Optional[Project] = None
        project_user: Optional[ProjectUser] = None
        current_node: Optional[str] = node
        node_cid_data: List[str]
        data: List[Case] = []
        pointer_case_data: CaseAllDataDTO

        try:
            project_user = db.session.query(ProjectUser).filter(
                ProjectUser.pid == bindparam('pid_param'), # type: ignore
                ProjectUser.uid == bindparam('uid_param'), # type: ignore
            ).params(
                pid_param=project_id,
                uid_param=user_id
            ).first()

            if project_user is None:
                return ServiceResult.fail(f"you can not get this project case info")

            project = db.session.query(Project).filter(
                Project.pid == bindparam('pid_param'), # type: ignore
                Project.is_init == bindparam('is_init_param'), # type: ignore
                Project.is_delete == bindparam('is_delete_param') # type: ignore
            ).params(
                pid_param=project_id,
                is_init_param=True,
                is_delete_param=False
            ).first()

            if project is None:
                return ServiceResult.fail(f"project can not found")
            else:
                '''
                先经过case_pointer表查询当前项目的c_pointer指向的cid_array
                然后拿cid_array去到case表查询出case_detail
                返回的数据结构为: {'c_p': '', 'cid_list': [cid1, cid2, cid3], 'data_list': [case_detail1, case_detail2, case_detail3]}
                '''
                node_cid_data = db.session.query(
                    CasePointer.cid_array # type: ignore
                ).filter(
                    CasePointer.pid == bindparam('pid_param'), # type: ignore
                    CasePointer.c_pointer == bindparam('c_pointer_param') # type: ignore
                ).params(
                    pid_param=project_id,
                    c_pointer_param=current_node
                ).scalar()

                node_cid_data = list(node_cid_data)

                data = db.session.query( # type: ignore
                    func.jsonb_set(
                        func.jsonb_set(
                            cast(Case.case_detail, JSONB),
                            '{case_state}',
                            func.to_jsonb(Case.case_state)
                        ),
                        '{update_time}',
                        func.to_jsonb(Case.update_time)
                    ).label('case_detail')
                ).filter(
                    Case.pid == bindparam('pid_param'), # type: ignore
                    Case.cid.in_(node_cid_data) # type: ignore
                ).params(
                    pid_param=project_id,
                ).all()

                # pointer_case_data = CaseAllDataDTO( # type: ignore
                #     c_p=current_node, # type: ignore
                #     cid_list=node_cid_data,
                #     data_list=data # type: ignore
                # )

                return ServiceResult.success(data=data) # type: ignore
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
