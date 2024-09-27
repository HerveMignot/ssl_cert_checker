#!/bin/bash

# Deploying a Cloud Function with a custom runtime

if [ "$#" -lt 2 ]; then
  echo "Usage: $0 PROJECT_ID REGION"
  exit 1
fi
PROJECT_ID=$1
REGION=$2

gcloud functions deploy ssl-cert-checher \
--gen2 \
--runtime=python312 \
--region=${REGION} \
--source=./ssl_cert_checker \
--entry-point=check_endpoints \
--trigger-http \
--allow-unauthenticated \
--project=${PROJECT_ID}

