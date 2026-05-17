# Deployment Notes

Personal notes from deploying this project — what worked,
what failed, and what I learned.

---

## Environment

- OS: Windows 11 Home
- Docker Desktop: v29.4.3
- minikube: v1.38.1
- kubectl: v1.36.1
- Kubernetes: v1.35.1

---

## Issues Encountered and Fixed

Issue 1 — Docker context conflict on Windows
Docker Desktop on Windows Home uses desktop-linux context
not the default context. Running docker ps failed until
switching context with: docker context use desktop-linux
Fix: Always run docker context use desktop-linux before
any docker or minikube commands on Windows Home.

Issue 2 — Dockerfile saved as Dockerfile.txt by Notepad
Windows Notepad adds .txt extension by default.
Fix: rename Dockerfile.txt Dockerfile in CMD.

Issue 3 — minikube image load taking very long
Loading a 150MB image into minikube takes 5-10 minutes.
This is normal — minikube copies the image into its
internal Docker registry.

Issue 4 — TLS handshake timeout on kubectl
Happens when opening a new CMD window after minikube
was started in a different window. kubectl loses the
cluster context.
Fix: Keep one CMD window open. Always run minikube start
in the same window as kubectl commands.

---

## Successful Deployment Output

    deployment.apps/rag-api created
    service/rag-api-service created

    NAME                          READY   STATUS    RESTARTS
    rag-api-7b456588df-pss62      1/1     Running   0
    rag-api-7b456588df-sgtfk      1/1     Running   0

    http://127.0.0.1:59386

Both pods running. API accessible at the minikube URL.

---

## Key Lessons

1. Context matters in Docker on Windows
   docker context use desktop-linux before everything

2. One CMD window rule
   Never open a new CMD window mid-deployment
   kubectl loses connection to the cluster

3. Resource limits are not optional
   Without limits a memory leak kills the whole node
   Always set requests AND limits

4. Liveness vs readiness probes are different
   Liveness restarts broken pods
   Readiness removes pods from load balancer
   Both are needed in production
