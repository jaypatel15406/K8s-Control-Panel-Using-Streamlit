# Docker K8s Test Environment

This directory contains a local Kubernetes testing environment using **K3s** (lightweight Kubernetes) for testing the K8s Control Panel application without connecting to a production cluster.

## 🎯 Purpose

- Test deployment scaling operations (scale up/down)
- Test pod deletion operations
- Validate application functionality in an isolated environment
- No cloud provider account required
- No risk to production resources

## 📦 What's Included

| File | Description |
|------|-------------|
| `docker-compose.yml` | Orchestrates K3s cluster with auto kubeconfig setup |
| `test-namespace.yaml` | Creates isolated test namespace |
| `test-deployment.yaml` | Sample deployments for scaling tests |
| `test-pod.yaml` | Sample pods for deletion tests |

---

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

```bash
cd docker-k8s-test
./setup.sh
```

This script handles everything automatically:
- Starts the cluster
- Waits for it to be ready
- Extracts kubeconfig
- Validates the connection

### Option 2: Manual Steps

#### Step 1: Start the K8s Cluster

```bash
cd docker-k8s-test
docker-compose up -d
```

#### Step 2: Wait for Cluster to Be Ready

```bash
# Monitor cluster startup logs
docker-compose logs -f k8s-cluster

# Wait until you see: "Node k8s-cluster is ready"
# This typically takes 30-60 seconds
# Press Ctrl+C to stop watching
```

#### Step 3: Extract Kubeconfig Automatically

```bash
# This copies and configures kubeconfig automatically
docker-compose run kubeconfig-extractor
```

**That's it!** The kubeconfig is automatically:
- ✅ Extracted from the cluster
- ✅ Copied to `config/k8sconfig.txt`
- ✅ Server URL set to `https://localhost:6443`
- ✅ Certificates embedded inline (no file dependencies)

#### Step 4: Run the Application

```bash
# From project root
python -m streamlit run main_application.py
```

#### Step 5: Stop the Cluster

```bash
docker-compose down
```

To completely remove all data:
```bash
docker-compose down -v
```

---

## 🧪 Pre-Created Test Resources

### Namespace
- `k8s-control-panel-test` - Isolated test namespace

### Deployments
| Name | Initial Replicas | Image | Description |
|------|-----------------|-------|-------------|
| `test-nginx-deployment` | 2 | nginx:1.25-alpine | Web server for scaling tests |
| `test-busybox-deployment` | 1 | busybox:1.36 | Lightweight container for testing |

### Pods (Standalone)
| Name | Image | Purpose |
|------|-------|---------|
| `test-nginx-pod` | nginx:1.25-alpine | Test pod deletion |
| `test-busybox-pod` | busybox:1.36 | Test pod deletion |
| `test-resource-pod` | nginx:1.25-alpine | Test with resource limits |

---

## 📋 Essential kubectl Commands

### Set Up Environment (Optional)

Avoid repeating `--kubeconfig` flag by setting environment variable:

```bash
# macOS/Linux
export KUBECONFIG=/Users/jaypatel/Documents/GitHub\ Repositories/K8s-Control-Panel-Using-Streamlit/config/k8sconfig.txt

# Now run kubectl without the flag
kubectl get namespaces
```

---

### Namespace Operations

```bash
# List all namespaces
kubectl --kubeconfig=../config/k8sconfig.txt get namespaces
kubectl --kubeconfig=../config/k8sconfig.txt get ns

# List all resources in test namespace
kubectl --kubeconfig=../config/k8sconfig.txt get all -n k8s-control-panel-test
```

---

### Pod Operations

```bash
# List all pods in test namespace
kubectl --kubeconfig=../config/k8sconfig.txt get pods -n k8s-control-panel-test
kubectl --kubeconfig=../config/k8sconfig.txt get po -n k8s-control-panel-test

# List pods with more details (IP, node)
kubectl --kubeconfig=../config/k8sconfig.txt get pods -n k8s-control-panel-test -o wide

# Watch pods in real-time
kubectl --kubeconfig=../config/k8sconfig.txt get pods -n k8s-control-panel-test -w

# Describe pod (detailed information)
kubectl --kubeconfig=../config/k8sconfig.txt describe pod test-nginx-pod -n k8s-control-panel-test

# View pod logs
kubectl --kubeconfig=../config/k8sconfig.txt logs test-nginx-pod -n k8s-control-panel-test

# Follow logs (streaming)
kubectl --kubeconfig=../config/k8sconfig.txt logs -f test-nginx-pod -n k8s-control-panel-test

# View last 50 log lines
kubectl --kubeconfig=../config/k8sconfig.txt logs --tail=50 test-nginx-pod -n k8s-control-panel-test

# Execute command inside pod (interactive shell)
kubectl --kubeconfig=../config/k8sconfig.txt exec -it test-nginx-pod -n k8s-control-panel-test -- /bin/sh

# Execute single command inside pod
kubectl --kubeconfig=../config/k8sconfig.txt exec test-nginx-pod -n k8s-control-panel-test -- ls -la

# Test nginx is serving from inside pod
kubectl --kubeconfig=../config/k8sconfig.txt exec test-nginx-pod -n k8s-control-panel-test -- wget -qO- http://localhost:80

# Delete a pod (it will restart if part of deployment)
kubectl --kubeconfig=../config/k8sconfig.txt delete pod test-nginx-pod -n k8s-control-panel-test
```

