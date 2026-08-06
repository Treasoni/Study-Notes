# 轻量智能家居 Agent 镜像
# 运行方式（host 网络，直连 127.0.0.1:8123 的 Home Assistant）：
#   docker build -t ha-agent .
#   docker run --network host -e HA_BASE_URL=http://127.0.0.1:8123 -e DEEPSEEK_API_KEY=xxx -e HA_TOKEN=yyy ha-agent
FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 只拷贝运行必需文件；.env 通过 -e / --env-file 注入，避免把密钥烤进镜像
COPY main.py tools.py entity_map.py entity_map.yaml ./

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
