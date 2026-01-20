---
crated: 2026-01-18T12:49
updated: 2026-01-20T15:39
---

WPScan 是一个专门用于扫描 **WordPress 站点** 的安全工具，主要用于发现 **安全漏洞**、**错误配置** 以及 **敏感信息泄露**，适用于 **渗透测试** 和 **站点安全检测**。





### **WPScan 的主要功能**

1. **枚举信息（信息收集）**
    - **WordPress 版本**（检查是否有已知漏洞）
    - **插件** 和 **主题**（检查是否存在已知漏洞）
    - **用户**（可能用于暴力破解）
    - **配置备份文件**（如 `wp-config.php.bak`）
2. **漏洞检测**
    - 通过 **WPScan API** 查询 WordPress、插件、主题的已知漏洞
    - 检测是否存在 **默认凭据**、**弱密码**
    - 检测 **文件泄露**（如 `.bak`、`.sql` 文件）
3. **暴力破解**
    - 使用字典攻击 WordPress 登录（`-passwords <file>`）
    - 适用于管理员账号未启用强密码策略的情况
4. **安全配置检测**
    - 检查是否存在 `xmlrpc.php`（可能导致 DDoS）
    - 检测 `wp-config.php` 是否可访问
    - 检查目录列表是否被禁用

### **WPScan 的常见用法**

🔹 **扫描 WordPress 站点基本信息**

```shell
bash
复制编辑
wpscan --url http://example.com
```

🔹 **枚举 WordPress 用户**

```shell
bash
复制编辑
wpscan --url http://example.com --enumerate u
```

🔹 **枚举插件**

```shell
bash
复制编辑
wpscan --url http://example.com --enumerate p
```

🔹 **使用 API Token 获取漏洞详情**

```shell
bash
复制编辑
wpscan --url http://example.com --api-token YOUR_API_TOKEN
```

🔹 **暴力破解 WordPress 用户密码**

```shell
bash
复制编辑
wpscan --url http://example.com --passwords passwords.txt
```
