---
title: od脱壳脚本的使用与编写
date: 2024-10-29 22:44:22
categories: 逆向
tags: reverse
created: 2026-01-18T12:49
updated: 2024-10-29 22:44:22
---
# od脱壳脚本的使用与编写
我们的软件取自[52破解](https://www.52pojie.cn/thread-422100-1-1.html)
第一步查壳，并且丢到idapro中看看有什么
![](https://gitee.com/fogpost/photo/raw/master/202410292248198.png)  
可见这个软件是由tElock压缩过的
![](https://gitee.com/fogpost/photo/raw/master/202410292249831.png)  
Idapro也是不负众望的啥也没扫出来，我们od加载一下，这里注意看一下内存加载，基地址是400000，这代表了我们关闭了ALSR这点对我们后面的脱壳很重要
![](https://gitee.com/fogpost/photo/raw/master/202410292251590.png)  
在单步运行到这里时，我们程序会直接跑飞
![](https://gitee.com/fogpost/photo/raw/master/202410292253699.png)  
下断点键入后，逐步步过，发现出现下面这个弹窗，表示本程序是有程序自校验，这里有两个方法，一是找到自校验方式nop掉，二是在每次键入时将断点取消，这也是一个好习惯
![](https://gitee.com/fogpost/photo/raw/master/202410292254330.png)
看下图发现，此程序还有对调试器的检测，我们这里开启了od的内核插件，但是好像在win10不起作用，没有防止检测，可以选择用win7，来加载
![](https://gitee.com/fogpost/photo/raw/master/202410292303768.png)
我们重新加载文件，在此处发现对od检测的jmp函数我们将这个函数进行nop即可正常进入软件
![](https://gitee.com/fogpost/photo/raw/master/202410292321969.png)
如果刚刚没有nop那么我们在下面这个图便会跳转到exitprocess进程结束
![](https://gitee.com/fogpost/photo/raw/master/202410292321971.png)