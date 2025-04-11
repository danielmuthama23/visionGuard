# ai_processing/rag_system/vector_store.py
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex, 
    SimpleField,
    SearchFieldDataType,
    VectorSearch,
    HnswAlgorithmConfiguration
)

class VectorStoreManager:
    def __init__(self, endpoint, key):
        self.client = SearchIndexClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(key)
        )

    def create_index(self, index_name):
        vector_config = HnswAlgorithmConfiguration(name="hnsw-config")
        vector_search = VectorSearch(algorithmConfigurations=[vector_config])
        
        fields = [
            SimpleField(name="id", type=SearchFieldDataType.String, key=True),
            SimpleField(name="content", type=SearchFieldDataType.String),
            SearchField(
                name="embedding",
                type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
                searchable=True,
                vectorSearchDimensions=1536,
                vectorSearchConfiguration="hnsw-config"
            )
        ]
        
        index = SearchIndex(
            name=index_name,
            fields=fields,
            vectorSearch=vector_search
        )
        
        self.client.create_index(index)

    def store_document(self, index_name, text, embedding):
        doc = {
            "id": str(uuid.uuid4()),
            "content": text,
            "embedding": embedding
        }
        search_client = self.client.get_search_client(index_name)
        search_client.upload_documents(documents=[doc])