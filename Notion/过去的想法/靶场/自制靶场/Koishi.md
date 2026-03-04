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
文件探测发现phpinfo（）
