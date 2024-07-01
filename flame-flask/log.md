## 2024-06-20

###  feature

1. 讨论 home 页面需要的字段, 字段的交互和来源
2. Excel 上传功能的设计和实现
3. api 


## 需求返回的 api response json

### 项目
#### 1. 录入项目
url: /project/create
input:  {
	data: {
		project_name: str
		project_descript: str
		start_time: datetime
		end_time: datetime
	}
}
output:  {
	code: int
	data: any
	msg: str
}

#### 2. 查询现有项目
url: /project/
input:  {
	data: {
	}
}
output: {
	code: int
	data: [
		{
			project_id: int
			project_name: str
			project_descript: str
			start_time: datetime
			end_time: datetime
		}, 
		{
			project_id: int
			project_name: str
			project_descript: str
			start_time: datetime
			end_time: datetime
		}, 
	]
	msg: str
} 

#### Excel field
required:
	1.  模块
	2.  实际结果(enum(0: fail, 1: pass))
	3.  状态(enum (0: 待审查, 1: 通过审查, 2: 待执行) )
	4.  修改时间
option:
	1.  前置条件
	2.  测试内容
	3.  测试步骤
	4.  预期结果
	5.  原因
	6.  备注


### case 

#### 1. 上传用例
url : /case/upload
input: {
	project_id: int
	case_type: int
	data: {
		file: Excel(bytestream)
		<!-- user_id: int(from token) -->
	}
}
output: {
	code: int
	data: {}
	msg: str
} 

#### 2. 查询用例

```python
url: /case/search
input: {
	project_id: int
	case_type: enum(0: all, 1: func_case, 2: api_case, 3: ui_case)
}
output: {
	code: int
	data: {
		func_case: [
			{
				case_id: int
				case_name: str
				case_descript: str
				before_step: str
				...
			}, 
			{
				case_id: int
				case_name: str
				case_descript: str
				before_step: str
				...
			}			 
		], 
		ui_case: [

	 	], 
		api_case: [

	 	], 
		automatic_case: [

	 	]
	}
	msg: str
} 
```

3. 



TODO<2024-06-20, @xcx>  熟悉 flask, 代码模块化 


##  表设计

### 1. project
id: int pk
project_id: int   auto_increase  项目编号
project_name: str(256)   项目名称   wechat_3a: 1     wechat_3b   ...	
project_descript str(1024)   项目描述
start_time: datetime
end_time: datetime
create_time: data timestamp with zone utc 
update_time: data timestamp with zone utc

### 2. case_base
id: int pk
base_case_id: int 
user_id: int fk
source: str(256)  用例来源 import
dirty: bool  是否是已覆盖?
delete: bool  软删除
project_id: int fk
state: int 待审核  待执行  已执行 已废弃 
case_create_time: data timestamp with zone utc 
case_update_time: data timestamp with zone utc

### 3. func_case
id : int pk
case_name: str(256)
case_descript: str(1024)
before_step: str(1024)
base_case_id: int fk case_base


### 4. api_case
id: int pk
caseid: int 
script: str(1024)  api 脚本




### database design

To record test cases in a database, you can design a table with the following columns:

1. **Test Case ID**: A unique identifier for each test case.
2. **Test Case Name**: A descriptive name for the test case.
3. **Test Case Type**: A field to indicate the type of test case (e.g., functionality, UI).
4. **Test Case Description**: A detailed description of the test case.
5. **Test Steps**: The steps to execute the test case.
6. **Expected Results**: The expected results of the test case.
7. **Actual Results**: The actual results of the test case.
8. **Status**: The status of the test case (e.g., pass, fail).
9. **Assigned To**: The person responsible for executing the test case.
10. **Created Date**: The date when the test case was created.
11. **Last Updated Date**: The date when the test case was last updated.

You can create additional columns based on your specific requirements. This table structure will allow you to store and manage different types of test cases in your database effectively.


```python
@app.route('/func_case', methods=['POST'])
def create_func_case():
	data = request.json
	func_case = FuncCase(func_detail=data['func_detail'])
	db.session.add(func_case)
	db.session.commit()
	return jsonify(func_case.to_dict()), 201

@app.route('/func_case/<int:id>', methods=['GET'])
def get_func_case(id):
	func_case = FuncCase.query.get(id)
	if func_case is None:
		return jsonify({'message': 'FuncCase not found'}), 404
	return jsonify(func_case.to_dict())

@app.route('/func_case/<int:id>', methods=['PUT'])
def update_func_case(id):
	func_case = FuncCase.query.get(id)
	if func_case is None:
		return jsonify({'message': 'FuncCase not found'}), 404
	data = request.json
	func_case.func_detail = data['func_detail']
	db.session.commit()
	return jsonify(func_case.to_dict())

@app.route('/func_case/<int:id>', methods=['DELETE'])
def delete_func_case(id):
	func_case = FuncCase.query.get(id)
	if func_case is None:
		return jsonify({'message': 'FuncCase not found'}), 404
	db.session.delete(func_case)
	db.session.commit()
	return jsonify({'message': 'FuncCase deleted'})
```
 
 
 
```python
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Case(Base):
	__tablename__ = 'case'
	id = Column(Integer, primary_key=True)
	type = Column(String(50))
	
	__mapper_args__ = {
		'polymorphic_identity':'case',
		'polymorphic_on':type
	}

class FuncCase(Case):
	__tablename__ = 'func_case'
	id = Column(Integer, ForeignKey('case.id'), primary_key=True)
	func_detail = Column(String(100))  # FuncCase特有的字段
	
	__mapper_args__ = {
		'polymorphic_identity':'func_case',
	}

class ApiCase(Case):
	__tablename__ = 'api_case'
	id = Column(Integer, ForeignKey('case.id'), primary_key=True)
	api_detail = Column(String(100))  # ApiCase特有的字段
	
	__mapper_args__ = {
		'polymorphic_identity':'api_case',
	}
	
```

读取成字典
```python
# 确保已安装 pandas 和 openpyxl
# 读取 Excel 文件
try:
    df = pd.read_excel('/Users/xcx/WorkSpaces/BlueFlame/flame-flask/static/func_case_template.xlsx', engine='openpyxl')
    df = df.to_dict()
    # 查看数据
    for k, v in df.items():
        print(type(k))
        print(type(v))
        print(k, v)
        print('-'*80)
except Exception as e:
    print("Error occurred while reading Excel file:", str(e))
```


# 20240701
### 确定事项

##### project表字段更改

加入is_delete字段 -> project表
提供删除功能 -> 前端(double check)
case表字段尽量不变
case_log -> before和after

必做:
1、fix掉获取用例模板不同浏览器拿不到后缀名的bug
2、提供编辑项目信息api
	1、更改项目名称
	2、更改项目描述
3、修改/project/user/case/all接口.返回project_id


暂定:
1、项目邀请码邀请用户加入项目
	1、生成project_id项目邀请链接
	2、用户点击以后请求api确认用户是否注册
		1、用户未注册，跳转到注册页面
		2、用户已注册，跳转到项目页面
