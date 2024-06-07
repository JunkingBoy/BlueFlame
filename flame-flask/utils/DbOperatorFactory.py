from typing import Dict, Any, Tuple

from ..config import UserOrm

def insertFactory(insertData: Dict[str, Any]) -> bool:
    '''
    取出字典内的值,
    还需要构造一层ORM -> 防止api直接暴露数据库字段给到外部,
    构造元组
    将元组传给数据库进行插入操作
    '''
    tableName: str = insertData['table']
    tempInsert: Dict[str, Any] = insertData['data'][0]
    # userOrm: object = UserOrm(tempInsert)
    # realInsert: Dict[str, Any] = userOrm.getUserOrm()

    # columnsName: str = ','.join(realInsert.keys())
    # dataTuple: Tuple[str] = tuple(realInsert.values())

    # # 构造插入语句的值部分，使用？作为占位符
    # placeholders: str = ','.join(['?'] * len(realInsert))

    # sql: str = f'INSERT INTO {tableName} ({columnsName}) VALUES ({placeholders})'

    sql: str = ''

    return sql