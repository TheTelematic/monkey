
image_name ?= monkey
image_tag ?= latest

install-requirements:
	python -m pip install -r requirements.txt

build:
	docker build -t ${image_name}:${image_tag} .

deploy:
	@extra=$1

	helm upgrade --install --wait monkey kubernetes/chart --set config.OLLAMA_URL=${OLLAMA_URL} ${extra}

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
	helm upgrade --install redis bitnami/redis --set auth.enabled=false --set architecture=standalone --set master.persistence.enabled=false --set slave.persistence.enabled=false --set slave.replicas=0
	helm upgrade --install rabbitmq bitnami/rabbitmq --set auth.password=monkey --set auth.username=monkey
	helm upgrade --install nginx-ingress-controller bitnami/nginx-ingress-controller --set controller.service.type=LoadBalancer

infra-stop:
	helm uninstall redis
	helm uninstall rabbitmq
	helm uninstall nginx-ingress-controller
