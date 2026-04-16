- 反射型
- 存储型（危害最大）
- DOM型

- 本质：前端未过滤用户输入
- 利用：窃取cookie / 劫持会话

```js
<script>alert(document.cookie)</script>
```

- 输出编码
- CSP策略
- HttpOnly