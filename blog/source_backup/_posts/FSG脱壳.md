---
title: MSG脱壳过程中的IAT修复
categories: 逆向
date: 2024-09-12 14:59:07
tags: reverse
---
### FSG脱壳过程中的IAT修复
进行手动查找和IAT修复
找可以在动态连接库中查得到的call
![](https://gitee.com/fogpost/photo/raw/master/202409122016001.png)
在命令行中敲425210然后查连接库函数
![](https://gitee.com/fogpost/photo/raw/master/202409122016599.png)  
向上向下查找为0的数值(分割处)
![](https://gitee.com/fogpost/photo/raw/master/202409122016253.png)
![](https://gitee.com/fogpost/photo/raw/master/202409122016865.png)  
手动修改RVA和size的值  
![](https://gitee.com/fogpost/photo/raw/master/202409122016959.png)