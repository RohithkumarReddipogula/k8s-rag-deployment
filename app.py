"""
RAG System API — Kubernetes Deployment
Author: Rohith Kumar Reddipogula
MSc Data Science — University of Europe for Applied Sciences, Berlin

Production FastAPI application deployed on Kubernetes with:
- 2 pod replicas for high availability
- Rolling update strategy for zero downtime deployments
- Liveness and readiness health probes
- Resource limits per pod

Endpoints:
    GET /        System overview and RAG performance results
    GET /health  Pod uptime, server info — used by Kubernetes probes
    GET /info    Full performance metrics and portfolio links
    GET /docs    Interactive Swagger UI documentation
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import time
import platform
import os

# ─────────────────────────────────────────────────────────────────────────────
# Application setup
# ─────────────────────────────────────────────────────────────────────────────

app = FastAPI(
    title="RAG System API",
    description=(
        "Hybrid BM25 + E5 Retrieval-Augmented Generation System. "
        "Achieves 93% Recall@10 and MRR=1.0 on 8.84M MS MARCO passages. "
        "Deployed on Kubernetes with 2 replicas and rolling update strategy."
    ),
    version="1.0.0",
    contact={
        "name": "Rohith Kumar Reddipogula",
        "email": "rohithkumar336699@gmail.com",
    },
    license_info={
        "name": "MIT",
    },
)

# Allow cross-origin requests from any client
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Track server start time for uptime calculation
start_time = time.time()


# ─────────────────────────────────────────────────────────────────────────────
# Endpoints
# ─────────────────────────────────────────────────────────────────────────────

@app.get("/", tags=["Overview"])
def root():
    """
    System overview — RAG performance results and deployment info.

    Returns the pod name from the HOSTNAME environment variable which
    Kubernetes sets automatically. This shows which of the 2 replicas
    is handling the request — useful for verifying load balancing.
    """
    return {
        "name": "AI-Powered RAG System",
        "version": "1.0.0",
        "author": "Rohith Kumar Reddipogula",
        "thesis": "MSc Data Science — University of Europe for Applied Sciences Berlin 2026",
        "deployment": {
            "platform": "Kubernetes",
            "replicas": 2,
            "strategy": "RollingUpdate",
            "pod": os.environ.get("HOSTNAME", "local"),
        },
        "results": {
            "recall_at_10": "93.0%",
            "mrr": "1.0 — perfect",
            "improvement_over_baseline": "11.4%",
            "optimal_alpha": 0.70,
            "corpus": "8.84M MS MARCO passages",
            "index_size_mb": 4.46,
        },
        "links": {
            "health": "/health",
            "info": "/info",
            "docs": "/docs",
            "rag_demo": "https://rohith2026-hybrid-rag-demo.hf.space",
            "rag_api": "https://rohith2026-hybrid-rag-api.hf.space/docs",
        },
    }


@app.get("/health", tags=["Monitoring"])
def health():
    """
    Health check endpoint — used by Kubernetes liveness and readiness probes.

    Kubernetes calls this endpoint every 30 seconds (liveness) and every
    10 seconds (readiness). If this returns a non-200 status:
    - Liveness failure: Kubernetes restarts the pod
    - Readiness failure: Kubernetes removes the pod from the load balancer

    The pod name shows which replica is responding — demonstrates that
    Kubernetes is routing traffic across both pods.
    """
    uptime = time.time() - start_time
    hours = int(uptime // 3600)
    minutes = int((uptime % 3600) // 60)
    seconds = int(uptime % 60)

    return {
        "status": "healthy",
        "uptime_seconds": round(uptime, 1),
        "uptime_human": f"{hours}h {minutes}m {seconds}s",
        "pod": {
            "name": os.environ.get("HOSTNAME", "local"),
            "node": platform.node(),
            "python": platform.python_version(),
            "os": platform.system(),
        },
        "kubernetes": {
            "replicas": 2,
            "strategy": "RollingUpdate",
            "liveness_probe": "GET /health every 30s",
            "readiness_probe": "GET /health every 10s",
            "resource_limits": {
                "memory": "256Mi",
                "cpu": "500m",
            },
        },
    }


@app.get("/info", tags=["Overview"])
def info():
    """
    Full system information — research context, performance metrics,
    technical stack, and complete portfolio links.
    """
    return {
        "research": {
            "title": (
                "Hybrid Retrieval-Augmented Generation with BM25 "
                "and Dense Embeddings"
            ),
            "institution": "University of Europe for Applied Sciences, Berlin",
            "degree": "MSc Data Science",
            "year": 2026,
        },
        "system": (
            "Hybrid RAG combining BM25 sparse retrieval with Microsoft "
            "E5-base-v2 dense embeddings using FAISS for vector search. "
            "Optimal fusion weight alpha=0.70 validated statistically."
        ),
        "performance": {
            "recall_at_10": "93.0%",
            "mrr": "1.0 — perfect",
            "improvement_over_bm25": "11.4%",
            "statistical_validation": "paired t-test p=0.002",
            "optimal_fusion_weight": "alpha=0.70",
            "corpus_size": "8.84M MS MARCO passages",
            "index_size_compressed_mb": 4.46,
            "index_size_original_gb": 27.0,
            "compression_ratio": "6x via product quantisation",
        },
        "kubernetes_config": {
            "replicas": 2,
            "update_strategy": "RollingUpdate",
            "max_unavailable": 1,
            "max_surge": 1,
            "liveness_probe": "GET /health — restarts broken pods",
            "readiness_probe": "GET /health — removes unready pods from LB",
            "memory_request": "128Mi",
            "memory_limit": "256Mi",
            "cpu_request": "250m",
            "cpu_limit": "500m",
        },
        "stack": [
            "FastAPI",
            "uvicorn",
            "Docker",
            "Kubernetes",
            "minikube",
            "kubectl",
            "Python 3.11",
        ],
        "portfolio": {
            "rag_demo": "https://rohith2026-hybrid-rag-demo.hf.space",
            "rag_api": "https://rohith2026-hybrid-rag-api.hf.space/docs",
            "ai_agent": "https://rohith2026-ai-agent-react.hf.space",
            "llm_evaluation": (
                "https://rohith2026-llm-evaluation-dashboard.hf.space"
            ),
            "aws_api": "http://3.71.32.203:8000/docs",
            "fine_tuned_model": "https://huggingface.co/Rohith2026/nlp-rag-expert",
            "github": "https://github.com/RohithkumarReddipogula",
            "linkedin": (
                "https://linkedin.com/in/rohith-kumar-reddipogula-a6692030b"
            ),
        },
    }
