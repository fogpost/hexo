综述：反序列化漏洞是指程序在反序列化用户可控数据时，没有对对象进行安全校验，从而导致攻击者构造恶意对象触发魔术方法执行危险操作。在 PHP 中常见利用 `__destruct`、`__wakeup` 等魔术方法，通过 POP 链实现代码执行。防御方法是避免反序列化不可信数据，使用 JSON 替代，并对可反序列化类进行白名单限制。
## 序列化：
把对象转换成字符串或字节流。

```Python
import pickle  
pickle.dumps(obj)
```

```PHP
serialize($obj);
```

```Java
ObjectOutputStream
```

## 什么是反序列化
把字符串恢复成对象。
```python
pickle.loads(data)
```

```php
unserialize($data)
```

## 反序列化漏洞原理
如果程序：
反序列化用户可控数据
攻击者就可以构造恶意对象。
例如：
cookie、session、POST数据

## PHP 反序列化漏洞
```php
class Test{
    public $cmd;
    function __destruct(){
        system($this->cmd);
    }
}
```

pyload:O:4:"Test":1:{s:3:"cmd";s:2:"id";
unserialize:system("id")

## 魔术方法触发
### PHP 反序列化利用依赖 **魔术方法**：
>__wakeup()
__destruct()
__toString()
__call()

## POP链
Property Oriented Programming 利用多个类组合成利用链。
## java反序列化
函数：readObject()
攻击工具：ysoserial
经典漏洞：CommonsCollections
攻击 payload：Runtime.exec()
## Python 反序列化
pickle、yaml
```python
pickle.loads(data)
```

## 反序列化漏洞防御
1. 不要反序列化不可信数据
2. 使用安全格式
使用：JSON
不用：pickle、PHP serialize、Java ObjectInputStream
3. 白名单类：ObjectInputFilter
4. 禁止危险函数：disable_functions
