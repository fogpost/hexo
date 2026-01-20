---
title: pip下载
date: 2024-11-07 20:34:56
categrories: python
tags: tool
updated: 2024-11-07 20:34:56
---
# pip下载

## 下载

```shell
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple <package>
```

## 下载指定版本

```shell
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple <package>==<version>
```

## 永久配置国内镜像源
```shell
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

## 配置多个镜像源
```shell
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
extra-index-url = https://pypi.douban.com/simple
extra-index-url = https://mirrors.aliyun.com/pypi/simple/
```