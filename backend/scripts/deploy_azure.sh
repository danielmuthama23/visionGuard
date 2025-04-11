#!/bin/bash
# scripts/deploy_azure.sh
set -e

RESOURCE_GROUP="VisionGuard-RG"
LOCATION="eastus"
DEPLOYMENT_NAME="vg-deploy-$(date +%s)"

az login

# Create resource group
az group create --name $RESOURCE_GROUP --location $LOCATION

# Deploy infrastructure
az deployment group create \
  --name $DEPLOYMENT_NAME \
  --resource-group $RESOURCE_GROUP \
  --template-file infrastructure/main.bicep \
  --parameters prefix=vgprod

# Configure environment
echo "AZURE_VISION_ENDPOINT=$(az cognitiveservices account show --name vgprod-vision --query 'properties.endpoint' -o tsv)" >> .env
echo "COSMOS_DB_CONN_STR=$(az cosmosdb keys list --name vgprod-cosmos --type connection-strings --query 'connectionStrings[0].connectionString' -o tsv)" >> .env

echo "Azure deployment completed successfully!"