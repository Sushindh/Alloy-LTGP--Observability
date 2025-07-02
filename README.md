# 📡 Flask Observability App - LTGP Stack Enabled

<div align="center">

![Flask](https://img.shields.io/badge/Flask-Backend-000000?style=for-the-badge)
![OpenTelemetry](https://img.shields.io/badge/OpenTelemetry-Enabled-orange?style=for-the-badge)
![Grafana](https://img.shields.io/badge/Grafana-Dashboard-orange?style=for-the-badge)
![Prometheus](https://img.shields.io/badge/Prometheus-Metrics-brightgreen?style=for-the-badge)
![Loki](https://img.shields.io/badge/Loki-Logs-blue?style=for-the-badge)
![Tempo](https://img.shields.io/badge/Tempo-Traces-yellow?style=for-the-badge)

**A minimal Flask app instrumented with OpenTelemetry and Grafana Alloy to visualize metrics, logs, and traces using Prometheus, Loki, and Tempo**

</div>

---

## 🎯 Purpose

This project demonstrates observability instrumentation for a simple Flask application using OpenTelemetry and the **LTGP stack** — **Loki**, **Tempo**, **Grafana**, and **Prometheus** — with **Grafana Alloy** as the collector.

---

## 🌟 Impact

| Feature                  | Benefit                                               |
|--------------------------|--------------------------------------------------------|
| 📈 **Metrics Collection**   | Track endpoint usage, performance, and traffic trends |
| 📜 **Logs Aggregation**     | Centralized and structured logging with context        |
| 🔍 **Tracing Support**      | End-to-end request flow and latency insights          |
| ⚙️ **Lightweight Setup**    | Ideal for learning observability or prototyping       |

---

## ⚙️ Features

### 🔗 Endpoints

| Method | Endpoint     | Description          |
|--------|--------------|----------------------|
| GET    | `/home`      | Simulates Home page  |
| GET    | `/cart`      | Simulates Cart page  |
| GET    | `/payment`   | Simulates Payment    |

### 📊 Observability

- ✅ Metrics via Prometheus
- ✅ Logs via Loki
- ✅ Traces via Tempo
- ✅ Grafana Dashboards for visualization
- ✅ Logs enriched with endpoint, trace ID, and span ID

---

## 🏗️ Architecture

```mermaid
graph TD
    A[Flask App] -->|OTLP Exporter| B[Grafana Alloy]
    B -->|Metrics| C[Prometheus]
    B -->|Logs| D[Loki]
    B -->|Traces| E[Tempo]
    C --> F[Grafana]
    D --> F
    E --> F

🚀 Getting Started
📦 Prerequisites
Docker + Docker Compose

Python 3.9+

Git

🧑‍💻 Run the App
Clone the repository

bash
Copy
Edit
git clone https://github.com/your-username/flask-observability-app.git
cd flask-observability-app
Build and Start the stack

bash
Copy
Edit
docker-compose up --build
Access endpoints

http://localhost:5000/home

http://localhost:5000/cart

http://localhost:5000/payment

Explore Observability Tools

Tool	URL	Use Case
Grafana	http://localhost:3000	Dashboards
Prometheus	http://localhost:9091	View collected metrics
Loki	http://localhost:3100	Logs API
Tempo	http://localhost:3200	Traces API

📌 Grafana Login: admin / admin

📂 Project Structure
bash
Copy
Edit
flask-observability-app/
├── app.py                  # Flask app with OpenTelemetry
├── Dockerfile              # Build Flask image
├── docker-compose.yml      # Multi-service orchestration
├── config.alloy            # Grafana Alloy configuration
├── prometheus.yml          # Prometheus config
├── tempo.yaml              # Tempo config
└── requirements.txt        # Python dependencies
🔧 Technologies Used
🐍 Flask

📦 OpenTelemetry (metrics, logs, traces)

📊 Prometheus

📜 Loki

🔍 Tempo

📈 Grafana

🔄 Grafana Alloy

🐳 Docker & Docker Compose

📊 Metrics Example
Prometheus Counter:

python
Copy
Edit
compute_request_count = meter.create_counter(
    name="app_compute_request_count",
    description="Counts the requests",
    unit="1"
)
Metrics by endpoint:

app_compute_request_count{endpoint="/home"}

app_compute_request_count{endpoint="/cart"}

app_compute_request_count{endpoint="/payment"}

📜 License
This project is licensed under the MIT License.
Feel free to fork, modify, and use for your own learning or observability setups.

<div align="center">
⭐ Star this repo if you found it helpful
📬 Made by Sushindh A

</div> ```
