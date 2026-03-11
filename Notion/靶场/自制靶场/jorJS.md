## 信息获取
得到ip为127.0.1.1
```
┌──(root㉿kali)-[/home/kali/Downloads]
└─# nmap -sS -sV -A -p- 127.0.1.1         
Starting Nmap 7.95 ( https://nmap.org ) at 2026-03-11 05:31 EDT
Nmap scan report for kali (127.0.1.1)
Host is up (0.000061s latency).
Not shown: 65534 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.9p2 Debian 1 (protocol 2.0)
| ssh-hostkey: 
|   256 a8:d0:e4:b8:29:16:48:11:7b:95:e1:93:0a:47:98:0b (ECDSA)
|_  256 a3:fc:96:d5:d3:4b:20:52:a8:2a:20:49:29:1b:8d:4d (ED25519)
Device type: general purpose
Running: Linux 2.6.X|5.X
OS CPE: cpe:/o:linux:linux_kernel:2.6.32 cpe:/o:linux:linux_kernel:5 cpe:/o:linux:linux_kernel:6
OS details: Linux 2.6.32, Linux 5.0 - 6.2
Network Distance: 0 hops
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 3.34 seconds

```
发现nmap还有带了一个名为 **NSE (Nmap Scripting Engine)** 的脚本引擎。它可以自动执行漏洞扫描、暴力破解甚至服务识别
```
sudo nmap -p 22 --script ssh-auth-methods,ssh-run,ssh-brute 127.0.1.1
`sudo nmap -p 22 --script ssh2-enum-algos,ssh-hostkey 127.0.1.1` 
这会列出服务器支持的加密算法，帮助你判断是否存在过时的、弱对称加密算法（如 3DES 或 RC4）。
```
A:ssh-auth-methods 认证方式探测,支持哪些登录方式
- 如果返回 `password`，说明支持密码登录（易被暴力破解）。
- 如果只返回 `publickey`，说明服务器非常安全，只允许密钥登录。
- 如果返回 `keyboard-interactive`，通常意味着可能开启了多因素验证 (2FA)。
B:`ssh-run` (命令执行测试)
- **作用**: 这个脚本尝试在远程主机上运行简单的命令。
- **注意**: 它通常需要你提供凭据（用户名/密码）。如果不提供，它主要用于检测某些特定配置下是否存在未经授权执行命令的风险。
C: **`ssh-brute` (暴力破解模拟)**
- **作用**: 它是 Nmap 内置的“破门工具”。它会自动调用 Nmap 自带的简单用户名和密码字典，尝试登录你的 SSH 服务。
- **实验价值**:  
    - 如果你设置的密码太简单（如 `123456` 或 `password`），这个脚本会直接在扫描结果中显示出你的明文密码。
    - 这是提醒管理员“弱口令危害”最直观的方式。
```
PORT   STATE SERVICE
22/tcp open  ssh
|_ssh-run: Failed to specify credentials and command to run.
| ssh-auth-methods: 
|   Supported authentication methods: 
|     publickey
|_    password
| ssh-brute: 
|   Accounts: No valid accounts found
|_  Statistics: Performed 114 guesses in 601 seconds, average tps: 0.2

```
