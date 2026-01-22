---
title: web安全流程
date: 2024-11-15 22:33:26
tags:
updated: 2024-11-15 22:33:26
---
作者：Ph0rse
链接：https://www.zhihu.com/question/267204109/answer/320502511
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

一、前期一系列的练习平台，大部分都有题解，实在十几天弄不出来可以看看题解。    
SQL注入：RedTiger's Hackit    
web:网络安全实验室|网络信息安全攻防学习平台  
综合：[WeChall]   
Challenges经典老平台：南京邮电大学网络攻防训练平台  
综合性新平台：CTF - 练习平台  
渗透：Penetration test lab   
综合性黑客game：Game of Hacks  
XCTF的训练平台：XCTF实训平台 | 登 录  
I春秋的CTF复现平台：https://www.ichunqiu.com/racing/58837  
安恒的平台：登录 - 明御® 攻防实验室  
一个综合的新平台，貌似里面二进制的题挺好：Jarvis OJ
一个高端平台，里面有一些硬件、云安全、内网渗透的题：Exploit Exercises  
又一个高端平台，里面有一些Oracle、密码学之类的题目：Under the Wire  
渗透练习平台：https://pentest.training/mockexams.php
一个代码审计的平台（不是web方向，有很多都是C语言的审计，墙裂建议女装大佬来秒）：Websec  
一个封装好的CTF平台：Vulnerable Docker VM - NotSoSecure  
也是封装好的一些训练环境：Vulnerable By Design ~ VulnHub  
PHP安全训练平台：PHP Security Advent Calendar 2017  
一个国外的CTFwiki，质量好像一般:Forgotten Security’s CTF Wiki  
一个和Metasploit配套的靶场---Metasploitable： http://downloads.metasploit.com/data/metasploitable/metasploitable-linux-2.0.0.zip  
CTF工具库： CTF资源库|CTF工具下载|CTF工具包|CTF工具集合  
以上是我自己整理的内容，同时推荐其它大佬的资源整理贴
~个人总结-网络安全学习和CTF必不可少的一些网站 - ida0918的博客 - CSDN博客  

二、中期打一些有奖金的CTF比赛，一些优质的CTF比赛还是比较贴近实战的，比如17年的HCTFCTF时间表：  
XCTF比赛的时间表：首页 - XCTF社区  
大型比赛的时间表：All about CTF (Capture The Flag)  
CTF指南：CTF Rank，你的CTF参赛指南  
CTFwiki：墙裂推荐！CTF Wiki 
2018年的CTF竞赛 2018·CTF·信息安全竞赛导航  

一些CTF大佬的博客：
Hackfun - | Secblog | Pentest | Auditing | Sectool | CTF Write-up  
Go0s @ 老 锥  
Swing'Blog 有恨无人省  
http://haojiawei.xyz/page/3/  
pcat - 博客园  
Si1ence's Blog - 雨一落，化开我眼中的冰，蔓延成河。  
Medici.Yan's Blog  
Radiation's blog  
http://l-team.org/  
Sebastian Neef - 0day.work  
https://www.jimwilbur.com/  
M4x - 博客园  
当然，也不要仅仅局限于CTF比赛，多用docker去复现一些CVE环境，自己玩玩儿，再跟着P神学一下代码审计，不要拿到别人网站源码还不知道怎么getshell~一些闭源的cms，很容易审出洞。

这里在推荐一下p神的一个项目，用docker-compose去一键复现漏洞环境。

vulhub/vulhub首页 | 离别歌vulhub/vulhub

三、后期那些刻意的环境已经满足不了你了，去实战吧
日常关注着漏洞预警：Exploits Database by Offensive Security  
瞄准相关漏洞之后，用shodan去进行漏洞全球主机探测：Shodan Manual · GitBook  
先知安全服务平台  
漏洞银行(BUGBANK) 官方网站 | 全球领先的漏洞发现平台  
补天 - 企业和白帽子共赢的漏洞响应平台，帮助企业建立SRC，库带计划 - 国内首个现金奖励漏洞平台  
一些非法网站，比如黄网、赌博网站也可以用来练手，反正是它们也是违法的，但不要去谋取利益就好。  
大陆政府的网站绝对不要碰。如果心痒痒就去搞国外zf的，因为他们的人也在搞咱们政府的练手。  

作者：Ph0rse
链接：https://www.zhihu.com/question/267204109/answer/320502511
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
