from analytical.func import func_analitic
from flask import current_app
from typing import List, Dict, Any

from utils.CaseDb import CaseDbTemplate
from utils.DateUtil import now
from utils.StringUtil import sha256_str

'''
将数据打包处理成可入库的形式的数组
'''
def parse_process(data: List[Dict[str, Any]], type: int, pid: str, uid: str) -> List[CaseDbTemplate]:
    '''
    将data、type、pid、uid打包成CaseDbTemplate
    '''
    case_list: List[CaseDbTemplate] = []
    pack_data: Dict[str, Any] = {}

    try:
        for item in data:
            pack_data = {
                'pid': pid,
                'uid': uid,
                'case_type': type,
                'case_detail': item,
                'case_row_hash': sha256_str(str(item)),
            }
            case_list.append(CaseDbTemplate(**pack_data))
    except Exception as e:
        current_app.logger.error(e)

    return case_list