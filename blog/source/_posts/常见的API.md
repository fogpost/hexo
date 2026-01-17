---
title: 常见的API
date: 2024-09-27 10:24:18
categories: 逆向
tags: reverse
---
### 常见的API接口查找方法
写一些常见的API以后每次遇见我都会抄下来，写一下相关的解释和什么时候可以用到
我们要有一个想法，凡是这些api我们都知道这些都是系统所写好的东西，动态链接库给我们准备好的接口，就像c语言导入的头文件，但是很多强者也可能根本就不屑这些api自己实现，那么我们就完蛋了，但是也可以根据可能编写的代码，下断点，逆向本质就是由汇编看代码

#### od快速查找
突然发现od早就有古人创建的api断电器了，可喜可贺可喜可贺
![](https://gitee.com/fogpost/photo/raw/master/202409201016637.png)
#### od的命令行断点
![](https://gitee.com/fogpost/photo/raw/master/202409201018652.png)
#### 模块名称查找
![](https://gitee.com/fogpost/photo/raw/master/202409201018703.png)
![](https://gitee.com/fogpost/photo/raw/master/202409201019644.png)



### 常见的api
#### MessageBoxA
这个人尽皆知，在出现类似登录的窗口时当我们选择登录按键时便会发现，有弹窗便可以在此api下断点，到达判断位置

#### GetwindowsTestA
这个的话是在登录窗口无明显回显时使用的方法可以获取我们的窗口输入文本

#### 易语言的窗口特征ID
看到004012AC这句代码 PUSH  5201008了吗
PUSH 10001，告诉你，这个是易语言通用的，每个窗口ID语句上面都会有一个PUSH 10001

#### Openfile
打开文件的api构建，用到再说

#### GetDlgItemInt
将获取的文本转化为整数

#### SetWindowsTextA
将某个窗口或者字段中的文字进行设定所调用的api窗口哦


### 主要的dll
看样子我后面还要了解一下，这些api在那些dll里面了

kernel32.dll、user32.dll、gdi32.dll