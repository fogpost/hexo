---
title: ctf_vm虚拟机
date: 2024-11-02 09:56:22
cat额gories: CTF
tags: ctf
created: 2026-01-18T12:49
updated: 2024-11-02 09:56:22
---

# ctf_vm虚拟机
最近打些大比赛果然都有这个虚拟机，但是本人学的不够精细，这次强网杯又有了，借此机会来开个新篇章让自己的技术和见识都涨涨

## [HGAME 2023 week4]vm
先借助去年的HGAME来了解一下，这个题非常好，因为已经有了较多的wp可以借助前人的智慧来分析分析，虚拟机题简单来讲就是利用伪代码，在程序中重新实现了一个虚拟机，其实就是把几个重要的汇编代码隐藏起来了而已，我们就要去分析在哪发生了什么。
- 查壳
可以看出这个是c++编写的64位EXE程序，没有壳
![](https://gitee.com/fogpost/photo/raw/master/202411021001405.png)
- IDA分析
可见这个直接就是一个简单的判断我们直达vm虚拟机内部
![](https://gitee.com/fogpost/photo/raw/master/202411021004776.png)
这代表这这个命令函数的最大值是255(0xff)
![](https://gitee.com/fogpost/photo/raw/master/202411021005546.png)  
进入虚拟机主要函数，逐步分析每个分支分别代表什么
![](https://gitee.com/fogpost/photo/raw/master/202411021021368.png)  
我们来看看每个函数的内部来了解发生了什么
1. mov
![](https://gitee.com/fogpost/photo/raw/master/202411021023687.png)
2. push&pop
这两个同理
![](https://gitee.com/fogpost/photo/raw/master/202411021026035.png)
![](https://gitee.com/fogpost/photo/raw/master/202411021027121.png)
3. mul数据计算单元
感觉和我们之前学的数电计算单元一样，单独分出了一个模块来运算操作，分别是【+、-、*、^、<<、>>、0】
![](https://gitee.com/fogpost/photo/raw/master/202411021031712.png)
4. cmp比较单元  
直接看就看出来了，从cmp也是相同为0不同为1
![](https://gitee.com/fogpost/photo/raw/master/202411021033928.png)
5. jmp跳转单元  
![](https://gitee.com/fogpost/photo/raw/master/202411021034959.png)
6. je和jne
相同跳转和不相同跳转
![](https://gitee.com/fogpost/photo/raw/master/202411021037299.png)
![](https://gitee.com/fogpost/photo/raw/master/202411021037492.png)

至此已分析完毕,很简单对不对，汇编语句总共就那么多条，常用且能用的就更少了我们只要仔细分析就行
- exp
直接抄的，这个其实涉及一些idc脚本的编写，之后我也会出一篇博客来讲，怎么利用idc脚本去进行SMC的解密以及花指令的去除
```python
opcode = [0x00, 0x03, 0x02, 0x00, 0x03, 0x00, 0x02, 0x03,0x00, 0x00,0x00, 0x00, 0x00, 0x02, 0x01, 0x00, 0x00, 0x03, 0x02, 0x32,0x03, 0x00, 0x02, 0x03, 0x00, 0x00, 0x00, 0x00, 0x03, 0x00,0x01, 0x00, 0x00, 0x03, 0x02, 0x64, 0x03, 0x00, 0x02, 0x03,0x00, 0x00, 0x00, 0x00, 0x03, 0x03, 0x01, 0x00, 0x00, 0x03,0x00, 0x08, 0x00, 0x02, 0x02, 0x01, 0x03, 0x04, 0x01, 0x00,0x03, 0x05, 0x02, 0x00, 0x03, 0x00, 0x01, 0x02, 0x00, 0x02,0x00, 0x01, 0x01, 0x00, 0x00, 0x03, 0x00, 0x01, 0x03, 0x00,0x03, 0x00, 0x00, 0x02, 0x00, 0x03, 0x00, 0x03, 0x01, 0x28,0x04, 0x06, 0x5F, 0x05, 0x00, 0x00, 0x03, 0x03, 0x00, 0x02,0x01, 0x00, 0x03, 0x02, 0x96, 0x03, 0x00, 0x02, 0x03, 0x00,0x00, 0x00, 0x00, 0x04, 0x07, 0x88, 0x00, 0x03, 0x00, 0x01,0x03, 0x00, 0x03, 0x00, 0x00, 0x02, 0x00, 0x03, 0x00, 0x03,0x01, 0x28, 0x04, 0x07, 0x63, 0xFF, 0xFF]
input1 = []
i = 0
while opcode[i] != 0xFF:
    match opcode[i]:
        case 0x00:
            print(f'{i}', end=' ')
            o = i + 1
            if opcode[o]:
                match opcode[o]:
                    case 0x01:
                        print("mov input[reg[2]], reg[0]")
                    case 0x02:
                        print("mov reg[%d], reg[%d]" % (opcode[i+2],opcode[i+3]))
                    case 0x03:
                        print("mov reg[%d], %d" % (opcode[i+2], opcode[i+3]))
            else:
                print("mov reg[0], input[reg[2]]")
            i += 4
        case 0x01:
            print(f'{i}', end=' ')
            o = i + 1
            if opcode[o]:
                match opcode[o]:
                    case 0x01:
                        print("push reg[0]")
                    case 0x02:
                        print("push reg[2]")
                    case 0x03:
                        print("push reg[3]")
            else:
                print("push reg[0]")
            i += 2
        case 0x02:
            print(f'{i}', end=' ')
            o = i + 1
            if opcode[o]:
                match opcode[o]:
                    case 0x01:
                        print("pop reg[1]")
                    case 0x02:
                        print("pop reg[2]")
                    case 0x03:
                        print("pop reg[3]")
            else:
                print("pop reg[0]")
            i += 2
        case 0x03:
            print(f'{i}', end=' ')
            o = i + 1
            match opcode[o]:
                case 0:
                    print("add reg[%d],reg[%d]" % (opcode[i + 2], opcode[i + 3]))
                case 1:
                    print("sup reg[%d],reg[%d]" % (opcode[i + 2], opcode[i + 3]))
                case 2:
                    print("mul reg[%d],reg[%d]" % (opcode[i + 2], opcode[i + 3]))
                case 3:
                    print("xor reg[%d],reg[%d]" % (opcode[i + 2], opcode[i + 3]))
                case 4:
                    print("shl reg[%d],reg[%d]" % (opcode[i + 2], opcode[i + 3]))
                case 5:
                    print("shr reg[%d],reg[%d]" % (opcode[i + 2], opcode[i + 3]))
            i += 4
        case 0x04:
            print(f'{i} cmp reg[0], reg[1]')
            i += 1
        case 0x05:
            print(f'{i} jmp %d ' % (opcode[i+1]))
            i += 2
        case 0x06:
            print(f'{i} je %d ' % (opcode[i+1]))
            i += 2
        case 0x07:
            print(f'{i} jne %d ' % (opcode[i+1]))
            i += 2
```
- 输出和分析  
0 mov reg[2], 0  
4 add reg[2],reg[3]  
8 mov reg[0], input[reg[2]]  
12 mov reg[1], reg[0]   
//前四局  用于数据的初始化 
16 mov reg[2], 50  
20 add reg[2],reg[3]  
24 mov reg[0], input[reg[2]]  
28 add reg[1],reg[0]    
//以50为分界线，将新的数据与原来的reg[1]相加相当于数组之间全部加一遍
32 mov reg[2], 100  
36 add reg[2],reg[3]  
40 mov reg[0], input[reg[2]]  
44 xor reg[1],reg[0]  
//以100为分界线，将新的数据与原来的reg[1]进行异或
48 mov reg[0], 8  
52 mov reg[2], reg[1]  
56 shl reg[1],reg[0]  
60 shr reg[2],reg[0]  
64 add reg[1],reg[2]  
68 mov reg[0], reg[1]  
72 push reg[0]  
//这一步是将reg[0]置为8，然后进行左移右移操作，最后将结果加到reg[1]上，并将结果压入栈中
74 mov reg[0], 1  
78 add reg[3],reg[0]  
82 mov reg[0], reg[3]  
86 mov reg[1], 40  
90 cmp reg[0], reg[1]  
91 je 95  
93 jmp 0 
95 mov reg[3], 0  
//这个代表的是将上面的过程重复40次
99 pop reg[1]  
101 mov reg[2], 150  
105 add reg[2],reg[3]  
109 mov reg[0], input[reg[2]]  
113 cmp reg[0], reg[1]  
114 jne 136  
//这个是将栈中的数据与150号位置的数据进行比较，如果相同则跳转到136，否则跳转到0
116 mov reg[0], 1  
120 add reg[3],reg[0]  
124 mov reg[0], reg[3]  
128 mov reg[1], 40  
132 cmp reg[0], reg[1]  
133 jne 99  
//循环四十次回到99，好像是干扰项

函数就是这个
```python
    flag = []  
    a1 = []  
    a2 = []  
    a3 = []  
    k = a1 + flag  
    k2 = a2 ^ k  
    a3 = k2 << 8 + k2 >> 8
    #nixiang
    for i in range(40):
        k2=((a3[i])>>8)&0xff+((a3[i])<<8)&0xff
        k=k2^a2
        flag=k-a1
```
```py
a1 = [155, 168, 2, 188, 172, 156, 206, 250, 2, 185, 255, 58, 116, 72, 25, 105, 232, 3, 203, 201,
      255, 252, 128, 214, 141, 215, 114, 0, 167, 29, 61, 153, 136, 153, 191, 232, 150, 46, 93, 87]
a2 = [201, 169, 189, 139, 23, 194, 110, 248, 245, 110, 99, 99, 213, 70, 93, 22, 152, 56, 48, 115, 56,
      193, 94, 237, 176, 41, 90, 24, 64, 167, 253, 10, 30, 120, 139, 98, 219, 15, 143, 156]
a3 = [18432, 61696, 16384, 8448, 13569, 25600, 30721, 63744, 6145, 20992, 9472, 23809, 18176, 64768, 26881, 23552,
      44801, 45568, 60417,
      20993, 20225, 6657, 20480, 34049, 52480, 8960, 63488, 3072, 52992, 15617, 17665, 33280, 53761, 10497, 54529, 1537,
      41473, 56832, 42497, 51713]
a4 = a3[::-1]
# a4 = [51713, 42497, 56832, 41473, 1537, 54529, 10497, 53761, 33280, 17665, 15617, 52992, 3072, 63488, 8960, 52480, 34049, 20480, 6657, 20225, 20993, 60417, 45568, 44801, 23552, 26881, 64768, 18176, 23809, 9472, 20992, 6145, 63744, 30721, 25600, 13569, 8448, 16384, 61696, 18432]
flag = [0] * 40
for i in range(40):
    flag[i] = ((a4[i] >> 8) & 0xff + (a4[i] << 8))
    flag[i] ^= a2[i]
    flag[i] -= a1[i]
print("".join([chr(a&0xff) for a in flag]))

# hgame{y0ur_rever5e_sk1ll_i5_very_g0od!!}
```

## [强网杯 2024 easy_vm]
接触完了去年的我们来看看强网杯的vm吧
- 查壳  
![](https://gitee.com/fogpost/photo/raw/master/202411021111059.png)
- ida分析  
![](https://gitee.com/fogpost/photo/raw/master/202411021116697.png)
这次的区块有点大，我们逐段来分析一下


