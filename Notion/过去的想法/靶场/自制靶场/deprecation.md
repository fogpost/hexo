## 信息收集
![image.png](https://gitee.com/fogpost/photo/raw/master/202603021106830.png)
利用nmap进行网段信息分析，发现对应的80http端口和22ssh端口，
![image.png|474](https://gitee.com/fogpost/photo/raw/master/202603021105276.png)
页面结构没有明显的漏洞服务件
![image.png](https://gitee.com/fogpost/photo/raw/master/202603021115327.png)
打开页面后仅发现登录模块，发现存在次数限制和session控制，查看源码

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>Neon Abyss • Login</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="style.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
</head>
<body>
<div class="container">
    <div class="card">
        <h1>Neon Abyss</h1>    
        <form method="post">//在此处发现CSRF漏洞可能
            <input type="hidden" name="action" value="login">
            <div class="input-group">
                <input type="text" name="username" placeholder="用户名" required autocomplete="off">//无语句转义，发现可能存在sql注入
                <i class="fas fa-user-astronaut"></i>
            </div>
            <div class="input-group">
                <input type="password" name="password" placeholder="密码" required>
                <i class="fas fa-key"></i>
            </div>
            <button type="submit">登录</button>
        </form>
    </div>
</body>
</html>
```
代码缺少安全措施，无直接漏洞
## 漏洞获取
在登录页面尝试sql注入和暴力破解发现admin和test为主账户之一
![image.png](https://gitee.com/fogpost/photo/raw/master/202603021120372.png)
在尝试过修改参数值后
- `'` 无注入
- sqlmap无效
- action无效
- 有登录锁定
- 使用 empty()
- 单入口 `/`
- PHPSESSID 存在
- 标题 deprecation
- 结合标题认为是某种废弃的php特性
