# ai_processing/rag_system/vector_store.py
from azure.search.documents import SearchClient
from datetime import datetime, timedelta

class ParkingVectorStore:
    def __init__(self, search_endpoint, search_key, index_name):
        self.client = SearchClient(
            endpoint=search_endpoint,
            index_name=index_name,
            credential=AzureKeyCredential(search_key))
        
        # Semantic Kernel integration cache
        self.context_cache = {}
        self.last_refresh = datetime.utcnow()

    async def semantic_search(self, query: str, top_k: int = 5):
        # Refresh cache every 15 minutes
        if (datetime.utcnow() - self.last_refresh) > timedelta(minutes=15):
            await self._refresh_context_cache()
            
        results = self.client.search(
            search_text=query,
            vector=self._get_query_vector(query),
            top=top_k
        )
        return [doc["content"] async for doc in results]

    async def _refresh_context_cache(self):
        # Get frequently accessed data
        self.context_cache = {
            "recent": await self._get_time_window_data("24h"),
            "stats": await self._get_system_stats()
        }
        self.last_refresh = datetime.utcnow()

    async def _get_time_window_data(self, time_range: str):
        time_map = {"24h": 1, "7d": 7, "30d": 30}
        days = time_map.get(time_range, 1)
        return self.client.search(
            query=f"timestamp ge {datetime.utcnow() - timedelta(days=days)}"
        )

    async def _get_system_stats(self):
        return {
            "total_vehicles": await self._get_total_count(),
            "peak_hours": await self._get_peak_times()
        }