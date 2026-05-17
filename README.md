# Kubernetes Deployment — RAG System API

Production-grade Kubernetes deployment of a FastAPI RAG inference API.
Runs 2 pod replicas with rolling update strategy, liveness and readiness
health checks, resource limits, and NodePort service exposure.

Live AWS deployment: http://3.71.32.203:8000/docs
RAG Demo: https://rohith2026-hybrid-rag-demo.hf.space

---

## What I Built

Containerised a FastAPI application and deployed it to a Kubernetes cluster
using minikube. The deployment demonstrates production engineering practices:
multiple replicas for availability, rolling updates for zero-downtime
deployments, health probes for automatic recovery, and resource limits
for cluster stability.

---

## Architecture

    Client Request
          |
          v
    Kubernetes Service
    (NodePort 30080)
          |
          v
    +---------------------------+
    |   Kubernetes Deployment   |
    |   rag-api                 |
    |   RollingUpdate strategy  |
    +---------------------------+
          |              |
          v              v
    +-----------+  +-----------+
    | Pod 1     |  | Pod 2     |
    | rag-api   |  | rag-api   |
    | :8000     |  | :8000     |
    |           |  |           |
    | /health   |  | /health   |
    | /info     |  | /info     |
    | /docs     |  | /docs     |
    +-----------+  +-----------+
          |              |
          v              v
    Docker Container (python:3.11-slim)
    FastAPI + uvicorn


---

## Deployment Configuration

| Setting | Value | Why |
|---------|-------|-----|
| Replicas | 2 | High availability — one pod can fail without downtime |
| Update strategy | RollingUpdate | Zero-downtime deployments |
| Max unavailable | 1 | At least 1 pod always running during updates |
| Max surge | 1 | 1 extra pod during rollout for smooth transition |
| Memory request | 128Mi | Guaranteed memory for scheduling |
| Memory limit | 256Mi | Prevents one pod consuming all node memory |
| CPU request | 250m | Guaranteed CPU allocation |
| CPU limit | 500m | Prevents CPU starvation of other workloads |
| Liveness probe | GET /health every 30s | Restarts unhealthy pods automatically |
| Readiness probe | GET /health every 10s | Stops traffic to pods not yet ready |
| Restart policy | Always | Pods always restarted on failure |

---

## Project Files

| File | Purpose |
|------|---------|
| app.py | FastAPI application — 3 REST endpoints |
| Dockerfile | Container image — python:3.11-slim base |
| requirements.txt | Minimal dependencies — fastapi + uvicorn |
| deployment.yaml | Kubernetes Deployment manifest |
| service.yaml | Kubernetes Service — NodePort exposure |

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| / | GET | System overview and RAG performance results |
| /health | GET | Pod uptime, Python version, deployment info |
| /info | GET | Full performance metrics and portfolio links |
| /docs | GET | Interactive Swagger UI documentation |

---

## Sample Responses

Root endpoint:

    {
        "name": "AI-Powered RAG System",
        "author": "Rohith Kumar Reddipogula",
        "deployment": "Kubernetes",
        "pod": "rag-api-7b456588df-pss62",
        "results": {
            "recall_at_10": "93.0%",
            "mrr": "1.0",
            "optimal_alpha": 0.70
        }
    }

Health endpoint:

    {
        "status": "healthy",
        "uptime_seconds": 3672.4,
        "pod": "rag-api-7b456588df-sgtfk",
        "python": "3.11.0",
        "deployment": "Kubernetes"
    }

---

## How to Deploy Locally

Install prerequisites:

    # Install Docker Desktop
    # https://www.docker.com/products/docker-desktop/

    # Install minikube
    # https://minikube.sigs.k8s.io/docs/start/

    # Install kubectl
    winget install -e --id Kubernetes.kubectl

Start the cluster:

    minikube start --driver=docker

Build and load Docker image:

    docker build -t rag-api:v1 .
    minikube image load rag-api:v1

