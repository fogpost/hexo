---
title: PEcompact脱壳
categories: 逆向
date: 2024-09-12 14:59:07
tags: reverse
---
### PEcompact脱壳
 
![](http://gitee.com/fogpost/photo/raw/master/202409122017434.png)
>3   
BP VirtualFree
F9到达取消断点
![](http://gitee.com/fogpost/photo/raw/master/202409122017793.png)
返回到用户代码alt+f9
查找PUSH 8000
![](http://gitee.com/fogpost/photo/raw/master/202409122017787.png)
然后单步到达
![](http://gitee.com/fogpost/photo/raw/master/202409122017628.png)

>4  
BP VirtualFree
两次shift+f9到达
![](http://gitee.com/fogpost/photo/raw/master/202409122017209.png)
返回到用户代码alt+f9
![](http://gitee.com/fogpost/photo/raw/master/202409122017851.png)
然后单步跟踪到达oep

![](http://gitee.com/fogpost/photo/raw/master/202409122017705.png)
>5  
bp 0045DE74
运行,到达后取消断点
![](http://gitee.com/fogpost/photo/raw/master/202409122018701.png)
在retn处会返回并执行程序我们现在下面下个断点，然后单步到OEP
![](http://gitee.com/fogpost/photo/raw/master/202409122018935.png)
这一段汇编比较重要注意在retn后面加上断点

![](http://gitee.com/fogpost/photo/raw/master/202409122018816.png)
>6  
bp VirtualAlloc
shift+f9,取消断点,返回用户代码alt+f9
![](http://gitee.com/fogpost/photo/raw/master/202409122018918.png)
查找jump
![](http://gitee.com/fogpost/photo/raw/master/202409122018029.png)
单步到OEP

![](http://gitee.com/fogpost/photo/raw/master/202409122018091.png)

>7  取消异常
![](http://gitee.com/fogpost/photo/raw/master/202409122018128.png)
![](http://gitee.com/fogpost/photo/raw/master/202409122018041.png)
利用shift+f9,两次过后发现跑飞，利用第二次的SE句柄地址，（如果发现单词就跑飞了那是应为吾爱破解od中的插件strongod的过在option中将skip some Exception取消就行）  
![](http://gitee.com/fogpost/photo/raw/master/202409122019809.png)
查找句柄
![](http://gitee.com/fogpost/photo/raw/master/202409122018041.png)
![](http://gitee.com/fogpost/photo/raw/master/202409122019805.png)

![](http://gitee.com/fogpost/photo/raw/master/202409122019946.png)

>8  两次内存
注意对比跳跃代码
>9  at Getversion
到达OEP的下方
