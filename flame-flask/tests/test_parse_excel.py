# 读取 Excel 的文件类型兼容问题...
import pandas as pd

def read_excel_file(file_path):
    try:
        data = pd.read_excel(file_path, engine='openpyxl')
        print(data.head())
    except Exception as e:
        print(f"Error reading Excel file: {e}")

# Replace 'path_to_your_file.xlsx' with your actual file path
file_path = '/Users/xcx/Downloads/case_template.xlsx'
read_excel_file(file_path)
