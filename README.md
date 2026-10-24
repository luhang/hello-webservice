# hello-webservice

跑在 Docker 里的一个小型 Web 服务（Python + Flask），用于演示容器化开发的完整流程。

## 快速开始

```bash
# 构建镜像
docker build -t hello-webservice:1.0 .

# 启动容器（映射到本机 8080 端口，开机自动重启）
docker run -d --name hello-web --restart unless-stopped -p 8080:8080 hello-webservice:1.0
```

浏览器打开 <http://localhost:8080> 即可访问。

## 接口

| 路径 | 说明 |
|---|---|
| `GET /` | 服务首页 |
| `GET /api/info` | 服务信息（主机名、Python 版本、启动时间） |
| `GET /api/time` | 当前时间（Asia/Tokyo） |
| `GET /api/health` | 健康检查（容器 HEALTHCHECK 依赖此接口） |

## 项目结构

```
webservice/
├── app.py              # Flask 应用（页面 + API）
├── Dockerfile          # 多阶段构建、非 root 用户、自带 HEALTHCHECK
├── requirements.txt    # Python 依赖
├── .dockerignore       # 构建时排除的文件
└── .gitignore
```

## 常用命令

```bash
docker logs hello-web        # 查看日志
docker stop hello-web        # 停止
docker start hello-web       # 启动
docker rm -f hello-web       # 删除容器（重建前需要）
```
