---
title: web反序列化
date: 2024-09-27 08:00:57
categories: 网络
tags: php
updated: 2024-09-27T08:00:57+08:00
---
本人在学习php反序列化时，深感无力，发现并不能将发序列化作为一个小点，要从php底层开始理解

先了解一下php的魔术方法
>__construct()	类的构造函数，在类实例化对象时自动调用构造函数  
__destruct()	类的析构函数，在对象销毁之前自动调用析构函数  
__sleep()	在对象被序列化（使用 serialize() 函数）之前自动调用，可以在此方法中指定需要被序列化的属性，返回一个包含对象中所有应被序列化的变量名称的数组  
__wakeup()	在对象被反序列化（使用 unserialize() 函数）之前自动调用，可以在此方法中重新初始化对象状态。  
__set($property, $value)	当给一个对象的不存在或不可访问(private修饰)的属性赋值时自动调用，传递属性名和属性值作为参数。  
__get($property)	当访问一个对象的不存在或不可访问的属性时自动调用，传递属性名作为参数。  
__isset($property)	当对一个对象的不存在或不可访问的属性使用 isset() 或 empty() 函数时自动调用，传递属性名作为参数。  
__unset($property)	当对一个对象的不存在或不可访问的属性使用 unset() 函数时自动调用，传递属性名作为参数。  
__call($method, $arguments)	调用不存在或不可见的成员方法时，PHP会先调用__call()方法来存储方法名及其参数  
__callStatic($method, $arguments)	当调用一个静态方法中不存在的方法时自动调用，传递方法名和参数数组作为参数。  
__toString()	当使用echo或print输出对象将对象转化为字符串形式时，会调用__toString()方法  
__invoke()	当将一个对象作为函数进行调用时自动调用。  
__clone()	当使用 clone 关键字复制一个对象时自动调用。  
__set_state($array)	在使用 var_export() 导出类时自动调用，用于返回一个包含类的静态成员的数组。  
__debugInfo()	在使用 var_dump() 打印对象时自动调用，用于自定义对象的调试信息。

1.__construct
构造函数 __construct在实例化对象时便会自动执行该方法  
```php
<?php
class User {
    public $username;
    public function __construct($username) {
        $this->username = $username;
        echo "触发了构造函数1次" ;
    }
}
$test = new User("benben");    //实例化对象时触发构造函数__construct()
$ser = serialize($test);       //在序列化和反序列化过程中不会触发构造函数
unserialize($ser);
?>
``` 
2.__destruct()
析构函数__destruct,在对象被销毁时自动执行该方法
```php
<?php
class User {
    public function __destruct()
    {
        echo "触发了析构函数1次";
    }
}
$test = new User("benben");  //实例化对象结束后，代码运行完会销毁，触发析构函数_destruct()
$ser = serialize($test);     //在序列化过程中不会触发
unserialize($ser);           //在反序列化过程中会触发，反序列化得到的是对象，用完后会销毁，触发析构函数_destruct()
?>
```
>以上代码总共触发两次析构函数，第一次为实例化对象后，代码运行完会，对象会被销毁，触发析构函数_destruct()；第二次在反序列化过程中会触发，反序列化得到的是对象，用完后会销毁，触发析构函数_destruct()

3.__sleep()

>在进行序列化时，serialize()函数会检查类中是否存在一个魔术方法__sleep()。如果存在，该方法会先被调用，可以在此方法中指定需要被序列化的属性，返回一个包含对象中所有应被序列化的变量名称的数组。然后才执行序列化操作。  
此功能可以用于清理对象，并返回一个包含对象中所有应被序列化的变量名称的数组。如果该方法未返回任何内容，则 NULL 被序列化，并产生一个 E_NOTICE级别的错误。
```php
<?php
class User {
    const SITE = 'uusama';
    public $username;
    public $nickname;
    private $password;
    public function __construct($username, $nickname, $password) {
        $this->username = $username;
        $this->nickname = $nickname;
        $this->password = $password;
    }
    public function __sleep() {
        return array('username', 'nickname');      //sleep执行返回需要序列化的属性名，过滤掉password变量
    }
}
$user = new User('a', 'b', 'c');
echo serialize($user);      //serialize()只序列化sleep返回的变量，序列化之后的字符串：O:4:"User":2:{s:8:"username";s:1:"a";s:8:"nickname";s:1:"b";}
//
?>
```
4.__wakeup()

>在进行反序列化时，unserialize()会检查是否存在一个魔术方法__wakeup()，如果存在，则会先调用__wakeup方法，做一些初始化工作。  
使用__wakeup方法的原因是为了重建在序列化中可能丢失的数据库连接，或者执行其它初始化操作。
```php
<?php
class User {
    const SITE = 'uusama';
    public $username;
    public $nickname;
    private $password;
    private $order;
    public function __wakeup() {
        $this->password = $this->username;       //反序列化之前触发_wakeup(),给password赋值
    }
}
$user_ser = 'O:4:"User":2:{s:8:"username";s:1:"a";s:8:"nickname";s:1:"b";}';    // 字符串中并没有password
var_dump(unserialize($user_ser));   // object(User)#1 (4) { ["username"]=> string(1) "a" ["nickname"]=> string(1) "b" ["password":"User":private]=> string(1) "a" ["order":"User":private]=> NULL } 
?>
```
>__wakeup()在反序列化unserialize()之前被调用  
__destruct()在反序列化unserialize()之后被调用

