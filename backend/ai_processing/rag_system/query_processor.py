# ai_processing/rag_system/query_processor.py
from langchain.chains import RetrievalQA
from langchain.llms import AzureOpenAI
from azure.search.documents import SearchClient

class RAGQueryProcessor:
    def __init__(self, search_endpoint, search_key, index_name):
        self.llm = AzureOpenAI(
            deployment_name="gpt-4",
            temperature=0.1
        )
        
        self.search_client = SearchClient(
            endpoint=search_endpoint,
            index_name=index_name,
            credential=AzureKeyCredential(search_key)
        )

    def create_chain(self):
        return RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self._custom_retriever(),
            return_source_documents=True
        )

    def _custom_retriever(self):
        def _retriever(query):
            vector = self._get_embedding(query)
            results = self.search_client.search(
                search_text="",
                vector=vector,
                top_k=3,
                vector_fields="embedding"
            )
            return [doc["content"] for doc in results]
        return _retriever

    def _get_embedding(self, text):
        # Use Azure OpenAI embeddings
        response = openai.Embedding.create(
            input=text,
            engine="text-embedding-ada-002"
        )
        return response['data'][0]['embedding']