---

### Deployment Operations

```bash
# List all deployments
kubectl --kubeconfig=../config/k8sconfig.txt get deployments -n k8s-control-panel-test
kubectl --kubeconfig=../config/k8sconfig.txt get deploy -n k8s-control-panel-test

# Describe deployment
kubectl --kubeconfig=../config/k8sconfig.txt describe deployment test-nginx-deployment -n k8s-control-panel-test

# View replica sets
kubectl --kubeconfig=../config/k8sconfig.txt get rs -n k8s-control-panel-test

# Scale deployment UP (increase replicas)
kubectl --kubeconfig=../config/k8sconfig.txt scale deployment test-nginx-deployment --replicas=5 -n k8s-control-panel-test

# Scale deployment DOWN (decrease replicas)
kubectl --kubeconfig=../config/k8sconfig.txt scale deployment test-nginx-deployment --replicas=1 -n k8s-control-panel-test

# Scale to zero
kubectl --kubeconfig=../config/k8sconfig.txt scale deployment test-nginx-deployment --replicas=0 -n k8s-control-panel-test

# Export deployment as YAML
kubectl --kubeconfig=../config/k8sconfig.txt get deployment test-nginx-deployment -n k8s-control-panel-test -o yaml

# Edit deployment (opens in editor)
kubectl --kubeconfig=../config/k8sconfig.txt edit deployment test-nginx-deployment -n k8s-control-panel-test

# Restart deployment (rolling restart)
kubectl --kubeconfig=../config/k8sconfig.txt rollout restart deployment test-nginx-deployment -n k8s-control-panel-test

# Check rollout status
kubectl --kubeconfig=../config/k8sconfig.txt rollout status deployment test-nginx-deployment -n k8s-control-panel-test

# View rollout history
kubectl --kubeconfig=../config/k8sconfig.txt rollout history deployment test-nginx-deployment -n k8s-control-panel-test
```

---

### Service Operations

```bash
# List services
kubectl --kubeconfig=../config/k8sconfig.txt get services -n k8s-control-panel-test
kubectl --kubeconfig=../config/k8sconfig.txt get svc -n k8s-control-panel-test

# Describe service
kubectl --kubeconfig=../config/k8sconfig.txt describe svc test-nginx-deployment -n k8s-control-panel-test
```

---

### Cluster Operations

```bash
# Check cluster info
kubectl --kubeconfig=../config/k8sconfig.txt cluster-info

# Check API server health
kubectl --kubeconfig=../config/k8sconfig.txt get --raw='/healthz'

# View events in namespace (sorted by time)
kubectl --kubeconfig=../config/k8sconfig.txt get events -n k8s-control-panel-test --sort-by='.lastTimestamp'

# Check resource usage (if metrics-server installed)
kubectl --kubeconfig=../config/k8sconfig.txt top pods -n k8s-control-panel-test
kubectl --kubeconfig=../config/k8sconfig.txt top nodes
```

---

### Debugging Commands

```bash
# Get shell access to K3s cluster itself
docker exec -it k8s-control-panel-test-cluster sh

# Then run kubectl directly inside cluster
kubectl get namespaces
kubectl get pods -n k8s-control-panel-test
kubectl describe pod test-nginx-pod -n k8s-control-panel-test

# Exit when done
exit
```

---

## 🎯 Testing the Application

### Step 1: Start the Application

```bash
python -m streamlit run main_application.py
```

### Step 2: Test Deployment Operations

1. Login with your credentials
2. Select **"Deployment Operations"** tab
3. Choose namespace: `k8s-control-panel-test`
4. Select deployments: `test-nginx-deployment`, `test-busybox-deployment`
5. Choose operation:
   - **Scale Up**: Set replicas to 3-5
   - **Scale Down**: Reduce to 0
