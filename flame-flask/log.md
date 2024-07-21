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
# 2024-06-29

1. case log 记录 case 更改
```python
case_log
    case_id: int
    before: json({"name": "value", ...}) 
    after: json({"name": "value", ...})
    user_id: xcx
    modify_time: 
```





### plan 2024-07-05

<!-- ------------------------------------------------------------------------- -->
plan CRUD
<!-- ------------------------------------------------------------------------- -->
create_plan(POST):
	input: {
		project_id: int
		plan_name: str
		start_time: date
		end_time: date
		user_id: from jwt
	}
	output: {
		"data": <plan_id: int> if success else <error_msg: str>
	}
	
modify_plan(PUT):
	input: {
		plan_name: str
		start_time: date
		end_time: date
	}
	output: {
		"msg": str
	}

delete_plan(DELETE):
	input:  {
		plan_id: int
	}
	output: {
		"msg": str
	}

all_plan(GET):
	input: {
		user_id: from jwt
		project_id: int
	}
	output: {
		"data": [
			{
				"plan_id": int,
				"plan_name": str,
				"start_time": date,
				"end_time": date,
				"case_ids": list<int>,
			}	
			...
		]
	}

<!-- ------------------------------------------------------------------------- -->
about plan'case CRUD
<!-- ------------------------------------------------------------------------- -->

append_plan_case(POST):
	i: {
		plan_id: int
		case_ids: list<id: int>
	}
	o: {
		 "msg": str
	}
	
delete_plan_case(DELETE):
	i: {
		plan_id: int
		case_ids: list<id: int>
	}
	o: {
		 "msg": str
	}
	

modify_plan_case(PUT):
	I: {
		plan_id: int
		case_ids: list<int>
	}
	o: {
		"msg": str
	}

获取一个项目下的一个plan下的所有case
get_plan_case(GET):
	i: {
		plan_id: int
	}
	o: {
		"data": [
			{
				"plan_case_id": int,
				"case_name": str,
				"case_type": str,
				"case_detail": str,
			}
			...
		]
	}







-------------------------------------------------------------------------

<!-- case CRUD  -->

-------------------------------------------------------------------------

creage_case(POST):
	input: {
		case_type: str
		case_detail: json
		user_id: from jwt
		project_id: int
		plan_id: int
	}
	output: {
		
	}
	
modify_case(PUT):
	input: {
		case_id: int
		case_detail: json
	}
	output: {
		"msg": str
	}

delete_case(DELETE):
	input:  {
		case_id: int
	}
	output: {
		"msg": str
	}

all_case(GET):












<!-- ------------------------------------------------------------------------- -->
plan 相关的数据表设计
<!-- ------------------------------------------------------------------------- -->

<!-- done -->
project表:
	id: int
	project_id: int, 
	project_name: str, 
	project_desc: str,
	is_init: bool, 
	creator: str,
	create_time: date, 
	update_time: date

project_plan表:


plan表: 
	id: int
	project_id: int
	plan_name: str
	start_time: date
	end_time: date
	user_id: str
	create_time: date
	update_time: date

plan_case表:
	id: int
	plan_id: int
	case_id: int json                   #_tag_case_id_list
	create_time: date
	update_time: date

case表:
	id: int
	id_by_user: str    		# 这个字段记录为一个hash值 -> 在初始化case的时候生成字段 -> 先id后id_by_user
	case_type: str                #enum{func_case, api_case}
	case_detail: json             #_tag_case_detail -> 源数据
	case_hash: str # 参考git这一块的设计,git是如何识别两次提交的不同的内容
	user_id: str					# init_user
	project_id: int                # for_project
	create_time: date
	update_time: date

user表:
	id: int
	user_id: str, 
	phone: str
	pwd: str
	create_time: date, 
	update_time: date

project_user表:
	id: int
	project_id: int
	user_id: str
	update_time: date

 
<!-- ------------------------------------------------------------------------- -->
备注
case_detail_tag:

	func_case
	{
		"case_num": str,
		"case_name": str,
		"test_env": str,
		"case_module": str,
		"case_condition": str,
		"case_step": str,
		"case_expect": str,
		"case_actual": str,
		"create_time": date
	},

	api_case
	{
		"api_name": str,
		"api_url": str,
		"api_method": str,
		"api_params": str,
		"api_return": str,
		"api_desc": str,
	}
	
	
_tag_case_id_list:
	[case_id1, case_id2, ...]
<!-- ------------------------------------------------------------------------- -->


时间格式: 建议使用ISO 8601格式
ISO 8601 格式的示例：
```text
仅日期：2024-07-01
日期和时间（24小时制）：2024-07-01T12:00:00
日期和时间（带时区）：2024-07-01T12:00:00+00:00

```


# 2024-07-16

## 一个项目下的所有的 case 信息
url: /project/case/info
i: {
	"project_id": int
}
o: {
	"data": [
		{
			"case_id_by_user": str,
			"case_name": str,
			"case_type": str,
			"case_detail": str,
			"case_state": str,
			"create_time": date,
			"update_time": date,
		}, 
		...
	]
}

## plan 创建
url: /project/plan/create
i: {
	"project_id": str,
	"plan_name": str,
	"start_time": date,
	"end_time": date,
	"case_ids": list<case_id: str>
}
o: {
	"msg": str
}
logic:  
	1. 创建 plan_id: str, 根据 user_id + plan_name, sha256


## bug
1. 上传解析 Excel, case_id_by_user: int, 实际需要 str, 出现类型错误
2. excel 去除update_time
3. excel create_time 不需要时间, 只需要日期,  datetime   date, 

# 20240718

## User重构

### 表字段重构

user表:
	id: int
	user_id: str -> phonehash生成
	user_name: str -> 用户phone(如:用户18785452131) 
	phone: str -> 账号,区别不同用户的核心
	pwd: str
	create_time: date, 
	update_time: date

#### 提供api

- 注册api
- 登录api
- 修改api
	- 可修改用户名、密码
	- 原密码、修改密码、确认密码

# 20240720

### Case表重构

Case的需求:
1、首先.case是源数据.只针对project级别下的case进行修改的记录
2、project下的case的级别类似master分支.在git当中master分支通过设置规则进行保护.在这里则直接把第一次提交的case作为master分支.
3、git当中在规则条件下提交pr进行合并.这里通过创建plan.执行了plan以后提交pr进行合并.每一个plan类似一个commit.提交合并要记录plan_id作为commit的id
