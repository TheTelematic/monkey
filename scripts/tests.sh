#!/usr/bin/env bash

set -e
set -o pipefail

image_tag=${image_tag:-latest}

########################################################## LINTING #####################################################
make build image_name=monkey-tests image_tag="${image_tag}" target=tests
docker run --rm monkey-tests:"${image_tag}" pylama --max-line-length 120

########################################################## TESTING #####################################################
namespace=tests
release=monkey-tests

helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update

helm upgrade --install --namespace "${namespace}" --create-namespace --wait \
  redis bitnami/redis -f kubernetes/clusters/local/redis.yaml --version 19.5.0

#helm upgrade --install --namespace "${namespace}" --create-namespace --wait \
#  rabbitmq bitnami/rabbitmq -f kubernetes/clusters/local/rabbitmq.yaml --version 14.3.1
#kubectl exec -n "${namespace}" rabbitmq-0 -c rabbitmq -- rabbitmqctl add_vhost tests

if [ -z "${DEBUG_ENABLED}" ]; then
  helm upgrade --install --namespace "${namespace}" --wait "${release}" kubernetes/tests --set "image.tag=${image_tag}" --set "tests.integration.debug.enabled=false"
else
  echo "Debug mode enabled !!!"
  helm upgrade --install --namespace "${namespace}" --wait "${release}" kubernetes/tests --set "image.tag=${image_tag}" --set "tests.integration.debug.enabled=true"
fi


# Workaround for https://github.com/helm/helm/issues/9098 so I can't use --logs in helm test
#helm test --namespace "${namespace}" "${release}" --timeout 10m --logs
set +e
helm test --namespace "${namespace}" "${release}" --timeout 10m
tests_return_code=$?
pod=$(kubectl get pods -n tests | grep "monkey-tests" | awk '{print $1}')
kubectl logs -n "${namespace}" "${pod}"
kubectl delete pod -n "${namespace}" "${pod}"

exit $tests_return_code
