
image_name ?= monkey
image_tag ?= latest

install-requirements:
	python -m pip install -r requirements.txt

build:
	docker build -t ${image_name}:${image_tag} .

deploy:
	helm upgrade --install monkey kubernetes/chart

undeploy:
	helm uninstall monkey

check-chart:
	helm template --debug monkey kubernetes/chart
	helm lint kubernetes/chart
