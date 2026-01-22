---
title: dvwa全解
date: 2024-11-23 12:35:02
tags: dvwa
categories: 渗透测试
updated: 2024-11-23 12:35:02
---
# 简介
说到靶机，那么经典的dvwa靶机肯定不能错过，它是一款非常适合新手入门的靶机，它集成了多种漏洞，并且可以自由选择难度，非常适合新手入门，想玩的话自己搭建就好，我这是在服务器上搭的，用来玩玩

## Low
### Brute Force
随便输入后便是这个返回值，说明密码错误
![](https://gitee.com/fogpost/photo/raw/master/202411231240412.png)
我们用抓包软件抓包，然后发送到repeat，yakit的爆破采用的是文件标签，原理是和bp一样的对字典有要求,利用响应的大小来判断正误
![](https://gitee.com/fogpost/photo/raw/master/202411261753518.png)
![](https://gitee.com/fogpost/photo/raw/master/202411261806101.png)

### command injection
直接在ip查询后面加入的命令执行，可怕可怕，cat也可以执行
![](https://gitee.com/fogpost/photo/raw/master/202411261810028.png)
![](https://gitee.com/fogpost/photo/raw/master/202411261811659.png)

### CSRF
抓取原来修改密码的报文后在yakit中修改略微，重放便可以修改密码，也可以将网址修改一部分再重放，同样修改成功
![](https://gitee.com/fogpost/photo/raw/master/202411261817959.png)
![](https://gitee.com/fogpost/photo/raw/master/202411261818130.png)
这个过程有个技巧就是长链变短链，利用站长工具即可实现，防止社工时让受击者发现
![](https://gitee.com/fogpost/photo/raw/master/202411261824846.png)
还可以页面构造

### XSS(DOM)
查看页面源码，没有php代码，仅有js代码，我们可以利用js脚本
![](https://gitee.com/fogpost/photo/raw/master/202411261914977.png)
点击英文发现，存在一个明文网址，我们可以利用这个English来做个文章
>http://110.41.22.24/vulnerabilities/xss_d/?default=English

>http://110.41.22.24/vulnerabilities/xss_d/?default=\<script>alert('xss')\</script>

![](https://gitee.com/fogpost/photo/raw/master/202411261906137.png)

### XSS(Reflected)
反射式XSS，查看源码，同上只不过这次是在输入框中进行反射
![](https://gitee.com/fogpost/photo/raw/master/202411261914096.png)
>\<script>alert('xss')\</script>

拿cookie
>\<script>alert(document.cookie)\</script>
![](https://gitee.com/fogpost/photo/raw/master/202411261911735.png)
