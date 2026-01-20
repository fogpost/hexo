---
title: sicctfwp
date: 2024-11-01 22:15:18
categories: CTF
tags: ctf
updated: 2024-11-01 22:15:18
---
# web
## Sigin
打开网页后出现这个页面
![](https://gitee.com/fogpost/photo/raw/master/202411012216221.png)
典型的robots协议，访问robots.txt
按照提示进入，发现一下界面
![](https://gitee.com/fogpost/photo/raw/master/202411012217411.png)
在本地弄一个php环境跑一下出了这个
> system(get_deined_vars()[_GET)][W3lc0me_t0_SICTF.2024])  

简单来说就是将W3lc0me_t0_SICTF.2024作为system的get参数，多亏了有蒋✌教,这里存在一个php特性就是不能过多的下划线要改为W3lc0me_t0\[SICTF.2024这个才行
>http://27.25.151.29:33218/wh3re_1s_thi5_fl4g.php?W3lc0me_t0[SICTF.2024=cat /flag
SICTF{e79dbf83-bce6-4545-a9d7-53c527f3f13c} 

# reverse
## Exc??
感觉和之前moectf的一个很像，直接打开看看
将这个xlsx分为一下几个模块
- 输入输出模块
![](https://gitee.com/fogpost/photo/raw/master/202411012230759.png)
- 算法模块
![](https://gitee.com/fogpost/photo/raw/master/202411012231237.png)
先看wrong格中的内容  


>IF(C3=D19,IF(F3=G19,IF(I3=J19,IF(L3=D21,IF(O3=G21,IF(R3=J21,IF(U3=D23,IF(X3=G23,IF(AA3=J23,

>IF(D13=Q19,IF(G13=T19,IF(J13=W19,IF(D15=Q21,IF(G15=T21,IF(J15=W21,IF(D17=Q23,IF(G17=T23,IF(J17=W23,

>IF(D31=AT10,IF(G31=AW10,IF(J31=AZ10,IF(M31=AT12,IF(P31=AW12,IF(S31=AZ12,IF(V31=AT14,IF(Y31=AW14,IF(AB31=AZ14,"Accepted!")))))))))))))))))))))))))))

  发现存在一个accpted，去找这个实现条件，发现是输入输出模块中的数要与算法模块中的紫色数据块相同
继续找紫色output的实现函数

分别如下
=BITLSHIFT(CODE(C2),3)+BITLSHIFT(CODE(D2),4)+BITLSHIFT(CODE(E2),5)
第二个是
=CODE(C2)*3+CODE(D2)*4+CODE(E2)*5
第三个是
=CODE(C2)*CODE(D2)+CODE(D2)*CODE(E2)+CODE(E2)*CODE(C2)

解释一下几个函数
BITLSHIFT(number, shift_amount)：执行左移操作
CODE(text)：将文本转换为ASCII码
```py
enc = [3976, 5728, 5640, 4232, 5272, 3776, 6464, 6136, 5408]
enc1 = [876, 1147, 1182, 824, 1082, 866, 1361, 1278, 1087]
enc2 = [16511, 24822, 26991, 11999, 21215, 16374, 37800, 32739, 21505]

for l in range(0, 9):
    found = False  # 初始化找到标志
    for i in range(32, 127):
        for j in range(32, 127):
            for k in range(32, 127):
                # 使用 and 代替 &
                if (i * 8 + j * 16 + k * 32 == enc[l] and 
                    i * 3 + j * 4 + k * 5 == enc1[l] and 
                    i * j + j * k + k * i == enc2[l]):
                    print(f"{chr(i)}{chr(j)}{chr(k)}",end="")
                    found = True  # 设置找到标志
                    break  # 跳出内层循环
            if found:  # 如果找到匹配，则跳出中间循环
                break
        if found:  # 如果找到匹配，则跳出外层循环
            break

```
SICTF{Exc31_1s_r3@lly_fun!}