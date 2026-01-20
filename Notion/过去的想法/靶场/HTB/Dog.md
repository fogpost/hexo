---
crated: 2026-01-18T12:49
updated: 2026-01-20T15:39
---
攻击机IP：172.18.94.245 内网tun0：10.10.14.130

靶机IP：10.10.11.58

openvpn连接上之后利用nmap扫描查看端口服务

```php
Starting Nmap 7.95 ( [https://nmap.org](https://nmap.org/) ) at 2025-03-13 10:31 CST
Nmap scan report for 10.10.11.58
Host is up (0.44s latency).
Not shown: 998 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.12 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   3072 97:2a:d2:2c:89:8a:d3:ed:4d:ac:00:d2:1e:87:49:a7 (RSA)
|   256 27:7c:3c:eb:0f:26:e9:62:59:0f:0f:b1:38:c9:ae:2b (ECDSA)
|_  256 93:88:47:4c:69:af:72:16:09:4c:ba:77:1e:3b:3b:eb (ED25519)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
| http-git:
|   10.10.11.58:80/.git/
|     Git repository found!
|     Repository description: Unnamed repository; edit this file 'description' to name the...
|_    Last commit message: todo: customize url aliases.  reference:[https://docs.backdro](https://docs.backdro/)...
|_http-title: Home | Dog
|_http-generator: Backdrop CMS 1 ([https://backdropcms.org](https://backdropcms.org/))
|*http-server-header: Apache/2.4.41 (Ubuntu)
| http-robots.txt: 22 disallowed entries (15 shown)
| /core/ /profiles/ /README.md /web.config /admin
| /comment/reply /filter/tips /node/add /search /user/register
|*/user/password /user/login /user/logout /?q=admin /?q=comment/reply
Device type: general purpose
Running: Linux 5.X
OS CPE: cpe:/o:linux:linux_kernel:5
OS details: Linux 5.0 - 5.14
Network Distance: 2 hops
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE (using port 110/tcp)
HOP RTT       ADDRESS
1   359.70 ms 10.10.14.1
2   361.61 ms 10.10.11.58

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 311.74 seconds
```

看出存在80和22端口开启，存在.git 下载文件，linux5内核系统，Backdrop CMS服务

访问以下对应的服务页面，发现存在登录端口，同时尝试对文件目录的扫描，发现以下这些重要的配置文件

!![[image 17.png]]

!![[image 18.png]]

!![[image 19.png]]

利用git-hacker将文件下下来，利用命令查询对应的信息

获取