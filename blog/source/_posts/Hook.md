---
title: Hook
date: 2024-10-16 10:19:04
categories: 逆向
tags: DLL
created: 2026-01-18T12:49
updated: 2024-10-16 10:19:04
---

# Hook

## 原理

Hook是一种技术，它允许一个程序监视和修改另一个程序的运行。Hook技术通常用于调试、修改程序行为、保护程序等目的。

在Windows操作系统中，Hook技术主要分为以下几种：键盘Hook、鼠标Hook、消息Hook、API Hook等。

## 介绍
SetWindowsHookExA函数是Windows API中用于设置Hook的函数。它可以用于监视和修改其他程序的键盘、鼠标、消息等事件。

SetWindowsHookExA函数的原型如下：
```c
HHOOK SetWindowsHookExA(
  int       idHook,
  HOOKPROC  lpfn,
  HINSTANCE hmod,
  DWORD     dwThreadId
);
```

### 键盘消息钩取练习

