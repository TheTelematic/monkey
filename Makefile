docker_hub_image_name = thetelematic95/monkey
image_name ?= monkey
image_tag ?= latest
target ?= app

export DOCKER_BUILDKIT = 1

install-requirements:
	python -m pip install -r requirements.txt

build:
	docker build -t ${image_name}:${image_tag} --target monkey_${target} . --build-arg BUILD_TIMESTAMP=$(shell date -u +'%Y-%m-%dT%H:%M:%SZ')

local-context:
	kubectl config use-context docker-desktop

local-secret: local-context
	kubectl create secret generic monkey --from-env-file=local.env \
 		--save-config \
		--dry-run=client \
		-o yaml | \
		kubectl apply -f -
	kubectl create secret generic monkey --from-env-file=local.env \
 		--save-config \
		--dry-run=client \
		-o yaml | \
		kubectl apply -n infra -f -

deploy-local: local-context local-secret
	helm upgrade --install --wait monkey kubernetes/chart -f kubernetes/clusters/local/monkey.yaml
	helm test monkey

restart: local-context
	kubectl rollout restart deployment $(shell kubectl get deployments | grep monkey | awk '{print $$1}')

undeploy: local-context
	-helm uninstall monkey

check-chart:
	helm template --debug monkey kubernetes/chart
	helm lint kubernetes/chart

port-forward: local-context
	kubectl port-forward service/monkey-api 8000:80

infra-start-local: local-context
	helm repo add bitnami https://charts.bitnami.com/bitnami
	helm repo add kedacore https://kedacore.github.io/charts
	helm repo update

	helm upgrade --install --namespace infra --create-namespace keda kedacore/keda  --version 2.14.2
	helm upgrade --install --namespace infra --create-namespace redis bitnami/redis -f kubernetes/clusters/local/redis.yaml --version 19.5.0
	helm upgrade --install --namespace infra --create-namespace rabbitmq bitnami/rabbitmq -f kubernetes/clusters/local/rabbitmq.yaml --version 14.3.1
	helm upgrade --install --namespace infra --create-namespace nginx-ingress-controller bitnami/nginx-ingress-controller -f kubernetes/clusters/local/nginx-ingress-controller.yaml --version 11.3.0
	helm upgrade --install --namespace infra --create-namespace kube-prometheus bitnami/kube-prometheus -f kubernetes/clusters/local/kube-prometheus.yaml --version 9.2.1
	helm upgrade --install --namespace infra --create-namespace grafana bitnami/grafana -f kubernetes/clusters/local/grafana.yaml --version 11.3.0

infra-stop-local: local-context
	-helm uninstall --namespace infra keda
	-helm uninstall --namespace infra redis
	-helm uninstall --namespace infra rabbitmq
	-helm uninstall --namespace infra nginx-ingress-controller
	-helm uninstall --namespace infra kube-prometheus
	-helm uninstall --namespace infra grafana

tests: local-context
	./scripts/tests.sh

debug-tests: local-context
	kubectl debug --profile general -n tests $(shell kubectl get pods -n tests | grep "monkey-tests" | awk '{print $$1}' ) -it --copy-to=debugger --container=monkey-tests -- sh
	kubectl delete pod -n tests debugger

publish: build tests
	docker tag ${image_name}:${image_tag} ${docker_hub_image_name}:${image_tag}
	docker push ${docker_hub_image_name}:${image_tag}

	docker tag ${image_name}:${image_tag} ${docker_hub_image_name}:latest
	docker push ${docker_hub_image_name}:latest

	git tag -s -a v${image_tag} -m "Release v${image_tag}"
	git tag -v v${image_tag}
	git push origin v${image_tag}

raspberry-context:
	kubectl config use-context raspberry

raspberry-secret: raspberry-context
	kubectl create secret generic monkey --from-env-file=raspberry.env \
 		--save-config \
		--dry-run=client \
		-o yaml | \
		kubectl apply -f -
	kubectl create secret generic monkey --from-env-file=raspberry.env \
 		--save-config \
		--dry-run=client \
		-o yaml | \
		kubectl apply -n infra -f -
	kubectl create secret generic ngrok-ingress-controller-credentials --from-env-file=ngrok.env \
 		--save-config \
		--dry-run=client \
		-o yaml | \
		kubectl apply -n infra -f -

init-flux:
	flux bootstrap git \
        --url=ssh://git@github.com/TheTelematic/monkey.git \
        --branch=main \
        --path=kubernetes/clusters/raspberry \
        --private-key-file=.ssh/id_ed25519 \
        --components-extra=image-reflector-controller,image-automation-controller
