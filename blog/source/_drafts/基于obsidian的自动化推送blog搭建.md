
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

完成推送后两种方案，一种github自带的githubaction，或者vercal单独设构建都行我们采取第一种，并利用obsdian的git插件实现自动化,不行不行这个不用密钥的太搞了，建议各位想要搭建的去用vercel或者直接用密钥。
``` 
name: Hexo Deploy

on:
  push:
    branches:
      - main

permissions:
  contents: write

jobs:
  build-deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout source
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 20

      - name: Setup git identity
        run: |
          git config --global user.name "github-actions[bot]"
          git config --global user.email "github-actions[bot]@users.noreply.github.com"

      - name: Install dependencies
        run: |
          cd blog
          npm install

      # 关键修复 ①：先生成 public + deploy 仓库
      - name: Hexo generate
        run: |
          cd blog
          npx hexo clean
          npx hexo generate

      # 关键修复 ②：给 .deploy_git 强制写入带 token 的 remote
      - name: Fix deploy git remote
        run: |
          cd blog/.deploy_git
          git remote set-url origin https://x-access-token:${{ secrets.GITHUB_TOKEN }}@github.com/${{ github.repository }}.git

      # 最终部署
      - name: Hexo deploy
        run: |
          cd blog
          npx hexo deploy

```
