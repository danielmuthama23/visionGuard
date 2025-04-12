from azure.ai.ml import MLClient
from azure.ai.ml.entities import DataAsset

class FoundryDataManager:
    def __init__(self, credential, subscription_id, resource_group, workspace_name):
        self.ml_client = MLClient(
            credential=credential,
            subscription_id=subscription_id,
            resource_group=resource_group,
            workspace_name=workspace_name
        )
    
    def register_dataset(self, data_path, name):
        data_asset = DataAsset(
            name=name,
            path=data_path,
            type="uri_folder"
        )
        return self.ml_client.data.create_or_update(data_asset)
    
    def get_insight_model(self, model_name):
        return self.ml_client.models.get(name=model_name, label="latest")