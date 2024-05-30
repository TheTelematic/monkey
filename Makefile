
image_name ?= monkey
image_tag ?= latest

export DOCKER_BUILDKIT = 1

install-requirements:
	python -m pip install -r requirements.txt

build:
	docker build -t ${image_name}:${image_tag} .

deploy:
	@extra=$1

	helm upgrade --install --wait monkey kubernetes/chart ${extra}

deploy-with-ollama:
	helm upgrade --install monkey kubernetes/chart --set ollama.enabled=true

restart:
	kubectl rollout restart deployment monkey

undeploy:
	-helm uninstall monkey

check-chart:
	helm template --debug monkey kubernetes/chart
	helm lint kubernetes/chart

port-forward:
	kubectl port-forward service/monkey-api 8000:80

infra-start:
	helm repo add bitnami https://charts.bitnami.com/bitnami
	helm repo update
	helm upgrade --install redis bitnami/redis -f kubernetes/infra/redis.yaml --version 19.5.0
	helm upgrade --install rabbitmq bitnami/rabbitmq -f kubernetes/infra/rabbitmq.yaml --version 14.3.1
	helm upgrade --install nginx-ingress-controller bitnami/nginx-ingress-controller -f kubernetes/infra/nginx-ingress-controller.yaml --version 11.3.0
	helm upgrade --install kube-prometheus bitnami/kube-prometheus -f kubernetes/infra/kube-prometheus.yaml --version 9.2.1
	helm upgrade --install grafana bitnami/grafana -f kubernetes/infra/grafana.yaml --version 11.3.0

infra-stop:
	helm uninstall redis
	helm uninstall rabbitmq
	helm uninstall nginx-ingress-controller
