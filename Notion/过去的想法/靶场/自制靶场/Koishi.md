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

利用/proc/3473/fd/5获取到文件句柄
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