子网后缀过长导致扫描速度变慢的方法
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

- **Discover the target:** `arp-scan` or `netdiscover`.  
    找出目标： `arp-scan` 或 `netdiscover` 。
- **Fingerprint services:** `nmap` (with scripts and version detection).  
    指纹服务： `nmap` （带脚本和版本检测）。
- **Web recon:** browser + Nikto + Gobuster.  
    网络侦察：浏览器 + Nikto + Gobuster。
- **Exploit and prove:** searchsploit, Metasploit (optional), Hydra for logins.  
    利用并验证：searchsploit、Metasploit（可选）、Hydra 用于登录。