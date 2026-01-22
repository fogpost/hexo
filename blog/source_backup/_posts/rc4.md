---
title: rc4
date: 2024-10-28 21:13:17
categories: 逆向算法
tags: reverse
updated: 2024-10-28 21:13:17
---
# RC4
写题过程中会出现像rc4这种简单的对称加密算法，在此留下对应的解密脚本
由于初始化的s盒和产生的密钥流是由固定的密钥确定，并且加密的本质是异或所以为对称的
rc4加密主要分为三个部分
- 初始化s盒
- 生成密钥流
- 加密

```python
def KSA(key):
    key_length = len(key)

    # 初始化S盒
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % key_length]) % 256
        S[i], S[j] = S[j], S[i]

    return S

def PRGA(S):
    i = 0
    j = 0
    while True:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        yield K

def RC4(key, data):
    S = KSA(key)
    keystream = PRGA(S)
    res = []
    for c in data:
        res.append(c ^ next(keystream))
    return bytes(res)
```