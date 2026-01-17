
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

on:
  push:
    branches:
      - main
        
jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      # 1️⃣ 拉取仓库
      - name: Checkout code
        uses: actions/checkout@v4

      # 2️⃣ 安装 Node.js
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 20

      # 3️⃣ 配置 Git 用户信息
      - name: Configure Git
        run: |
          git config --global user.name "github-actions"
          git config --global user.email "github-actions@github.com"

      # 4️⃣ 安装 Hexo 依赖
      - name: Install dependencies
        run: |
          cd blog
          npm install

      # 5️⃣ Hexo 生成 & 部署（兼容 Fine-grained token）
      - name: Hexo Deploy
        env:
          GH_PAT: ${{ secrets.GH_PAT }}  # Fine-grained token
        run: |
          cd blog
          npx hexo clean
          npx hexo generate
          # 🔥 覆盖远程 URL，用用户名 + Fine-grained token
          git remote set-url origin https://fogpost:${GH_PAT}@github.com/fogpost/hexo.git
          git add -A
          git commit -m "Deploy Hexo site" || echo "No changes to commit"
          git push origin HEAD:web --force
```
