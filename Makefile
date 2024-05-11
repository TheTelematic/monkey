
image_name ?= monkey
image_tag ?= latest

build:
	docker build -t ${image_name}:${image_tag} .

deploy:
	helm upgrade --install monkey kubernetes/chart

check-chart:
	helm template --debug monkey kubernetes/chart
	helm lint kubernetes/chart
