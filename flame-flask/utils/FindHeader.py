import os
import json
from typing import Dict, Any
from flask import current_app

def find_header(file_type: str) -> Dict[str, Any]:
    what_file: str = ''
    match file_type:
        case '1':
            what_file = 'func_hander'
    
    # 寻找配置文件路径
    cwd: str = os.getcwd()
    module_cwd = os.path.dirname(os.path.realpath(__file__)) # flame-flsk/utils
    config_dir: str = os.path.join(os.path.dirname(module_cwd), 'config')
    confi_file: str = os.path.join(config_dir, 'header.json')

    header: Dict[str, Any] = {}

    if os.path.exists(confi_file):
        try:
            with open(confi_file, 'r', encoding='utf-8') as f:
                confi_data: Dict[str, Any] = json.load(f)

                if what_file in confi_data:
                    header: Dict[str, Any] = confi_data[what_file]
                    return header
                else:
                    current_app.logger.error(f"no such header in config: {what_file}")
                    return {}
        except Exception as e:
            current_app.logger.error(f"read file error: {e}")
            return {}
        
    return {}