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