6. Click **"Perform Deployment Scaling"**
7. Verify with kubectl:
   ```bash
   kubectl --kubeconfig=../config/k8sconfig.txt get deploy -n k8s-control-panel-test
   ```

### Step 3: Test Pod Operations

1. Select **"Pod Operations"** tab
2. Choose namespace: `k8s-control-panel-test`
3. Select pod: `test-nginx-pod`, `test-busybox-pod`
4. Choose operation: **Delete Pod**
5. Click **"Perform Pod Operation"**
6. Verify pod is deleted:
   ```bash
   kubectl --kubeconfig=../config/k8sconfig.txt get pods -n k8s-control-panel-test
   ```

---

## 🔧 Troubleshooting

### Cluster Won't Start

```bash
# Check Docker daemon
docker ps

# Check container logs
docker-compose logs k8s-cluster

# Remove and recreate
docker-compose down -v
docker-compose up -d
```

### Kubeconfig is Empty or Invalid

```bash
# 1. Check if cluster is running
docker-compose ps

# 2. Check cluster logs for errors
docker-compose logs k8s-cluster

# 3. Wait longer and try again (cluster may still be starting)
sleep 30
docker-compose run kubeconfig-extractor

# 4. Verify kubeconfig was created
ls -lh ../config/k8sconfig.txt
head -20 ../config/k8sconfig.txt
```

### Connection Issues

```bash
# Test kubeconfig with kubectl
kubectl --kubeconfig=../config/k8sconfig.txt get namespaces

# If connection fails, verify server URL
grep server ../config/k8sconfig.txt
# Should show: server: https://localhost:6443

# Check if cluster is accessible
curl -k https://localhost:6443/version
```

### Test Resources Not Appearing

```bash
# Check if manifests were loaded
docker-compose exec k8s-cluster kubectl get deployments -n k8s-control-panel-test

# Manually apply if needed
docker-compose exec k8s-cluster kubectl apply -f /var/lib/rancher/k3s/server/manifests/test-deployment.yaml
docker-compose exec k8s-cluster kubectl apply -f /var/lib/rancher/k3s/server/manifests/test-pod.yaml
```

### Permission Denied Errors

```bash
# Ensure Docker is running with proper permissions
# On Linux, add user to docker group:
sudo usermod -aG docker $USER
# Then logout and login again
```

---

## 📊 Resource Usage

| Resource | Approximate Usage |
|----------|------------------|
| CPU | 500MB - 1GB |
| Memory | 1GB - 2GB |
| Disk | 500MB |

---

## 🛑 Important Notes

1. **This is for testing only** - Do not use for production workloads
2. **Data is not persistent** - Cluster state is lost when stopped (unless volumes are preserved)
3. **Single node only** - K3s runs as a single-node cluster
4. **Network isolation** - Cluster runs in isolated Docker network
5. **HTTPS** - The kubeconfig uses `https://localhost:6443` with embedded certificates

---

## 🔄 Reset Test Environment

To reset to initial state:

```bash
# Stop and remove everything
docker-compose down -v

# Restart fresh
docker-compose up -d

# Wait for cluster ready
sleep 45

# Extract kubeconfig again
docker-compose run kubeconfig-extractor
```

---

## 📝 Alternative: Manual Resource Creation

If you prefer to create test resources manually:

```bash
# Get shell access to cluster
docker-compose exec k8s-cluster sh

# Create namespace
kubectl create namespace my-test

# Create deployment
kubectl create deployment my-app --image=nginx:alpine -n my-test

# Scale deployment
kubectl scale deployment my-app --replicas=3 -n my-test

# Create pod
kubectl run my-pod --image=busybox --command -- sleep 3600 -n my-test

# Delete pod
kubectl delete pod my-pod -n my-test
```

---

## 🎓 Learning Resources

- [K3s Documentation](https://docs.k3s.io/)
- [Kubernetes Basics](https://kubernetes.io/docs/tutorials/kubernetes-basics/)
- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
- [Kubernetes Pod Overview](https://kubernetes.io/docs/concepts/workloads/pods/)
- [Kubernetes Deployment Overview](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)

---

## 🚀 Quick Reference Card

```bash
# Start cluster
cd docker-k8s-test && docker-compose up -d

# Extract kubeconfig
docker-compose run kubeconfig-extractor

# Test connection
kubectl --kubeconfig=../config/k8sconfig.txt get ns

# Run application
python -m streamlit run main_application.py

# Stop cluster
docker-compose down -v
```
