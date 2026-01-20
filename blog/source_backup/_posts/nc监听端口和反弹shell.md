---
title: nc监听端口和反弹shell
date: 2025-01-05 20:28:03
categories: WEB
tags: web
crated: 2026-01-20T15:50
updated: 2026-01-20T15:39
---

nc [-hlnruz] [-g<网关...>] [-G<指向器数目>] [-i<延迟秒数>] [-o<输出文件>] [-p<通信端口>] [-s<来源位址>] [-v...] [-w<超时秒数>] [主机名称] [通信端口...]

![](https://gitee.com/fogpost/photo/raw/master/202501052042662.png)

注意再使用nc的-l时连接成功不会有明显的回显，但是这个时候可能已经连接上了
![](https://gitee.com/fogpost/photo/raw/master/202501052046913.png)
![](https://gitee.com/fogpost/photo/raw/master/202501052047210.png)