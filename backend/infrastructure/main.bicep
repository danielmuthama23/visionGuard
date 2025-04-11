// infrastructure/main.bicep
param location string = 'eastus'
param prefix string = 'visionguard'

resource cognitiveServices 'Microsoft.CognitiveServices/accounts@2023-05-01' = {
  name: '${prefix}-vision'
  location: location
  sku: {
    name: 'S1'
  }
  kind: 'ComputerVision'
}

resource cosmosDB 'Microsoft.DocumentDB/databaseAccounts@2023-04-15' = {
  name: '${prefix}-cosmos'
  location: location
  properties: {
    databaseAccountOfferType: 'Standard'
    locations: [
      {
        locationName: location
        failoverPriority: 0
      }
    ]
  }
}

resource iotHub 'Microsoft.Devices/IotHubs@2022-04-30-preview' = {
  name: '${prefix}-iothub'
  location: location
  sku: {
    name: 'S1'
    capacity: 1
  }
}

resource aks 'Microsoft.ContainerService/managedClusters@2023-02-02-preview' = {
  name: '${prefix}-aks'
  location: location
  properties: {
    kubernetesVersion: '1.24'
    dnsPrefix: '${prefix}-aks'
    agentPoolProfiles: [{
      name: 'default'
      count: 3
      vmSize: 'Standard_DS2_v2'
    }]
  }
}

resource aiSearch 'Microsoft.Search/searchServices@2023-11-01' = {
  name: '${prefix}-search'
  location: location
  sku: {
    name: 'basic'
  }
}