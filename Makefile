
# Load .env file
ifneq (,$(wildcard ./.env))
	include .env
	export
endif

docker_hub_image_name = thetelematic95/monkey
image_name ?= monkey
image_tag ?= latest

export DOCKER_BUILDKIT = 1

install-requirements:
	python -m pip install -r requirements.txt

build:
	docker build -t ${image_name}:${image_tag} .

local-context:
	kubectl config use-context docker-desktop

deploy-local: local-context
	helm upgrade --install --wait monkey kubernetes/chart \
		--set config.LLM_ENGINE=openai \
		--set config.OPENAI_API_KEY=${OPENAI_API_KEY} \
		--set config.DOMAIN_HOST=localhost \
		--set ingress.enabled=false

deploy-with-ollama: local-context
	helm upgrade --install monkey kubernetes/chart --set ollama.enabled=true

restart: local-context
	kubectl rollout restart deployment $(shell kubectl get deployments | grep monkey | awk '{print $$1}')

undeploy: local-context
	-helm uninstall monkey

check-chart:
	helm template --debug monkey kubernetes/chart
	helm lint kubernetes/chart

port-forward: local-context
	kubectl port-forward service/monkey-api 8000:80

infra-start:
	helm repo add bitnami https://charts.bitnami.com/bitnami
	helm repo add ngrok https://ngrok.github.io/kubernetes-ingress-controller
	helm repo add kedacore https://kedacore.github.io/charts
	helm repo update

	helm upgrade --namespace infra --create-namespace --install redis bitnami/redis -f kubernetes/infra/redis.yaml --version 19.5.0
	helm upgrade --namespace infra --create-namespace --install rabbitmq bitnami/rabbitmq -f kubernetes/infra/rabbitmq.yaml --version 14.3.1
	helm upgrade --namespace infra --create-namespace --install ngrok-ingress-controller ngrok/kubernetes-ingress-controller --version 0.14.0 \
		--set credentials.apiKey=${NGROK_API_KEY} \
		--set credentials.authtoken=${NGROK_AUTHTOKEN}
	helm upgrade --namespace infra --create-namespace --install kube-prometheus bitnami/kube-prometheus -f kubernetes/infra/kube-prometheus.yaml --version 9.2.1
	helm upgrade --namespace infra --create-namespace --install grafana bitnami/grafana -f kubernetes/infra/grafana.yaml --version 11.3.0 \
		--set admin.user=${GRAFANA_USER} \
		--set admin.password=${GRAFANA_PASSWORD}
	helm upgrade --namespace keda --create-namespace --install keda kedacore/keda

infra-stop:
	-helm uninstall --namespace infra redis
	-helm uninstall --namespace infra rabbitmq
	-helm uninstall --namespace infra ngrok-ingress-controller
	-helm uninstall --namespace infra kube-prometheus
	-helm uninstall --namespace infra grafana

publish: build
	docker tag ${image_name}:${image_tag} ${docker_hub_image_name}:${image_tag}
	docker push ${docker_hub_image_name}:${image_tag}

	docker tag ${image_name}:${image_tag} ${docker_hub_image_name}:latest
	docker push ${docker_hub_image_name}:latest

	git tag -a v${image_tag} -m "Release v${image_tag}"
	git push origin v${image_tag}

raspberry-context:
	kubectl config use-context raspberry

deploy-to-raspberry: raspberry-context
	helm upgrade --install --wait monkey kubernetes/chart \
		--set config.LLM_ENGINE=openai \
		--set config.OPENAI_API_KEY=${OPENAI_API_KEY} \
		--set config.DOMAIN_HOST=${NGROK_DOMAIN} \
		-f kubernetes/clusters/raspberry/monkey.yaml
