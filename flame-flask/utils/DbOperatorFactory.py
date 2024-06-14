from typing import Dict, Any, List, Tuple

from datetime import datetime
# from ..config import UserOrm

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
    realInsert: Dict[str, Any] = getUserOrm(tempInsert)

    columnsName: Tuple[str, ...] = tuple(realInsert.keys())
    dataTuple: Tuple[Any, ...] = tuple(realInsert.values())

    # 构造插入语句的值部分，使用？作为占位符 -> 确保与columnsName长度一致
    placeholders: Tuple[str, ...] = tuple('?' for _ in columnsName)

    sql: str = f'INSERT INTO {tableName} ({','.join(columnsName)}) VALUES ({','.join(placeholders)})'

    return True

def selectFactory(selectData: Dict[str, Any]) -> List[Dict[str, Any]]:
    '''
    传入一个字典对象.应该类似这种形式
    { table: 查哪张表, field: [ 查询字段 ], filter: { 筛选字段: 值 } } -> 如果查询字段没有的话就select *
    然后返回的是一个结果对象的数组
    '''
    tableName: str = selectData['table']
    tempField: List[str] = selectData.get('field', [])
    tempFilter: List[Dict[str, Any]] = selectData.get('filter', {})

    responseData: List[Dict[str, Any]] = []

    if tempField:
        fields: str = ','.join(tempField)
    else:
        fields: str = '*'

    # 构建查询语句
    sql: str = f'SELECT {fields} from {tableName}'
    
    # 构建where子句
    if tempFilter:
        filterClauses: List[str] = [f'{key} = ?' for key in tempFilter.keys()]
        whereClauses: str = 'WHERE' + 'AND'.join(filterClauses)
        sql += whereClauses
    
    # 提取出where子句需要的值 -> tempFilter.values()提取出字典的vlaue转为数组
    filterValue: List[Any] = list(tempFilter.values())

    # 执行查询

    # 构建临时返回值
    return [
        {'name': '第一个项目', 'pv': 100, 'uv': 200},
        {'name': '第二个项目', 'pv': 200, 'uv': 300},
        {'name': '第三个项目', 'pv': 300, 'uv': 400}
    ]

def getUserOrm(insertData: Dict[str, Any]) -> Dict[str, Any]:
    return {
        'username': insertData['email'],
        'email': insertData['email'],
        'phone': insertData['phone'],
        'password': insertData['password'],
        'insert_time': str(datetime.now()),
        'update_time': ''
    }