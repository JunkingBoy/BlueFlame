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

    sql: str = f"INSERT INTO {tableName} ({','.join(columnsName)}) VALUES ({','.join(placeholders)})"

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
        {'datetime': '2024-01-01', 'finishBug': 100, 'allBug': 200, 'amt': 2400},
        {'datetime': '2024-01-02', 'finishBug': 200, 'allBug': 300, 'amt': 2210},
        {'datetime': '2024-01-03', 'finishBug': 300, 'allBug': 400, 'amt': 2290},
        {'datetime': '2024-01-04', 'finishBug': 400, 'allBug': 500, 'amt': 2000},
        {'datetime': '2024-01-05', 'finishBug': 500, 'allBug': 600, 'amt': 2181},
        {'datetime': '2024-01-06', 'finishBug': 600, 'allBug': 700, 'amt': 2500},
        {'datetime': '2024-01-07', 'finishBug': 700, 'allBug': 800, 'amt': 2100},
        {'datetime': '2024-01-08', 'finishBug': 800, 'allBug': 900, 'amt': 2200},
    ]

def tempSelect(selectData: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [
        {'programName': '我的世界', 'allBug': 500, 'finishBug': 200, 'unWorkBug': 200, 'isNotBug': 100},
        {'programName': '你的世界', 'allBug': 600, 'finishBug': 300, 'unWorkBug': 200, 'isNotBug': 100},
        {'programName': '他的世界', 'allBug': 700, 'finishBug': 400, 'unWorkBug': 200, 'isNotBug': 100},
        {'programName': '她的世界', 'allBug': 800, 'finishBug': 500, 'unWorkBug': 200, 'isNotBug': 100},
        # {'programName': '它的世界', 'allBug': 800, 'finishBug': 200, 'unWorkBug': 200, 'isNotBug': 100},
        # {'programName': '塌的世界', 'allBug': 800, 'finishBug': 200, 'unWorkBug': 200, 'isNotBug': 100},
        # {'programName': '塔的世界', 'allBug': 800, 'finishBug': 200, 'unWorkBug': 200, 'isNotBug': 100}
    ]

def tempUserCareerData(selectData: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [
        {'subject': '提交Bug数', 'A': 18000, 'fullMark': 30000},
        {'subject': '确认Bug数', 'A': 15000, 'fullMark': 30000},
        {'subject': '解决Bug数', 'A': 10000, 'fullMark': 30000},
        {'subject': '完善需求数', 'A': 5000, 'fullMark': 30000},
        {'subject': '用例条数', 'A': 20000, 'fullMark': 30000},
        {'subject': '脚本数量', 'A': 15000, 'fullMark': 30000}
    ]

def tempUserProBugDiff(selectData: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [
        {'program': '你好', 'level_1': 3, 'level_2': 10, 'level_3': 100, 'level_4': 200},
        {'program': '我好', 'level_1': 2, 'level_2': 20, 'level_3': 150, 'level_4': 300},
        {'program': '他好', 'level_1': 4, 'level_2': 30, 'level_3': 120, 'level_4': 250},
        {'program': '她好', 'level_1': 5, 'level_2': 15, 'level_3': 130, 'level_4': 270},
        {'program': '大家好', 'level_1': 1, 'level_2': 12, 'level_3': 160, 'level_4': 230},
        {'program': '你家好', 'level_1': 6, 'level_2': 13, 'level_3': 122, 'level_4': 290},
        {'program': '我家好', 'level_1': 8, 'level_2': 18, 'level_3': 143, 'level_4': 243}
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
