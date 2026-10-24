# ---------- 构建阶段 ----------
FROM python:3.12-slim AS builder

WORKDIR /app

# 先复制依赖清单，利用 Docker 层缓存：依赖不变时不用重装
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ---------- 运行阶段 ----------
FROM python:3.12-slim

WORKDIR /app

# 非 root 用户运行，更安全
RUN useradd --create-home appuser

# 只带运行时依赖
COPY --from=builder /install /usr/local
COPY app.py .

USER appuser

EXPOSE 8080

ENV PORT=8080 PYTHONUNBUFFERED=1

HEALTHCHECK --interval=30s --timeout=3s \
  CMD python -c "import urllib.request;urllib.request.urlopen('http://localhost:8080/api/health')" || exit 1

CMD ["python", "app.py"]
