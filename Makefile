
# Load .env file
ifneq (,$(wildcard ./.env))
	include .env
	export
endif

image_name ?= monkey
image_tag ?= latest

export DOCKER_BUILDKIT = 1

install-requirements:
	python -m pip install -r requirements.txt

build:
	docker build -t ${image_name}:${image_tag} .

deploy:
	helm upgrade --install --wait monkey kubernetes/chart \
		--set config.LLM_ENGINE=openai \
		--set config.OPENAI_API_KEY=${OPENAI_API_KEY} \
		--set ingress.hostname=${NGROK_DOMAIN}

deploy-with-ollama:
	helm upgrade --install monkey kubernetes/chart --set ollama.enabled=true

restart:
	kubectl rollout restart deployment $(shell kubectl get deployments | grep monkey | awk '{print $$1}')

undeploy:
	-helm uninstall monkey

check-chart:
	helm template --debug monkey kubernetes/chart
	helm lint kubernetes/chart

port-forward:
	kubectl port-forward service/monkey-api 8000:80

infra-start:
	helm repo add bitnami https://charts.bitnami.com/bitnami
	helm repo add ngrok https://ngrok.github.io/kubernetes-ingress-controller
	helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
	helm repo update

	helm upgrade --namespace infra --create-namespace --install redis bitnami/redis -f kubernetes/infra/redis.yaml --version 19.5.0
	helm upgrade --namespace infra --create-namespace --install rabbitmq bitnami/rabbitmq -f kubernetes/infra/rabbitmq.yaml --version 14.3.1
	helm upgrade --namespace infra --create-namespace --install ngrok-ingress-controller ngrok/kubernetes-ingress-controller -f kubernetes/infra/ngrok-ingress-controller.yaml --version 0.14.0 \
		--set credentials.apiKey=${NGROK_API_KEY} \
		--set credentials.authtoken=${NGROK_AUTHTOKEN}
	helm upgrade --namespace infra --create-namespace --install kube-prometheus-stack prometheus-community/kube-prometheus-stack -f kubernetes/infra/kube-prometheus-stack.yaml --version 60.0.1

infra-stop:
	helm uninstall --ignore-not-found --namespace infra redis
	helm uninstall --ignore-not-found --namespace infra rabbitmq
	helm uninstall --ignore-not-found --namespace infra ngrok-ingress-controller
	helm uninstall --ignore-not-found --namespace infra kube-prometheus-stack

fix-node-exporter:  # Error: failed to start container "node-exporter": Error response from daemon: path / is mounted on / but it is not a shared or slave mount
	kubectl patch ds -n infra kube-prometheus-stack-prometheus-node-exporter --type "json" -p '[{"op": "remove", "path" : "/spec/template/spec/containers/0/volumeMounts/2/mountPropagation"}]'
