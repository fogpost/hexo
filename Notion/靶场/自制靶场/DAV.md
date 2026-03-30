之前主要是被网桥卡住了，现在配好可以快点打

## 信息收集
我只扫出这几个
```bash
┌──(kali㉿kali)-[~]
└─$ nmap -p- 192.168.56.3 
Starting Nmap 7.95 ( https://nmap.org ) at 2026-03-30 04:07 EDT
Nmap scan report for www.dav.dsz (192.168.56.3)
Host is up (0.00089s latency).
Not shown: 65532 closed tcp ports (reset)
PORT     STATE SERVICE
22/tcp   open  ssh
80/tcp   open  http
6065/tcp open  winpharaoh
MAC Address: 08:00:27:34:4D:CA (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
```
查看页面导向http://www.dav.dsz/。发现虚拟主机改/etc/hosts，
文件爆破发现about.html,查看文件,发现页面迁移到dev.dav.dsz，查看对应域名
> [04:13:16] 200 -    3KB - /about.html
```
System Administrator Note:
系统管理员说明：
The internal mount point for development assets has been migrated to the dev.dav.dsz sub-domain. Please update your local mapping scripts accordingly.
开发资产的内部挂载点已迁移到 dev.dav.dsz 子域。请相应更新您的本地映射脚本。
```
加hosts ip dev.dav.dsz
![image.png](https://gitee.com/fogpost/photo/raw/master/202603301624906.png)
目录爆破
> [04:27:20] 200 -   56KB - /test.php

猜测6065是这个域名的端口利用
curl -v -X options http://dev.dav.dsz:6065/ 来看响应报文，查看页面需要账户密码尝试爆破
```html
* Host dev.dav.dsz:6065 was resolved.
* IPv6: (none)
* IPv4: 192.168.56.3
*   Trying 192.168.56.3:6065...
* Connected to dev.dav.dsz (192.168.56.3) port 6065
* using HTTP/1.x
> options / HTTP/1.1
> Host: dev.dav.dsz:6065
> User-Agent: curl/8.12.1
> Accept: */*
> 
* Request completely sent off
< HTTP/1.1 401 Unauthorized
< Content-Type: text/plain; charset=utf-8
< Www-Authenticate: Basic realm="Restricted"
< X-Content-Type-Options: nosniff
< Date: Mon, 30 Mar 2026 08:30:00 GMT
< Content-Length: 15
< 
Not authorized
* Connection #0 to host dev.dav.dsz left intact
```
找到密码admin:qwertyuiop
![image.png](https://gitee.com/fogpost/photo/raw/master/202603301723530.png)
了解到这个dav是有挂载文件的
cadaver http://dev.dav.dsz:6065/
