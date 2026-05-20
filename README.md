# 🚀 Cloud-Native Django Application: GitOps CI/CD & Monitoring

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)
![ArgoCD](https://img.shields.io/badge/ArgoCD-EF7B4D?style=for-the-badge&logo=argo&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=prometheus&logoColor=white)

## 📖 Overview
This project demonstrates a complete Cloud-Native workflow for a Django application. It features a fully automated CI/CD pipeline using **GitHub Actions** and **ArgoCD** (GitOps approach), deployed on a **Kubernetes** cluster with comprehensive observability powered by the **Prometheus** stack.

## 🏗️ Architecture & Workflow

The pipeline follows a strict GitOps methodology. Changes to the source code trigger the CI pipeline, which builds the image, scans for vulnerabilities, and updates the Kubernetes manifests. ArgoCD automatically detects these changes and syncs the cluster state.

```mermaid
graph TD
    %% Developer Push
    Dev([Developer]) -->|1. Push Code/Tags| GitHub[GitHub Repository: main]
    
    %% CI Pipeline
    subgraph CI [Continuous Integration: GitHub Actions]
        GitHub -->|Trigger| Checkout[Checkout Code]
        Checkout --> BuildImage[Build Docker Image]
        BuildImage --> Scan[Trivy Vulnerability Scan]
        Scan --> Test[Run Pytest / Healthcheck]
    end
    
    %% Registry & CD Bridge
    subgraph Registry [Artifacts & Updates]
        Test -->|If Passed| PushImage[Push to Docker Hub]
        PushImage --> UpdateManifest[Update k8s/deployment.yaml with new Image Tag]
        UpdateManifest -->|Commit & Push| GitHub
    end
    
    %% CD Pipeline & Kubernetes
    subgraph CD [Continuous Deployment & Monitoring: Kubernetes]
        GitHub -.->|2. Watch targetRevision| ArgoCD{ArgoCD}
        ArgoCD -->|3. Sync Manifests| K8sCluster[Kubernetes Namespace: my-django-namespace]
        
        K8sCluster --> DjangoDeployment[Django App Replicas]
        K8sCluster --> DjangoService[Django ClusterIP Service]
        
        %% Monitoring
        Prometheus[Prometheus Instance] -.->|ServiceMonitor: /metrics| DjangoService
    end