Deploy to Kubernetes:

    kubectl apply -f deployment.yaml
    kubectl apply -f service.yaml

Check deployment:

    kubectl get pods
    kubectl get deployments
    kubectl get services

Access the API:

    kubectl port-forward service/rag-api-service 8080:80

Then open http://localhost:8080/docs

---

## Key Operations

Check pod status:

    kubectl get pods -o wide

View pod logs:

    kubectl logs -l app=rag-api

Scale replicas:

    kubectl scale deployment rag-api --replicas=3

Rolling update:

    kubectl set image deployment/rag-api rag-api=rag-api:v2
    kubectl rollout status deployment/rag-api

Rollback if update fails:

    kubectl rollout undo deployment/rag-api

Describe pod details:

    kubectl describe pod -l app=rag-api

---

## What I Learned Building This

Rolling updates are not just about running a new version.
They are about guaranteeing that traffic never hits a pod
that is not ready. The readiness probe is what makes this work
— Kubernetes only sends traffic to a pod after the /health
endpoint returns success. Without readiness probes, users
would hit 502 errors during deployments.

Resource limits matter even in development. Without limits,
a memory leak in one pod can kill all other pods on the same
node. Setting requests and limits is not optional in production
— it is the difference between a stable cluster and one that
crashes under load.

The liveness probe and readiness probe serve different purposes.
Liveness restarts a pod stuck in a broken state. Readiness
removes a pod from the load balancer when it cannot serve
traffic. Understanding the difference is a common Kubernetes
interview question.

---

## Dockerfile — Design Decisions

    FROM python:3.11-slim

python:3.11-slim chosen over full python:3.11 to reduce image
size from 1.0GB to 150MB. Smaller images pull faster and use
less storage in production container registries.

    COPY requirements.txt .
    RUN pip install -r requirements.txt
    COPY app.py .

Dependencies installed before copying application code.
Docker layer caching means pip install only reruns when
requirements.txt changes — not every time app.py changes.
This reduces build time from 40 seconds to 2 seconds on
subsequent builds.

---

## Related Projects

| Project | Description | Live |
|---------|-------------|------|
| [Hybrid RAG System](https://github.com/RohithkumarReddipogula/AI-Powered-Rag-System) | BM25 + dense embeddings · 93% Recall@10 · 8.84M passages | [Demo](https://rohith2026-hybrid-rag-demo.hf.space) · [API](https://rohith2026-hybrid-rag-api.hf.space/docs) |
| [AI Agent System](https://github.com/RohithkumarReddipogula/ai-agent-project) | ReAct agent · LangGraph · 3 tools | [Demo](https://rohith2026-ai-agent-react.hf.space) |
| [LLM Fine-Tuning](https://github.com/RohithkumarReddipogula/llm-finetune-project) | QLoRA · TinyLlama 1.1B · HuggingFace Hub | [Model](https://huggingface.co/Rohith2026/nlp-rag-expert) |
| [LLM Evaluation](https://github.com/RohithkumarReddipogula/llm-evaluation-project) | RAGAS · 5 metrics · Streamlit dashboard | [Dashboard](https://rohith2026-llm-evaluation-dashboard.hf.space) |
| [AWS EC2 Deployment](https://github.com/RohithkumarReddipogula/aws-deployment-project) | FastAPI · systemd · production EC2 | [API](http://3.71.32.203:8000/docs) |
| Kubernetes (this) | 2 replicas · rolling updates · health checks | This repo |

---

## Author

Rohith Kumar Reddipogula
MSc Data Science — University of Europe for Applied Sciences, Berlin

LinkedIn: https://linkedin.com/in/rohith-kumar-reddipogula-a6692030b
GitHub: https://github.com/RohithkumarReddipogula
HuggingFace: https://huggingface.co/Rohith2026
Email: rohithkumar336699@gmail.com
