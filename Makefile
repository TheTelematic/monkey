
image_name ?= monkey
image_tag ?= latest

install-requirements:
	python -m pip install -r requirements.txt

build:
	docker build -t ${image_name}:${image_tag} .

run-local:
	cd src/ && python main.py api

deploy:
	helm upgrade --install monkey kubernetes/chart

deploy-with-ollama:
	helm upgrade --install monkey kubernetes/chart --set ollama.enabled=true

restart:
	kubectl rollout restart deployment monkey

undeploy:
	helm uninstall monkey

check-chart:
	helm template --debug monkey kubernetes/chart
	helm lint kubernetes/chart

port-forward:
	kubectl port-forward service/monkey 8000:80
