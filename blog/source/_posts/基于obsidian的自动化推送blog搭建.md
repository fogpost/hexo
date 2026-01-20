---
title: 基于obsidian的自动化推送blog搭建
date: 2026-01-17 20:13:37
tags:
  - blog
created: 2026-01-18T12:49
updated: 2026-01-17 20:13:37
---

(这个好蠢呀，突然发现没标题没标签，难搞，难不成每次还要复制，看来下一下还要搞个什么自动化创建标签才行)

好久没有写blog了，考完研旅完游之后在家里面看了一点点32汇编的书之后发现还有一门c语言考试没完结，要是我没考过的话就得重读大四了，直接延毕，然后可以去考更好的大学研了，不过说到这个我还有一些关于转专业的想说的话，不过中心不在这（[[关于转专业想说的话]]），接下来开始讲blog搭建吧

本blog基于eviden博客优化希望可以比原版更易上手与理解  
[# 实现obs"蛋"结合hexo推送GitHub自动化工作流](https://www.eviden7.tech/%E7%BB%83%E4%B9%A0Obs'%E8%9B%8B'/)

```
git init                                                #初始化git  
git remote add origin `github仓库链接`  #与远程仓库建立连接  
git add .                                               #至暂存区  
git commit -m "初始化"                                   #添加至本地仓库  
git push -u origin main                                 
#推送至远程的main分支,这是生成后的我们要展示的网页分支
  
git checkout -b hexo             #该命令相当于 git branch hexo 以及 git checkout hexo，前者是创建分支 hexo，后者是切换到 hexo分支。  
  
git push origin HEAD -u


```

完成推送后两种方案，一种github自带的githubaction，或者vercal单独设构建都行我们采取第一种，并利用obsdian的git插件实现自动化,不行不行这个不用密钥的太搞了，建议各位想要搭建的去用vercel或者直接用密钥。原因就是这个方案外面一层main的要识别身份，内层更新web页面也需要识别身份所以有两次检验，有密钥就不需要了。
``` 
name: Hexo Deploy
permissions:
  contents: write  # 允许插件推送到你的 web 分支
  
on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 20

      - name: Install dependencies
        run: |
          cd blog
          npm install

      - name: Build Hexo
        run: |
          cd blog
          npx hexo clean
          npx hexo generate
          # 在生成的静态文件根目录生成这两个关键文件
          # touch public/.nojekyll
          # echo "你的域名.com" > public/CNAME  # 👈 这里填入你的真实域名
          
      - name: Deploy to Web Branch
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }} 
          # 使用内置 Token 即可，无需手动配置 PAT
          publish_dir: ./blog/public               # 👈 只发布这个目录下的内容
          publish_branch: web                      # 👈 发布到 web 分支
          force_modify: true                       # 强制覆盖
```

下面是成功的显示
![image.png](https://gitee.com/fogpost/photo/raw/master/202601171958945.png)
这下就行了可以看到我们的两步走在mian备份完全部文件后在web分支下完成页面部署实现了自动化，下次想在其他电脑上面部署就可以直接git clone了

需要注意的是刚刚才发现要配图床，图床这个我之前就讲过了[[可恶的gitee吃掉外链了]] 放外链的方式也有直接用就行，不过本地不能够离线看图片确实有点，但是其实你知道么，所有考win+shift+s截的图全会在你的个人用户的图片下面不会删掉，但是因为像素不高几百张好像就几十MB也不大留着就行。

到此未知我们彻底摆脱了onedirve的云端存储，利用github来实现了笔记的自动存储与上传，这几天我看了一下我的notion发现25年大部分我想说的东西其实写在notion上了没有更新，之后要好好整理一下。

最后来讲讲几者的区别。
⭐⭐⭐⭐⭐肯定是以obsidian为基础的自动化推送
这中间我觉得用vercel会好很多少很多配置，但是会多一个流程，能够保护源码也是重要的一环，主要是怕别人修改吧
⭐⭐⭐说实话我的onediver云端存储确实在早期提供了帮助，给了我一个很好的平台去写
⭐本地的还是写在纸上不如

不知不觉写了这么多字已经20:00了，该回去了，视频还没录呢。