5.__toString()
>当使用echo或print输出对象将对象转化为字符串形式，或者将一个“对象”与“字符串”进行拼接时，会调用__toString()方法
```php
<?php
class User {
    var $benben = "this is test!!";
    public function __toString()
    {
        return '格式不对，输出不了!';
    }
}
$test = new User() ;     // 把类User实体化并赋值给$test，此时$test是个对象
print_r($test);          // 打印输出对象可以使用print_r或者var_dump，该对象输出后为：User Object(    [benben] => this is test!!)
echo $test;              // 如果使用echo或者print只能调用字符串的方式去调用对象，即把对象当成字符串使用，此时自动触发toString()
?>
```
6.__invoke()  
当将一个对象作为函数进行调用时会触发__invoke()函数
```php
<?php
class User {
    var $benben = "this is test!!";
         public function __invoke()
         {
             echo  '它不是个函数!';
          }
}
$test = new User() ;     //把类User实例化为对象并赋值给$test
echo $test ->benben;     //正常输出对象里的值benben
$test();                 //加()是把test当成函数test()来调用，此时触发_invoke()
?>
```
7.__call()  
当调用不存在或不可见的成员方法时，PHP会先调用__call()方法来存储方法名及其参数
```php
<?php
class User {
    public function __call($arg1,$arg2)
    {
        echo "$arg1,$arg2[0]";
    }
}
$test = new User() ;
$test -> callxxx('a','b','c'); //调用的方法callxxx()不存在,触发魔术方法call(),传参(callxxx,a);$arg1:调用的不存在的方法的名称;$arg2:调用的不存在的方法的参数；
?>
```
>__call(string $function_name, array $arguments)该方法有两个参数，第一个参数 $function_name 会自动接收不存在的方法名，第二个 $arguments 则以数组的方式接收不存在方法的多个参数

8.__callStatic()  
当调用不存在或不可见的静态方法时，会自动调用__callStatic()方法，传递方法名和参数数组作为参数
```php
<?php
class User {
    public static function __callStatic($arg1,$arg2)
    {
        echo "$arg1,$arg2[0]";
    }
}
$test = new User() ;
$test::callxxx('a');        //静态调用使用"::"，静态调用方法callxxx()，由于其不存在，所以触发__callStatic，传参(callxxx,a)，输出：callxxx,a
?>
```
9.__set()  
__set($name, $value)函数，给一个对象的不存在或不可访问(private修饰)的属性赋值时，PHP就会执行__set()方法。__set()方法包含两个参数，$name表示变量名称，$value表示变量值，两个参数不可省略。
```php
<?php
class User {
    public $var1;
    public function __set($arg1 ,$arg2)
    {
        echo  $arg1.','.$arg2;
    }
}
$test = new User() ;
$test->var2=1;        //给不存在的成员属性var2赋值为1，自动触发__set()方法；如果有__get(),先调用__get(),再调用__set()，输出：var2,1
?>
```
10.__get()  
__get($name)函数，当程序访问一个未定义或不可见的成员变量时，PHP就会执行 __get()方法来读取变量值。__get()方法有一个参数，表示要调用的变量名
```php
<?php
class User {
    public $var1;
    public function __get($arg1)
    {
        echo  $arg1;
    }
}
$test = new User() ;
$test ->var2;         //调用的成员属性var2不存在，触发__get(),把不存在的属性的名称var2赋值给$arg1，输出：var2
?>
```
11.__isset()
当对一个对象的不存在或不可访问的属性使用 isset() 或 empty() 函数时自动调用，传递属性名作为参数。__isset()方法有一个参数，表示要调用的变量名
```php
<?php
    class User {
        private $var;
        public function __isset($arg1)
        {
            echo  $arg1;
        }
    }
$test = new User() ;
isset($test->var);       // 调用的成员属性var不可访问，并对其使用isset()函数或empty()函数，触发__isset()，输出：var
?>
```
12.__unset()
当对一个对象的不存在或不可访问的属性使用 unset() 函数时自动调用，传递属性名作为参数。__unset()方法有一个参数，表示要调用的变量名
```php
<?php
    class User {
        private $var;
        public function __unset($arg1 )
        {
            echo  $arg1;
        }
    }
$test = new User() ;
unset($test->var);        // 调用的成员属性var不可访问，并对其使用unset()函数，触发__unset()，输出：var
?>
```
.13 __clone()
当对象被复制执行
```php
<?php
    class User {
        private $var;
        public function __clone( )
        {
            echo  "__clone test";
        }
    }
$test = new User() ;
$newclass = clone($test)        // __clone test
?>
```