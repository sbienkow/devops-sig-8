
docker build -t devops-sig-8:v3 .
kind load docker-image devops-sig-8:v3
kubectl apply -f https://raw.githubusercontent.com/stakater/Reloader/master/deployments/kubernetes/reloader.yaml
kubectl apply -f configmap.yml
kubectl apply -f deploy.yml
