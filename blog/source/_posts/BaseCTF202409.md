---
title: BaseCTF202409
date: 2024-09-14 11:05:39
categories: CTF
tags: reverse
created: 2026-01-18T12:49
updated: 2024-09-14 11:05:39
---
## Reverse
### UPX mini
既然是UPX那必须先DIE查壳  
![](https://gitee.com/fogpost/photo/raw/master/202409141119212.png)  
一看就不对劲，upx最多只见过3.96的，不过这里先用upx自己脱一下可以脱
直接继续查，64位无壳，进入ida
![](https://gitee.com/fogpost/photo/raw/master/202409141122619.png)  
明显的base64直接，解密  
![](https://gitee.com/fogpost/photo/raw/master/202409141123562.png)  
秒解
BaseCTF{Hav3_@_g0od_t1m3!!!}
### ez_xor

简单xor，直接看ida，查位数64位  
![](https://gitee.com/fogpost/photo/raw/master/202409141128380.png)  
看码了解，关键函数keystream和encrpt，输入长度为28，str、v11、v12、v13加起来正好28位,这个题目要注意的就是ida中的c是小端序的会所有的数据都会反转，而且记得使用原数据，不要用转义后的容易出错
![](https://gitee.com/fogpost/photo/raw/master/202409141137462.png)
![](https://gitee.com/fogpost/photo/raw/master/202409141138498.png)  
写pythonexp
```python
#官方wp
def key_stream(key):
    key_box = []
    for i in range(28):
        key_box.append(key[i%3] ^ i)
    return key_box

def decrypt(enc, key):
    flag = ""
    key = key[::-1]
    for i in range(len(enc)):
        flag += chr(enc[i] ^ key[i])
    return flag

enc1 = bytes.fromhex("1D0B2D2625050901")[::-1]
enc2 = bytes.fromhex("673D491E20317A24")[::-1]
enc3 = bytes.fromhex("34056E2E2508504D")[::-1]
enc4 = b"\"@;%"
enc = enc1 + enc2 + enc3 + enc4
print(enc)

key = (7499608).to_bytes(4, 'little')
key_box = key_stream(key)
print(key_box)

flag = decrypt(enc,key_box)
print(flag)
```
### BasePlus
以上来就搞个base64啊，我感觉像，但是没有确定，于是就看不懂函数里面的几个值为什么没有数了，这么奇怪，果然还是没有学过，不过这次好好分析了一番下次应该就可以瞬间秒杀了，看题
![](https://gitee.com/fogpost/photo/raw/master/202409141107908.png)
我们能了解重要函数为Encode，进入
![](https://gitee.com/fogpost/photo/raw/master/202409141108814.png)
了解了这个是base64后我们还要和源代码分析，发现存在不同
![](https://gitee.com/fogpost/photo/raw/master/202409141109133.png)
了解了这中间有个异或的操作，十分简单
```c++
do
{
    *(_BYTE *)(a2 + v8) = v4[v8] ^ 0xE;
    ++v8;
}
while ( v8 != v5 );
```
直接cyberChef换表加异或双重解密完成，
贴个无广告的[cyberchef](https://cyberchef.org/)
![](https://gitee.com/fogpost/photo/raw/master/202409141116043.png)
得到flag
BaseCTF{BA5e_DEcoD1N6_sEcr3t}

### Ezpy
首先就是按照惯例，文件属性查询，直接die，也可以用DEID或者peexam去查。不过die很全面，但是确实很卡
![](https://gitee.com/fogpost/photo/raw/master/202409151024364.png)  
![](https://gitee.com/fogpost/photo/raw/master/202409151027465.png)  
看题目我们就知道是一个这是一个python题目，其实还有一个办法，pythonexe图标大多都是这个，看DIE竟然没有显示是什么软件打包的，那么我们便可以试试pyinstxtractor
![](https://gitee.com/fogpost/photo/raw/master/202409151029748.png)  
这就是解包过程，和使用方法，在这个过程中pyinstxtractor会自动创建一个导出包，我们可以查看，同时我们也可以发现解包软件对python版本的需求，你有想法的可以用[pyenv](https://zhuanlan.zhihu.com/p/36402791)去除掉这个错误，其实我感觉没什么区别，主要在于后面pyc文件中的magic number
进入解包文件夹，会发现资源文件夹和大量的动态链接库，我们只取敌将首级，直接看到一个没有后缀的题目同名软件Ezpy  
![](https://gitee.com/fogpost/photo/raw/master/202409151035853.png)  
这个其实是pyc也就是python的字节码。我们需要的就是这个，python大部分就是利用pyc来进行反编译，我们所知的反编译工具有[pycdc](https://www.52pojie.cn/thread-1854345-1-1.html)(pycdc会有些麻烦，不过感觉强大些，因为是反编译难免会出现错误，而这个的错误出现会更加稀少)和[uncompyle6](https://pypi.com.cn/project/uncompyle6/)这个的安装非常的简单，有python就行(但是只支持3.8及一下的，作者大大不更3.9了)  
好现在我们开始执行一下pycdc(记得改Ezpy后缀名，pycdc就没关系)，就会发现惊喜了，失败了
![](https://gitee.com/fogpost/photo/raw/master/202409151042742.png)
这个就是我说的magicnumber的问题解决办法也非常简单，一般解包后都会自带一个struct文件。用字节查看器打开推荐[010](https://www.52pojie.cn/thread-1863194-1-1.html)，不过大部分都是损坏的我在这贴一个[magicnumber](https://blog.csdn.net/OrientalGlass/article/details/134612786)。
注意大小端序，照着改就行。建议是十六个字节，留空留下栈区  
![](https://gitee.com/fogpost/photo/raw/master/202409151053398.png)  
然后直接反编译(也可以用网络版的)
```py
import Key
import sys

def init_Sbox(seed):
    k_b = (lambda .0 = None: [ ord(seed[i % len(seed)]) for i in .0 ])(range(256))
    s = list(range(256))
    j = 0
    for i in range(256):
        j = (j + s[i] + k_b[i]) % 256
        s[i] = s[j]
        s[j] = s[i]
    return s


def KeyStream(text, Sbox):
    s = Sbox.copy()
    (i, j) = (0, 0)
    k = [
        0] * len(text)
    for r in range(len(text)):
        i = (i + 1) % 256
        j = (j + s[i]) % 256
        s[i] = s[j]
        s[j] = s[i]
        t = (s[i] + s[j]) % 256
        k[r] = s[t] ^ Key.keykey[r % len(Key.keykey)]
    return k


def Encrypt(text, seed):
    Sbox = init_Sbox(seed)
    key = KeyStream(text, Sbox)
    enc = (lambda .0 = None: [ text[i] ^ key[i] for i in .0 ])(range(len(text)))
    return bytes(enc)

enc = b'\xe6\xaeC~F\xf2\xe3\xbb\xac\x9a-\x02U\x85p\xeb\x19\xd1\xe4\xc93sG\xb0\xeb1\xb5\x05\x05\xc3\xd7\x00\x18+D\xbc\x0cO\x9em\xf1\xbd'
flag = input('Please input Your flag:')
flag = (lambda .0: [ ord(i) for i in .0 ])(flag)
flag = Encrypt(flag, Key.key)
if flag != enc:
    print("It's not flag!")
    continue
print('You are right!')
sys.exit(1)
continue
```
就是一个非常简单的rc4
直接给出exp



