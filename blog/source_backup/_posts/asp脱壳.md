---
title: asp脱壳
date: 2024-09-12 14:59:07
categories: 逆向
tags: reverse
updated: 2024-09-12 14:59:07
---
asp脱壳时利用
#### 模拟跟踪法
利用tc命令跟踪   
![](http://gitee.com/fogpost/photo/raw/master/image12.png)  
查找带有sfx和输入表的字段    
![](http://gitee.com/fogpost/photo/raw/master/image-1.png)  
这个方法由于时程序自动进行的所以十分缓慢不建议用  
#### SFX法
![](http://gitee.com/fogpost/photo/raw/master/image-3.png)
自动抵达
![](http://gitee.com/fogpost/photo/raw/master/image-4.png)
### nspack
巧妙脱壳法  
![](http://gitee.com/fogpost/photo/raw/master/image-5.png)  
at GetVersion  

下版本断点
![](http://gitee.com/fogpost/photo/raw/master/image-6.png)
在retn处下断点
单步F8之后到打OEP之后向前找OEP
![](http://gitee.com/fogpost/photo/raw/master/202409122015500.png)