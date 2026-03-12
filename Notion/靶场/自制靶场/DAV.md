## 信息收集
nmap扫描ip，发现22、80、6065端口，借助提示了解6065为dva服务端口，需要挂载
```
┌──(root㉿kali)-[/home/kali]
└─# nmap -sS -sV -T4 -p- 172.25.85.96      
Starting Nmap 7.95 ( https://nmap.org ) at 2026-03-12 00:09 EDT
Nmap scan report for 172.25.85.96
Host is up (0.00092s latency).
Not shown: 65532 closed tcp ports (reset)
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 10.0 (protocol 2.0)
80/tcp   open  http    Apache httpd 2.4.66
6065/tcp open  http    Golang net/http server
```

