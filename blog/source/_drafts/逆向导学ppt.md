---
title: 逆向ppt
date: 2026-01-19T18:49:00
tags:
  - ctf
updated: 2026-01-27T20:21:02+08:00
---
# 开篇想说的话


- CTF 逆向在“逆”什么（入门认知 + 工具）
- 汇编不是敌人（逆向核心能力）
- 动态调试 = 逆向作弊器
- CTF 常见套路总结 + 进阶指路


```
本节课前提下载好群内下发的reverse文件
提前下好python
```
# CTF 逆向在“逆”什么（入门认知 + 工具）
一句话解释就是CTF逆向就是在静态程序中获取flag的检查逻辑，然后利用获取逻辑反推出逆向的flag。
## 常见的CTF形态
- crackme/flag校验
- 算法还原（base / xor / crc / 自定义 hash）
- 简单 VM / 花指令（点到为止）
## 工具（Windows方向）
初学者要了解的主要是工具的种类和用法，同web工具而言，逆向也有以下几个步骤，我顺带将各个流程工具写上
- 信息收集。（IDE，PEinfo）
IDE
![image.png](https://gitee.com/fogpost/photo/raw/master/202601221717345.png) 
PEinfo
![image.png](https://gitee.com/fogpost/photo/raw/master/202601221717988.png)

- 静态：
    - IDA / Ghidra（函数、字符串、交叉引用）
- 动态：
    - x64dbg（Windows）
    - gdb + pwndbg（Linux）

我们Windows电脑主要用的就是ida和x64的组合，x64有很多插件现在文件中的是纯净版
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
    - mov / lea / cmp / jmp / call / test 汇编指令
    - eax/ebx/ecx/edx 基本寄存器

>**RAX**：**“返回值之王”**。函数执行完后的结果（比如 `compare` 的结果 `0`）永远放在这里
>RIP：“指挥棒”。指向下一条要执行的指令地址。如果你修改了它，就能控制程序跳转到任何地方。
>RCX, RDX, R8, R9：“传参四大天王”。在 Windows x64 下，函数的前四个参数直接装在这四个寄存器里往函数里送。
>RSP：“栈顶指针”。永远指向当前“储物间”的最顶层。
![image.png](https://gitee.com/fogpost/photo/raw/master/202601252033095.png)


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

基础的strcmp
```c
; 假设 RCX 指向 str1, RDX 指向 str2
lea     rdx, [rbp+var_str2]    ; 将用户输入的地址传给 RDX
lea     rcx, [rbp+var_str1]    ; 将预设 Flag 的地址传给 RCX
call    std::string::compare   ; 调用比较函数
mov     [rbp+var_result], eax  ; 将返回值存入 result 变量

; --- 核心校验逻辑 ---
cmp     [rbp+var_result], 0    ; 比较结果是否为 0
jne     short loc_error_path   ; 如果不等于 0 (Jump if Not Equal)，跳到错误提示

; --- 正确路径 ---
lea     rcx, offset aCorrect   ; "Correct! You find the flag"
call    std::cout::operator<<
jmp     short loc_exit

loc_error_path:
lea     rcx, offset aTryIda    ; "Try the ida or dbg"
call    std::cout::operator<<
```
F5伪代码
```c
int __cdecl main() {
  // 局部变量声明
  char str1[32]; 
  char str2[32];
  int result;

  // 1. 初始化字符串
  std::string::string(str1, "Flag{example_strcmp}");
  
  // 2. 获取输入
  std::cout << "Enter the flag: ";
  std::getline(&std::cin, str2);

  // 3. 比较逻辑
  result = std::string::compare(str1, str2);

  // 4. 分支判断
  if ( result == 0 ) {
    std::cout << "Correct! You find the flag" << "\n";
  } else {
    std::cout << "Try the ida or dbg" << "\n";
  }

  return 0;
}
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

###  经典骚操作
- 直接修改寄存器
- patch 掉 jnz / jz
- 改返回值
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

### 进阶学习路线（为你后续课程铺路）
- 壳 / 反调试
UPX和isdebugger
- 混淆 / 虚拟机
简单的vm虚拟机和ollvm控制流平坦化
- Malware / 实战逆向