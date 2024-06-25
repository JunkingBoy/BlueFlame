import io
from typing import List, Dict, Any
from openpyxl import load_workbook
from openpyxl.worksheet.worksheet import Worksheet
from werkzeug.datastructures import FileStorage
from flask import current_app
from utils.FindHeader import find_header

class CaseTemplate:

    def __init__(self, file: FileStorage, case_type: str = ""):
        self.file = file
        self.case_type = case_type
        self.data = self.parse_case_template_excel()

    def get_data(self):
        return self.data

    def parse_case_template_excel(self,
                                  sheet_name: str = ""
                                  ) -> List[Dict[str, Any]]:
        try:
            # 将 FileStorage 对象的内容读取到内存中的 BytesIO 对象
            file_stream = io.BytesIO(self.file.read())
            
            # 使用 BytesIO 对象加载工作簿
            workbook = load_workbook(file_stream, data_only=True)
            sheet = workbook[sheet_name] if sheet_name else workbook.active
            headers = [cell.value for cell in next(sheet.iter_rows(min_row=1, max_row=1))]
            header_dict = self.get_header_dict()
            data = self.extract_data(sheet, headers, header_dict)
            return data
        except Exception as e:
            print(f"解析模板时发生错误: {str(e)}")
            return []

    def get_header_dict(self) -> Dict[str, str]:
        return {
            '用例编号': 'case_id',
            '用例名称': 'case_name',
            '测试环境': 'test_environment',
            '所属模块': 'module',
            '前置条件': 'precondition',
            '操作步骤': 'steps',
            '预期结果': 'expected_result',
            '测试结果': 'test_result',
            '创建时间': 'create_time',
            '修改时间': 'modify_time'
        }

    def extract_data(self, sheet: Worksheet, headers: List[str],
                     header_dict: Dict[str, str]) -> List[Dict[str, Any]]:
        data = []
        merged_cells_value = self.get_merged_cells_value(sheet)
        for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row):
            row_data = {}
            for cell, header in zip(row, headers):
                cell_value = merged_cells_value.get(cell.coordinate,
                                                    cell.value)
                english_header = header_dict.get(header, header)
                row_data[english_header] = cell_value
            data.append(row_data)
        return data

    def get_merged_cells_value(self, sheet: Worksheet) -> Dict[str, Any]:
        merged_cells_value = {}
        for merged_range in sheet.merged_cell_ranges.ranges:
            top_left_value = sheet.cell(merged_range.min_row,
                                        merged_range.min_col).value
            for row in range(merged_range.min_row, merged_range.max_row + 1):
                for col in range(merged_range.min_col,
                                 merged_range.max_col + 1):
                    merged_cells_value[sheet.cell(
                        row, col).coordinate] = top_left_value
        return merged_cells_value
