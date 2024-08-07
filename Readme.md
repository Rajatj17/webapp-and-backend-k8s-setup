# K8s Setup for a Web App & Backend Server

This repo contains the individual yaml files for creating resources on kubernetes as well as helm chart for doing the same.

## Prerequisite
- K8s cluster running (Use minikube for local development)
- kubectl cli
- helm cli
- docker

## How to deploy your applications on k8s
- Create a separate namespace with name `kube-test`
  - kubectl apply -f deployment-infra/namespace.yaml
  - Or
  - kubectl create namespace kube-test
- Create a service account for this namespace
  - kubectl apply -f deployment-infra/sa/*
- If using minikube, then docker build should be preceded by running following command to export minikube env variables, `eval $(minikube docker-env)`. For more info refer [here](https://stackoverflow.com/questions/52310599/what-does-minikube-docker-env-mean)
  - `docker build -t kube-test-frontend .` -> for frontend 
  - `docker build -t kube-test-backend .` -> for backend 
### Manually
- Frontend
    - kubectl apply -f deployment-infra/frontend/* files
- Backend
  - Change hostPath under volume.yaml inside deployment/backend folder to your local path
  - kubectl apply -f deployment-infra/backend* files
- Run ingress
  - kubectl apply -f ingress.yaml
- Do virtual hosting on your local to make the domain mentioned in the ingress.yaml work
  - Get minikube ip by running `minikube ip`. Let's say it is `192.169.1.5`
  - Edit /etc/hosts file on your local and add the following entry
    - `192.169.1.5  kube-test` - Obviously replace `192.169.1.5` with your minikube ip
- Access your application on
  - http://kube-test/backend
  - http://kube-test/frontend

### Using Helm Charts
You can go and configure your helmchart values based on your preference. A guide explaining all the fields being used at the moment is avaialble at [HELM VALUE GUIDE](Helm.md)
- Create PVC and Volume manually (Will see and add  the support automatic creation with the help of helm chart)
  - kubectl apply -f deployment-infra/backend/volume.yaml
  - kubectl apply -f deployment-infra/backend/pvc.yaml
- Frontend
  - helm upgrade --install kube-test-frontend .deployment -n helm-test
- Backend
  -  helm upgrade --install kube-test-backend .deployment -n helm-test

## Monitoring using Kubernetes Dashboard
You can go through the Readme & provision this dashboard as per your convenience. But if you are in a hurry, just follow the steps below, consider it shortcut
- To add monitoring capabilties to your cluster, you can follow the instruction [here](https://github.com/kubernetes/dashboard?tab=readme-ov-file#installation) to run a monitoring dashboard.
- To run it, follow https://github.com/kubernetes/dashboard/blob/master/docs/user/accessing-dashboard/README.md
- Generate token by following https://github.com/kubernetes/dashboard/blob/master/docs/user/access-control/creating-sample-user.md
- Change your namespace from the topbar to the one you want to monitor