---
title: tea.dm
categories: 逆向
date: 2024-09-10 18:33:20
tags: reverse
created: 2026-01-18T12:49
updated: 2024-09-10 18:33:20
---
# tea
终于自己做出一道tea了乐
看原题
![](http://gitee.com/fogpost/photo/raw/master/202409122053979.png) 
&emsp;典型的tea直接套模板，但是有问题，就是py中不会限定为32位所以最后的答案会超级大，我们就要去进行一个&ffffffff的操作使数值正确  
&emsp;然后就是关于题目中的小问题，首先就是delta，标准的tea是0x9E3779B9，但是在ida中总是会出现变成-0x61c88647的问题需要注意，然后就是最后的v5怎么求,就是一个偏移相加，在exp中有了
### exp 
```python
def decrypt(v0, v1):
    delta = 0x9E3779B9
    v3 = delta * 32
    for _ in range(32):
        v1 = (v1 - ((v0 + v3) ^ (16 * v0 + 1634038898) ^ ((v0 >> 5) + 1634038904))) & 0xFFFFFFFF
        v0 = (v0 - ((v1 + v3) ^ (16 * v1 + 1702060386) ^ ((v1 >> 5) + 1870148662))) & 0xFFFFFFFF
        v3 = (v3 - delta) & 0xFFFFFFFF
    return v0, v1
#已知的加密结果
v4 = 676078132
v5 = 957400408
#解密
v10, v11 = decrypt(v4, v5)
print(f"Decrypted v10: {hex(v10)}, v11: {hex(v11)}")
i=0x49BD
j=0x8e00
print(hex(i)+" "+hex(j)+" "+hex(i|(j<<16)))
#moectf{836153a5-8e00-49bd-9c42-caf30620caaf}
```
