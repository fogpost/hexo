---
title: bindiff
date: 2024-10-28 14:58:37
categories: 逆向
tags: tool
updated: 2024-10-28T14:58:37+08:00
---
# 用bindiff来显示二进制文件的区别
你是否在面对收到攻击的二进制文件无法比对，看着两个文件而陷入迷茫，不知如何分析，沉沦在函数之海无法自拔，找不到patcher前后的区别，那么bindiff可以帮助你。

### 1. 自行安装

### 2.使用  
首先我们打开一个我们所需要分析的软件，在ida完成分析之后我们退出将对应的.ida64包文件保存，然后加载patcher后的文件，在ida中键入crtl+6，使用bindiff插件  
![](https://gitee.com/fogpost/photo/raw/master/202410281503232.png)  
选择Diff DAtabase，选择刚刚保存的.ida64文件,出现对应的对比框
![](https://gitee.com/fogpost/photo/raw/master/202410281504805.png)  
在这个绿色框口下我们发现，在最下方的函数extract_dirs_from_files，与原来的文件对比，有仅0.84的相似度，我们便可以知道两个二进制文件在这个函数发生了区别
![](https://gitee.com/fogpost/photo/raw/master/202410281506283.png)
查看函数,在patcher中发现多了如下一个分支
```c++
LABEL_7:
        if ( v9 && !v9[1] )
        {
          *(_QWORD *)&lmao[8] = 0x3F7D132A2A252822LL;
          *(_QWORD *)lmao = 0x7D2E370A180F1604LL;
          *(_QWORD *)&lmao[24] = 0x31207C7C381320LL;
          *(_QWORD *)&lmao[16] = 0x392A7F3F39132D13LL;
          v18 = lmao;
          do
            *v18++ ^= **(_BYTE **)v7;
          while ( &lmao[31] != v18 );
          puts(lmao);
        }
        goto LABEL_9;
      }
      if ( !dirname )
        goto LABEL_21;
      component = last_component(*(const char **)v7);
      if ( *component == 46 )
      {
        v17 = component[(component[1] == 46) + 1];
        if ( !v17 || v17 == 47 )
          goto LABEL_7;
      }
      if ( *v9 == 47 )
      {
```
我们经过cyberchef的函数爆破，来获得最终的数据，注意在数组中存在大小端序的问题
![](https://gitee.com/fogpost/photo/raw/master/202410281511684.png)
[题目来源](https://www.nssctf.cn/problem/3687)