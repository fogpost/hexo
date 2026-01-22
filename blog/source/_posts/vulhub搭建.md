---
title: vulhub搭建
date: 2024-11-21 19:22:56
categories: 工具
tags: tool
updated: 2024-11-21T19:22:56+08:00
---
# 简介
涉及一些经典的漏洞和靶场环境，如果有现成的可以下载固然很好，但是当需要我们自己复现和搭建环境时便会出现许多的bug，这时便需要一个较好的工具来实现便捷的靶场环境构建，这个工具便是vulhub，它是一个基于docker的漏洞环境集合，方便我们快速搭建漏洞环境，作者是p牛也是人尽皆知的离别歌，可以去看看人家的博客网

# 安装
vulhub是个基于docker的工具平台，自行下载docker和docker-compose

## 下载Vulhub
任意创建一个文件夹,从github获取对应的靶场环境,然后进入vulhub目录
>git clone https://github.com/vulhub/vulhub.git
cd vulhub

随便进入一个目录,比如shiro,ls+cd进入想要的cve文件中启动docker-compose
即可创建靶场，注意内存资源的分配，以及部分漏洞各个工具的版本问题
![](https://gitee.com/fogpost/photo/raw/master/202411211945375.png)

搭建还是挺简单的