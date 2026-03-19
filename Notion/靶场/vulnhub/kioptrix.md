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
发现Samba，尝试利用Metasploit


