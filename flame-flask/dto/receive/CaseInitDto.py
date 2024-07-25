import io
import mimetypes
from email import message_from_bytes
import openpyxl
from pydantic import Field, field_validator
from werkzeug.datastructures import FileStorage

from dto.BaseDTO import BaseDTO

class ExcelFile(BaseDTO):
    file: FileStorage

    # type: str = Field(
    #     ...,
    #     description='file type'
    # )

    # project_id: str = Field(
    #     ...,
    #     min_length=16, 
    #     max_length=16,
    #     description="project id"
    # )

    @field_validator('file', mode='before')
    def validate_excel_file(cls, v):
        if not isinstance(v, FileStorage):
            raise ValueError(f'Invalid file type.')
        
        mime_type, _ = mimetypes.guess_type(v.file)

        if mime_type is None:
            raise ValueError(f'Unable to guess file type.')

        # # 读取前一部分数据来猜测MIME类型
        # initial_pos = v.tell()
        # v.seek(0)
        # data = v.read(1024)  # 读取前1024字节
        # v.seek(initial_pos)  # 重置文件指针

        # # 使用email库解析MIME类型，因为mimetypes不支持BytesIO
        # msg = message_from_bytes(data)
        # content_type = msg.get_content_type()

        # 检查MIME类型是否为Excel类型
        if mime_type not in ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                                'application/vnd.ms-excel']:
            raise ValueError(f'File is not an Excel file based on MIME type.')
        return v

    def __init__(self, **data):
        super().__init__(**data)

    # @field_validator('type', mode='before')
    # def check_type(cls, v):
        # if v == 'func_case':
        #     return 0
        # elif v == 'api_case':
        #     return 1
        # else:
        #     raise ValueError(f'Invalid type.')

