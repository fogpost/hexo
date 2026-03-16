## 网络安全三要素
CIA:
- Confidentiality（保密性）
- Integrity（完整性）
- Availability（可用性）

- 哪些攻击破坏完整性？
- SQL注入破坏什么？

## 常见端口
21 FTP
22 SSH
23 Telnet
25 SMTP
53 DNS
80 HTTP
443 HTTPS
3306 MySQL
6379 Redis

## TCP三次握手
SYN  
SYN + ACK  
ACK

为什么三次？
SYN Flood 原理？

## Web漏洞
### XSS
反射型、存储型、DOM型
可能问：XSS本质、如何防御、XSS蠕虫

### CSRF
原理
如何防御
token机制
same-site cookie
referer验证
### SSRF
攻击内网
打Redis
打Docker API
读取metadata

### 如何绕过上传检测
双写
大小写
00截断
MIME绕过

## 渗透测试流程
信息收集
漏洞扫描
漏洞利用
权限维持
内网横向
清理痕迹
### 信息收集工具
nmap
whatweb
dirsearch
fofa
shodan
### Web工具
burpsuite
sqlmap
xray
awvs

## linux安全
SUID
sudo
计划任务
内核漏洞
PATH劫持

### 常见命令
find
grep
chmod
chown
ps
netstat

## 内网渗透
### 内网横向
psexec
wmiexec
smbexec

### 凭证获取
mimikatz
hashdump
lsass

### 横向移动
pass the hash
pass the ticket

## 代码审计
### PHP危险函数
eval
system
exec
assert
passthru
###  变量覆盖
extract()
parse_str()

### 代码审计思路
输入点
危险函数
过滤绕过
漏洞利用

## 漏洞挖掘
你挖过什么漏洞？
有没有CVE？

## 自动化
写过扫描工具吗？
写过POC吗？

## 技术方向
SAST (静态应用安全测试)**在不运行程序的情况下，通过分析源代码来发现漏洞**。
SAST是通过静态分析源代码来发现漏洞，通常使用AST和污点分析技术追踪用户输入是否流入危险函数，例如SQL执行函数、命令执行函数等，从而发现SQL注入、XSS、命令执行等漏洞。
无法确定真实执行路径


DAST（动态应用安全测试）运行程序后，通过发送请求来检测漏洞
DAST是在应用运行状态下，通过模拟攻击请求来检测漏洞，例如SQL注入和XSS，通常通过扫描器发送payload观察返回结果来判断漏洞是否存在

IAST（交互式应用安全测试）SAST + DAST
IAST是在应用运行时通过Agent监控程序执行路径，结合动态请求和代码执行信息检测漏洞，因此误报率比SAST低，覆盖率比DAST高。

Fuzz（模糊测试）
Fuzzing是一种通过大量随机或变异输入测试程序稳定性的技术，通过触发程序崩溃或异常来发现漏洞，常用于发现缓冲区溢出、UAF等内存漏洞。
随机输入 → 未覆盖路径

++
模糊测试  
符号执行  
污点分析

SDL
DevSecOps
SAST

未来发展方向
为什么做安全
你最大的漏洞经验






















