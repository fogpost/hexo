Dockerfile：用于 **构建 Docker 镜像的脚本**
```dockerfile
FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python","app.py"]
```

使用流程：
1. 构建镜像
>docker build -t myapp .
2. 运行容器
> docker run -d -p 8000:8000 myapp

我写过 Dockerfile，用于打包 Python 项目部署。  
一般流程是先选择基础镜像，比如 python:3.10，然后设置工作目录、复制依赖文件、安装依赖，再复制代码，最后指定启动命令。  
构建镜像用 docker build，运行容器用 docker run，并通过端口映射对外提供服务。

比如部署 FastAPI 服务时会把项目打包成镜像，然后通过 docker run 启动。

docker的部署和设置代理
```bash
sudo nano /etc/docker/daemon.json

{
  "registry-mirrors": [
    "https://dockerproxy.com",
    "https://hub-mirror.c.163.com"
  ],
  "dns": ["8.8.8.8", "1.1.1.1"]
}
```
