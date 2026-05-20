# 🚀 Cloud-Native Django Application: GitOps CI/CD & Monitoring

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)
![ArgoCD](https://img.shields.io/badge/ArgoCD-EF7B4D?style=for-the-badge&logo=argo&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=prometheus&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-F46800?style=for-the-badge&logo=grafana&logoColor=white)

## 📖 Overview
This project demonstrates a complete Cloud-Native workflow for a Django application. It features a fully automated CI/CD pipeline using **GitHub Actions** and **ArgoCD** (GitOps approach), deployed on a **Kubernetes** cluster with comprehensive observability powered by the **Prometheus & Grafana** stack.

## 🏗️ Architecture & Workflow

The pipeline follows a strict GitOps methodology. Changes to the source code trigger the CI pipeline, which builds the image, scans for vulnerabilities, and updates the Kubernetes manifests. ArgoCD automatically detects these changes and syncs the cluster state.

```mermaid
graph TD
    %% Developer Push
    Dev([fas:fa-user Developer]) -->|1. Push Code/Tags| GitHub[fab:fa-github GitHub Repository: main]
    
    %% CI Pipeline
    subgraph CI [Continuous Integration: GitHub Actions]
        GitHub -->|Trigger| Checkout[fas:fa-code-branch Checkout Code]
        Checkout --> BuildImage[fab:fa-docker Build Docker Image]
        BuildImage --> Scan[fas:fa-shield-alt Trivy Vulnerability Scan]
        Scan --> Test[fab:fa-python Run Pytest / Healthcheck]
    end
    
    %% Registry & CD Bridge
    subgraph Registry [Artifacts & Updates]
        Test -->|If Passed| PushImage[fab:fa-docker Push to Docker Hub]
        PushImage --> UpdateManifest[fas:fa-edit Update k8s/deployment.yaml]
        UpdateManifest -->|Commit & Push| GitHub
    end
    
    %% CD Pipeline & Kubernetes
    subgraph CD [Continuous Deployment: Kubernetes]
        GitHub -.->|2. Watch targetRevision| ArgoCD{fas:fa-sync ArgoCD}
        ArgoCD -->|3. Sync Manifests| K8sCluster[fas:fa-server K8s Namespace: my-django-namespace]
        
        K8sCluster --> DjangoDeployment[fas:fa-layer-group Django App Replicas]
        K8sCluster --> DjangoService[fas:fa-network-wired Django ClusterIP Service]
    end

    %% Monitoring
    subgraph Observability [Monitoring: Prometheus & Grafana]
        Prometheus[fas:fa-database Prometheus Instance] -.->|ServiceMonitor: /metrics| DjangoService
        Grafana[fas:fa-chart-line Grafana Dashboard] -->|Query Metrics| Prometheus
    end

✨ Key Features & Functions
1. Continuous Integration (CI) - GitHub Actions
Automated Build & Test: Builds a lightweight Python 3.12-slim Docker image and runs a detached container to verify the application is responding on port 7070.

Security Scanning: Integrates aquasecurity/trivy-action to scan the built Docker image for CRITICAL and HIGH vulnerabilities. Results are exported in SARIF format.

Artifact Management: Automatically logs into Docker Hub and pushes the versioned image (${{ github.sha }}).

Manifest Mutation: Uses sed to automatically inject the new image tag into the Kubernetes deployment.yaml and commits the changes back to the repository using a bot account.

2. Continuous Deployment (CD) - GitOps via ArgoCD
Declarative Setup: ArgoCD Application (argo-app.yaml) points directly to the k8s directory in the repository.

Automated Sync: Configured with selfHeal: true and prune: true to ensure the cluster state strictly matches the Git repository.

Zero-Downtime Deployment: Rolling updates managed natively by Kubernetes via the Deployment controller (running 3 replicas).

3. Monitoring & Observability
Application Metrics: The Django app exposes custom metrics via prometheus_client at the /metrics endpoint.

Dynamic Scraping (Prometheus): Uses a ServiceMonitor (service_monitor.yaml) to dynamically discover the Django service and scrape metrics every 30 seconds with strict RBAC configurations.

Data Visualization (Grafana): Connects to Prometheus as a data source to visualize application performance, request rates, and cluster health through interactive dashboards.

📂 Project Structure

MY-DJANGO-APPLICATION/
├── .github/workflows/
│   └── ci-workflow.yml          # GitHub Actions CI/CD Pipeline
├── app/                         # Django Application Source Code
│   ├── core/
│   ├── manage.py
│   ├── requirements.txt         # Dependencies including Django, prometheus_client
│   └── Dockerfile               # Multi-layer optimized Dockerfile
└── k8s/                         # Kubernetes GitOps Manifests
    ├── deployment.yaml          # App Deployment & Service
    ├── argo-app.yaml            # ArgoCD Application CRD
    └── monitoring/              # Observability Stack Configurations
        ├── expose_prometheus.yaml
        ├── prometheus_instance.yaml
        ├── prometheus_rbac.yaml
        ├── service_monitor.yaml
        └── grafana/             # (Optional) Grafana manifests and dashboards