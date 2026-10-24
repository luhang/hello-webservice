from datetime import datetime, timezone, timedelta
import socket, os, platform
from flask import Flask, jsonify

app = Flask(__name__)

JST = timezone(timedelta(hours=9))
START = datetime.now(JST)

PAGE = """<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Docker Web Service</title>
<style>
  * { box-sizing: border-box; margin: 0; }
  body {
    font-family: "Hiragino Sans", "Yu Gothic", "Microsoft YaHei", system-ui, sans-serif;
    background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
    color: #F1F5F9; min-height: 100vh;
    display: flex; align-items: center; justify-content: center; padding: 24px;
  }
  .card {
    background: rgba(255,255,255,.06); border: 1px solid rgba(255,255,255,.12);
    border-radius: 20px; padding: 40px 44px; max-width: 560px; width: 100%;
    backdrop-filter: blur(8px); box-shadow: 0 20px 60px rgba(0,0,0,.35);
  }
  .badge {
    display: inline-flex; align-items: center; gap: 8px;
    background: rgba(16,185,129,.15); color: #34D399;
    border: 1px solid rgba(16,185,129,.3);
    border-radius: 999px; padding: 5px 14px; font-size: 13px; font-weight: 700;
  }
  .dot { width: 8px; height: 8px; border-radius: 50%; background: #34D399;
    box-shadow: 0 0 8px #34D399; animation: pulse 1.6s infinite; }
  @keyframes pulse { 50% { opacity: .4; } }
  h1 { font-size: 26px; margin: 18px 0 6px; letter-spacing: .02em; }
  .sub { color: #94A3B8; font-size: 14px; margin-bottom: 26px; }
  table { width: 100%; border-collapse: collapse; font-size: 14px; }
  td { padding: 10px 0; border-bottom: 1px solid rgba(255,255,255,.08); }
  td:first-child { color: #94A3B8; width: 42%; }
  td:last-child { font-variant-numeric: tabular-nums; font-weight: 600; }
  tr:last-child td { border-bottom: none; }
  .links { margin-top: 26px; display: flex; gap: 10px; flex-wrap: wrap; }
  a {
    color: #60A5FA; text-decoration: none; font-size: 13.5px;
    border: 1px solid rgba(96,165,250,.35); border-radius: 10px; padding: 8px 16px;
    transition: background .2s;
  }
  a:hover { background: rgba(96,165,250,.12); }
</style>
</head>
<body>
  <div class="card">
    <span class="badge"><span class="dot"></span> Service Running in Docker</span>
    <h1>你好，来自容器的问候 👋</h1>
    <p class="sub">这个页面由 Docker 容器内的 Flask 服务渲染PPP</p>
    <table>
      <tr><td>容器主机名</td><td>__HOSTNAME__</td></tr>
      <tr><td>容器内 Python</td><td>__PYVER__</td></tr>
      <tr><td>服务启动时间</td><td>__START__</td></tr>
      <tr><td>当前容器时间</td><td>__NOW__</td></tr>
      <tr><td>访问端口</td><td>__PORT__</td></tr>
    </table>
    <div class="links">
      <a href="/api/info">GET /api/info</a>
      <a href="/api/time">GET /api/time</a>
      <a href="/api/health">GET /api/health</a>
    </div>
  </div>
</body>
</html>"""


@app.route("/")
def index():
    now = datetime.now(JST)
    html = (PAGE
            .replace("__HOSTNAME__", socket.gethostname())
            .replace("__PYVER__", platform.python_version())
            .replace("__START__", START.strftime("%Y-%m-%d %H:%M:%S JST"))
            .replace("__NOW__", now.strftime("%Y-%m-%d %H:%M:%S JST"))
            .replace("__PORT__", os.environ.get("PORT", "8080")))
    return html


@app.route("/api/info")
def info():
    return jsonify({
        "service": "docker-webservice",
        "hostname": socket.gethostname(),
        "python": platform.python_version(),
        "started_at": START.isoformat(),
    })


@app.route("/api/time")
def time_api():
    return jsonify({"koto now": datetime.now(JST).isoformat(), "tz": "Asia/Tokyo"})


@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "uptime_sec": int((datetime.now(JST) - START).total_seconds())})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
