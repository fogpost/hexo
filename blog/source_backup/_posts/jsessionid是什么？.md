---
title: jsessionid是什么？
date: 2024-09-16 10:32:22
categories: 网络
tags: web
crated: 2026-01-20T15:50
updated: 2026-01-20T15:39
---
之前不是写了一个爬数据的脚本么，今天发现一个问题，就是jsessonid在刷新之后变了，所以我现在想要找到一个不会变的方法，不过这个修改和学习时间应该会变得比较久，感觉挺高阶的

看了一些文章将的都是tomcat的的例子，先讲讲什么是session，浏览器第一次访问服务器会生成一个session保存相关信息，会有一个sessionid来对应这个session，__那么我们就想可不可以利用这个id直接去查session的值__  

tomcat的StandardManager类将session存储在内存中也可以持久化到文件中，sessionid是一个指代session在服务器端位置的值，存储在客户端的cookie上，不会将session保存在本地,session也只能通过invalidate或超时来销毁

>那么Session在何时创建呢？当然还是在服务器端程序运行的过程中创建的，不同语言实现的应用程序有不同创建Session的方法，而在Java中是通过调用HttpServletRequest的getSession方法（使用true作为参数）创建的。在创建了Session的同时，服务器会为该Session生成唯一的Session id，而这个Session id在随后的请求中会被用来重新获得已经创建的Session；在Session被创建之后，就可以调用Session相关的方法往Session中增加内容了，而这些内容只会保存在服务器中，发到客户端的只有Session id；当客户端再次发送请求的时候，会将这个Session id带上，服务器接受到请求之后就会依据Session id找到相应的Session，从而再次使用之。

创建：sessionid第一次产生是在直到某server端程序调用 HttpServletRequest.getSession(true)这样的语句时才被创建。

删除：超时；程序调用HttpSession.invalidate()；程序关闭；

session存放在哪里：服务器端的内存中。不过session可以通过特殊的方式做持久化管理（memcache，redis）。

session的id是从哪里来的，sessionID是如何使用的：当客户端第一次请求session对象时候，服务器会为客户端创建一个session，并将通过特殊算法算出一个session的ID，用来标识该session对象

session会因为浏览器的关闭而删除吗？
不会，session只会通过上面提到的方式去关闭。

下面是tomcat中session的创建：
>ManagerBase是所有session管理工具类的基类，它是一个抽象类，所有具体实现session管理功能的类都要继承这个类，该类有一个受保护的方法，该方法就是创建sessionId值的方法：
（ tomcat的session的id值生成的机制是一个随机数加时间加上jvm的id值，jvm的id值会根据服务器的硬件信息计算得来，因此不同jvm的id值都是唯一的），
StandardManager类是tomcat容器里默认的session管理实现类，
它会将session的信息存储到web容器所在服务器的内存里。
PersistentManagerBase也是继承ManagerBase类，它是所有持久化存储session信息的基类，PersistentManager继承了PersistentManagerBase，但是这个类只是多了一个静态变量和一个getName方法，目前看来意义不大， 对于持久化存储session，tomcat还提供了StoreBase的抽象类，它是所有持久化存储session的基类，另外tomcat还给出了文件存储FileStore和数据存储JDBCStore两个实现。

所以会出现以下三种情况：

>1、server没有关闭，并在session对象销毁时间内，当客户端再次来请求serve端的servlet或jsp时，将会把将第一次请求该serve时生成的sessionid带到请求头上向server端发送，server端收到sessionid后根据此sessionid会去搜索server对应的session对象并直接返回这个session对象，此时不会重新创建session对象。  
2、当server关闭（之前产生的session对象也就消亡了），或者session对象过了销毁时间，浏览器窗口没有关闭，并在本窗口继续请求server端的servlet或者jsp时，此时同样会将sessionid 发送到 服务端，server拿着id去找对应的session对象；但是此时session对象已经不存在了。所以会重新生成一个session和对应的sessionid ，将这个新的id以响应报文的形式发到浏览器的内核中，重新更新cookie。  
3、当server没有关闭，并且session对象在其销毁时间内，当请求一个jsp页面返回客户端后，关闭此浏览器窗口，此时其内存中的sessionid也就随之销毁。在重新去请求server端的servlet或者jsp时，会重新生成一个sessionid给客户端浏览器，并且存在浏览器内存中。

我们使用的其实就是将已经存放的cookie来重放获取对应的数据，不过在刷新过后应该会调用HttpSession.invalidate()，并在下次请求时创建一个新的session来进行访问，所以要是想改的的话要么就是对应的服务器端有session持续化保存机制，不然我每隔两天就要手动更新session难受哦，/(ㄒoㄒ)/~~

__cookie的保存方式有两种：__  
如果没有设置cookie的失效时间，这个cookie就存在与浏览器进程；

设置了cookie的失效时间，那么这个cookie就存在于硬盘。
```java
//Cookie的一些基本设置
        Cookie cookie = new Cookie("Admin-Token", token);

        Cookie[] cookie2 = request.getCookies();
        //request.getContextPath()   mdrwebrest
        cookie.setPath("/");        //设置cookies有效路径
        //设置cookie有效时间  正数：存到硬盘，负数存到浏览器，0立刻销毁
        cookie.setMaxAge();      
        cookie.setDomain(loginToMDRConfig.getIP()); //跨域
        response.addCookie(cookie);
```
下面是实现机制图
![](https://gitee.com/fogpost/photo/raw/master/202409161116311.png)
文章给出的获取sessionid方法是
```java
HttpSession session=request.getSession(); //获取session
String sessionid=session.getId();  //获取sessionid
Cookie cookie=new Cookie("JSESSIONID",sessionid); //手动设置一个硬盘存储COOKIE，这个cooike时存在硬盘的，不是存在浏览器线程的
cookie.setMaxAge(30*60);
response.addCookie(cookie); //将COOKIE设置到响应上
```
其实我们可以假借服务器自己的手，通过burp抓包来实现获取对应的sessionid，进一步获取对应报文(这不就是我之前干过的么，现在学了一遍原理，👿我了)




[jsessionid](https://www.cnblogs.com/Timeouting-Study/p/16082575.html)
