FROM python:3.10-slim

# 设置工作目录为 /app
WORKDIR /app

# 将项目中的所有文件复制到容器的 /app 目录下
COPY . .

# 安装依赖项
RUN pip install -r requirements.txt

# 暴露 Flask 应用运行的端口（假设 Flask 应用监听在 8000 端口）
EXPOSE 8000

# 启动 Flask 应用
CMD ["python", "main.py"]
