
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
