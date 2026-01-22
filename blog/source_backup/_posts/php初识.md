---
title: php函数初识
date: 2024-09-30 10:11:50
category: 网络
tags: php
updated: 2024-09-30 10:11:50
---
本文讲对php的部分可能引起漏洞的部分函数进行讲解
<!--more-->
# php函数初识
## 1. phpinfo()
phpinfo() 函数会显示 PHP 配置信息以及当前的 PHP 环境信息，包括服务器信息、操作系统信息、PHP 版本、已安装的扩展、环境变量等。这个函数通常用于调试和开发过程中查看 PHP 配置信息。

## 2. eval()
eval() 函数会将传入的字符串作为 PHP 代码进行执行。如果传入的字符串包含恶意代码，eval() 函数将会执行这些恶意代码，从而可能导致代码注入漏洞。
```php
>>>x = 7
>>> eval( '3 * x' )
21
>>> eval('pow(2,2)')
4
>>> eval('2 + 2')
4
>>> n=81
>>> eval("n + 4")
85
```
## 3. preg_replace()
preg_replace() 函数用于执行正则表达式替换操作。如果正则表达式不正确或者传入的替换字符串包含恶意代码，preg_replace() 函数将会执行这些恶意代码，从而可能导致代码注入漏洞。

## 4. include() 和 require()
- incluce 在用到时加载
include 的文件中出错了，主程序继续往下执行
- require 在一开始就加载
require 的文件出错了，主程序也停了
- _once 后缀表示已加载的不加载 

## 5. file_get_contents()
file_get_contents() 函数用于读取文件内容。如果传入的文件路径包含恶意代码，file_get_contents() 函数将会执行这些恶意代码，从而可能导致代码注入漏洞。

## 6. system()
system() 函数用于执行系统命令。如果传入的命令包含恶意代码，system() 函数将会执行这些恶意代码，从而可能导致命令注入漏洞。

## 7. exec()