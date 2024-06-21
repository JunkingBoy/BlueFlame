# 解析案例模板Excel 文件
import pandas as pd


class ParseCaseTemplate:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None
        self.parse()

    def parse(self):
        # 读取Excel 文件
        data = pd.read_excel(self.file_path, engine='openpyxl')
        # 将Excel 文件转换为字典
        self.data = data.to_dict(orient='records')

    def get_data(self):
        return self.data
