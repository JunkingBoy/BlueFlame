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
