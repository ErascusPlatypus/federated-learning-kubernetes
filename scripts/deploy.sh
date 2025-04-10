#!/bin/zsh

kubectl apply -f kubernetes/namespace.yaml
kubectl apply -f kubernetes/server-deployment.yaml
kubectl apply -f kubernetes/client-daemonset.yaml
