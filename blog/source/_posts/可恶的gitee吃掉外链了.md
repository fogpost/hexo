---
title: 可恶的gitee吃掉外链了
date: 2024-09-12 22:26:07
categories: 教程
tags: blog
created: 2026-01-18T12:49
updated: 2024-09-12 22:26:07
---
### 开始
这是这个博客最开始的故事，我想要用gitee做一个图床，当时我怎么也没想到gitee居然拒绝掉外链的请求了，就像这样
![](https://gitee.com/fogpost/photo/raw/master/202409122231370.png)  
但是反复尝试我们发现了一下返回值
### 防盗链
要实现防盗链，就需要知道图片的请求是从哪里发出的。可以实现这一功能的有请求头中的origin和referer。origin只有在XHR请求中才会带上，所以图片资源只能借助referer

通过判断请求的referer，如果请求来源不是本站就返回302

#### 一个完整的流程：
- 首先请求正常的图片，但是没有返回200，而是302重定向，其中响应头中的location就是要重定向去向的地址
- 接着浏览器会自动请求这个location，并用这个返回结果代替第一次请求的返回内容
![](https://gitee.com/fogpost/photo/raw/master/202409122241207.png)
#### 如何破解防盗链
想让gitee不知道我在盗用，就不能让他发现请求的来源是第三方，只要把referer藏起来就好

![](https://gitee.com/fogpost/photo/raw/master/202409122236635.png)  
但是我们可以骗过gitee，用butterfly和yilia的主题可以上网搜搜都有讲，fluid这类的不同，但是我们这里要讲下进阶的代码注入
![](https://gitee.com/fogpost/photo/raw/master/202409122233566.png)
按上面这个我们就可以写出header头前的代码来注入，骗过gitee使图片显现
下面是我的代码
```js
hexo.extend.injector.register('head_begin', '<meta name="referrer" content="no-referrer" />', 'post');
```
注解：
<meta name="referrer" content="no-referrer" /> 指定了 "no-referrer" 的内容，意味着浏览器在发送请求时不会包含任何引用来源信息。换句话说，当用户从当前网页跳转到其他页面时，新页面接收到的请求中将不包含这个跳转前的页面地址

[参考文章](https://blog.csdn.net/weixin_52479803/article/details/131774501)