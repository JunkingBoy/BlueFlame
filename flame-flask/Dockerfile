FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 将当前目录的内容复制到工作目录中
COPY . /app

# 安装 Python 包
RUN pip install --no-cache-dir -r requirements.txt

# 暴露应用运行的端口
EXPOSE 5000

# 运行 Flask 应用
CMD ["python", "-m main"]


# 构建镜像
# docker build -t bf .

# 运行镜像
# docker run -p 5000:8000 bf
