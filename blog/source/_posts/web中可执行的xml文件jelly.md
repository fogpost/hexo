---
title: web中可执行的xml文件jelly
date: 2024-12-11 14:03:29
category: 网络
tags: web
updated: 2024-12-11T14:03:29+08:00
---
# 简介
好久没有写东西了，最近的ctf中有遇到一个jelly的题目，记录一下，题目是国成杯的web题，题目描述如下：

## Jelly简介
[Jelly的官方介绍](https://commons.apache.org/proper/commons-jelly/)

Jelly是Java Server Pages XML的简称，它是一种基于XML的脚本语言，用于在Java EE应用程序中生成动态内容。Jelly是一种基于XML的脚本语言，它允许开发人员使用XML标记来编写Java代码，从而实现动态内容的生成。

Jelly脚本通常包含在JSP文件中，通过在JSP文件中使用特殊的XML标记来执行Java代码。这些标记被称为Jelly标签，它们可以用于执行Java代码、访问Java对象、处理请求和响应等操作。

## 如何实现并工作的
```xml
<document time="${now}">
  Welcome ${user.name} to Jelly!
</document>
```

原本有的脚本
```java
public class MyTask {

    // 'doIt' method that does some function/task...
    public void run() throws SomeException {
        // do something...
    }

    // Properties, can be any type
    public void setX(int x) {
        this.x = x;
    }
    public void setY(String y) {
        this.y = y;
    }
}
```
调用脚本的jelly文件
```xml
<j:jelly xmlns:j="jelly:core" xmlns:define="jelly:define" xmlns:my="myTagLib">

  <define:taglib uri="myTagLib">
    <define:jellybean name="foo" className="MyTask"/>
  </define:taglib>

  Now lets use the new tag
  
  <my:foo x="2" y="cheese"/>

</j:jelly>
```

## 继承功能
jelly继承了JSTL，Ant，XML和Web_Service等，可以执行很多功能