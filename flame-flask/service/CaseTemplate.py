import openpyxl
from openpyxl.worksheet.worksheet import Worksheet
from typing import List, Dict, Any
from flask import current_app
from utils.FindHeader import find_header

class CaseTemplate:

    def __init__(self, file_path: str, file_type: str):
        self.file_path = file_path
        self.data = None
        self.case_type = file_type
        self.parse()

    def parse(self):
        # 读取Excel 文件, 并解析数据成 list[dict[str, any]]
        self.data = self.parse_case_template_excel()

    def get_data(self):
        return self.data

    def parse_case_template_excel(
            self,
            sheet_name: str = None) -> List[Dict[str, Any]] | R:  # type: ignore
        try:
            # 加载Excel工作簿
            workbook = openpyxl.load_workbook(self.file_path)

            # 选择工作表
            if sheet_name:
                sheet: Worksheet = workbook[sheet_name]
            else:
                sheet: Worksheet = workbook.active  # type: ignore

            # 获取表头
            headers = [
                cell.value
                for cell in next(sheet.iter_rows(min_row=1, max_row=1))
            ]

            '''
            根据传入的file_type选择需要对应的表头
            '''
            header_dict: Dict[str, Any] = find_header(self.case_type)

            if header_dict is not {}:
                data = []
                # 从第二行开始读取数据
                for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row):
                    row_data = {}
                    for cell, header in zip(row, headers):
                        cell_value = cell.value
                        for merged_cell_range in sheet.merged_cells:  # type: ignore
                            if cell.coordinate in merged_cell_range:
                                cell_value = sheet.cell(
                                    row=merged_cell_range.min_row,
                                    column=merged_cell_range.min_col).value
                                break
                        # 将中文表头转换为英文表头
                        english_header = header_dict.get(header, header)  # type: ignore
                        row_data[english_header] = cell_value
                    data.append(row_data)
                    return data
            else:
                current_app.logger.error(f"An error occurred while parsing the case template")
                return []
        except Exception as e:
            current_app.logger.error(f"An error occurred while parsing the case template: {str(e)}")
            
        return []
