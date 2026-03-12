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

目录扫描
feroxbuster --url "http://www.dav.dsz/" --wordlist
/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x
.git,.php,.html,.xml,.zip,.7z,.tar,.bak,.sql,.py,.pl,.txt,.jpg,.jpeg,.png,.js,.aa
c,.ogg,.flac,.alac,.wav,.aiff,.dsd,.mp3,.mp4,.mkv,.phtml -s 200 301 302