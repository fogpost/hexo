
## 换源
```
sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak
sudo nano /etc/apt/sources.list
deb http://mirrors.ustc.edu.cn/kali kali-rolling main non-free contrib
deb-src http://mirrors.ustc.edu.cn/kali kali-rolling main non-free contrib
sudo apt update
```

## docker
# 1️⃣ Docker 版本 & 信息

docker version          # 查看客户端和服务端版本  
docker info             # 查看 Docker 系统详细信息（镜像、容器、存储驱动等）  
docker system info      # 系统信息（类似 docker info）  
docker context ls       # 查看当前 Docker 上下文

---

# 2️⃣ 镜像管理

docker pull <image>                 # 从 Docker Hub 或镜像仓库拉镜像  
docker build -t <name:tag> .        # 从 Dockerfile 构建镜像  
docker images / docker image ls     # 查看本地镜像列表  
docker rmi <image_id|name:tag>      # 删除本地镜像  
docker save -o <file.tar> <image>   # 保存镜像为 tar 文件  
docker load -i <file.tar>           # 导入镜像 tar 文件  
docker tag <image> <repo:tag>       # 给镜像打标签  
docker push <repo:tag>              # 推送镜像到仓库


>💡 Vulhub 常用：`docker pull vulhub/<cve>:<version>` 或 `docker-compose build`

# 3️⃣  容器管理

docker run -it --name <container> <image>        # 直接运行容器并进入终端  
docker run -d --name <container> <image>        # 后台运行容器  
docker ps                                       # 查看正在运行的容器  
docker ps -a                                    # 查看所有容器（包括停止的）  
docker stop <container>                          # 停止容器  
docker start <container>                         # 启动已停止容器  
docker restart <container>                       # 重启容器  
docker rm <container>                            # 删除容器（必须先停止）  
docker exec -it <container> /bin/bash           # 进入运行中的容器终端  
docker logs -f <container>                      # 查看容器日志  
docker inspect <container>                      # 查看容器详细信息（IP、端口映射等）  
docker stats                                    # 实时查看容器资源使用情况

---

# 4️⃣ Docker Compose

docker-compose up                # 启动 docker-compose.yml 定义的服务  
docker-compose up -d             # 后台启动  
docker-compose build             # 构建服务镜像  
docker-compose down              # 停止并删除容器/网络  
docker-compose logs -f           # 查看服务日志  
docker-compose ps                # 查看服务运行状态  
docker-compose restart           # 重启服务  
docker-compose pull              # 拉取服务镜像

>⚡ Vulhub 靶场通常使用 `docker-compose up -d` 一键启动漏洞环境

- 查看容器 IP（方便漏洞访问）：
    

>docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' <container>

- 停止所有 Vulhub 容器：
    

>docker stop $(docker ps -aq --filter "name=vulhub")