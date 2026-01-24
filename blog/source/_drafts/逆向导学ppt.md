---
title: 逆向ppt
date: 2026-01-19T18:49:00
tags:
  - ctf
updated: 2026-01-24T14:36:50+08:00
---
# 开篇想说的话
我去刚刚准备写ppt的时候发现我obsidian没有重命名和自动化创建标签的功能，不过还好社区的template和quickadd给我们提出了解决办法，不过现在还是先来好好写我们的ppt吧，下午本来三点中想写的不过睡了一觉就到6点了🤭。之后还要写毕设呢，不然脑袋痛
逆向导学打算按照接下来这四个方面写好，感觉这么多当导学都45min讲不完。

- CTF 逆向在“逆”什么（入门认知 + 工具）
- 汇编不是敌人（逆向核心能力）
- 动态调试 = 逆向作弊器
- CTF 常见套路总结 + 进阶指路
# CTF 逆向在“逆”什么（入门认知 + 工具）
一句话解释就是CTF逆向就是在静态程序中获取flag的检查逻辑，然后利用获取逻辑反推出逆向的flag。
## 常见的CTF形态
- crackme/flag校验
- 算法还原（base / xor / crc / 自定义 hash）
## 工具（Windows方向）
初学者要了解的主要是工具的种类和用法，同web工具而言，逆向也有以下几个步骤，我顺带将各个流程工具写上
- 信息收集。（IDE，PEinfo）
IDE
![image.png](https://gitee.com/fogpost/photo/raw/master/202601221717345.png) 
PEinfo
![image.png](https://gitee.com/fogpost/photo/raw/master/202601221717988.png)

目前用到的主要功能
- Strings
- main / WinMain
- 函数调用关系，相互引用
- 下断点 / 单步 / 看寄存器
# 汇编不是敌人（逆向核心能力）
汇编这个东西目前来说就8086汇编后面的win32汇编和arm汇编都可放后面一点（我怎么总记得还有一个和8086不一样的int汇编，但是这不是一家的么）汇编是一种软件分析工具攻击
## 必须会的汇编
- x86/x64 基础
- 常见指令：
    - mov / lea / cmp / jmp / call / test
```c
mov eax, 1        ; eax = 1
mov ebx, eax      ; ebx = eax
mov eax, [ebp-4]  ; 从内存读到寄存器
mov [ebp-8], eax  ; 从寄存器写到内存

lea eax, [ebp-4]      ; eax = &var
lea eax, [eax+4]      ; eax = eax + 4
lea eax, [eax*2+10]   ; eax = eax*2 + 10

cmp eax, 5
cmp eax, ebx
cmp [ebp-4], 0

jmp 0x401000
jmp short loc_123

call 0x401050
call eax

test eax, eax
test al, 1
```
- 栈、寄存器、函数调用
## 举例从 C → 汇编 → 反编译

举例：
```c++
    // 这是 "Flag{Hello_CTF}" 每个字符异或 0x55 后的结果
    // 这样用户输入正常的 Flag{...}，程序内部异或后去对比这些“乱码”
    unsigned char cipher[] = {
        0x13,0x39,0x34,0x32,0x2e,0x1d,0x30,0x39,
        0x39,0x3a,0x0a,0x16,0x01,0x13,0x28
    };
    string in;
    cout << "Enter Flag: ";
    cin >> in;
    if (in.length() != sizeof(cipher)) return 0;
    for (int i = 0; i < in.length(); i++) {
        // 用户输入可见字符 (如 'F')，异或 0x55 后与密文对比
        if ((unsigned char)(in[i] ^ 0x55) != cipher[i]) {
            cout << "Wrong!" << endl;
            return 0;
        }
    }
    cout << "Correct!" << endl;
```
 在 IDA 里对应哪几行？
利用F5可以看到主函数的伪代码
![image.png](https://gitee.com/fogpost/photo/raw/master/202601221715777.png)

 怎么一眼看出这是 XOR 校验？
![image.png](https://gitee.com/fogpost/photo/raw/master/202601221640600.png)
###  实战小题
- xor + for 循环
- flag 存在 cipher 段
- 轻度反编译即可还原
```python
cipher=[0x13,0x39,0x34,0x32,0x2e,0x1d,0x30,0x39,0x39,0x3a,0x0a,0x16,0x01,0x13,0x28]
for i in cipher:
    print(chr(i^0x55),end="")
```
---

# 第三章：动态调试 = 逆向作弊器

> 目标：**教他们“偷懒”而不是硬看**
---
###  为什么要调试

- 反编译看不懂
- 算法太绕
- 有反调试 / 花指令
---
###  动态调试核心技巧
- 下断点：
    - strcmp
    - 校验函数入口
- 单步跟
- 看寄存器 / 内存
- 条件跳转观察
📌 强调：
> **调试是为了“绕过思考成本”**
---
###  经典骚操作
- 直接修改寄存器
- patch 掉 jnz / jz
- 改返回值

---
###  demo 题
- flag 不直接出现
- 程序算完再比
- 用调试直接 dump 结果

---
# 第四章：CTF 常见套路总结 + 进阶指路

### 解题流程模板

给他们一个**标准 checklist**：
1. strings
2. 找 main
3. 找输入
4. 找校验
5. 静态 or 动态
6. 写脚本还原
---
### 常见误区
- 死磕汇编
- 不下断点
- 不利用程序自身