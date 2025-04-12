# ai_processing/rag_system/skills/parking_insight.py
import threading
from datetime import datetime, timedelta
from semantic_kernel.skill_definition import sk_function, sk_function_context_parameter
from semantic_kernel import ContextVariables
from .foundry_adapter import FoundryDataManager

class ParkingInsightGenerator:
    def __init__(self, cosmos_conn_str, foundry_config):
        self.data_loader = threading.Thread(target=self._load_data, daemon=True)
        self.insight_cache = {}
        self.foundry_mgr = FoundryDataManager(foundry_config)
        self._init_cosmos(cosmos_conn_str)
        self.data_loader.start()

    def _init_cosmos(self, conn_str):
        self.cosmos_client = CosmosClient.from_connection_string(conn_str)
        self.container = self.cosmos_client.get_container_client("ParkingDB", "Insights")

    def _load_data(self):
        while True:
            try:
                raw_data = self.container.query_items(
                    query="SELECT * FROM c WHERE c.timestamp >= @cutoff",
                    parameters=[{"name": "@cutoff", "value": datetime.utcnow() - timedelta(days=7)}]
                )
                self.insight_cache = self._process_raw_data(list(raw_data))
            except Exception as e:
                print(f"Data loading error: {str(e)}")
            time.sleep(3600)  # Refresh hourly

    @sk_function(
        description="Generate parking operation insights",
        input_description="Natural language query about parking patterns"
    )
    @sk_function_context_parameter(name="time_range", description="Analysis time window")
    async def generate_insight(self, context: ContextVariables) -> str:
        query = context["input"]
        time_range = context.get("time_range", "7d")
        
        # Get AI Foundry model
        model = self.foundry_mgr.get_insight_model("parking-analytics-v3")
        
        # Semantic Kernel processing
        return await self._analyze_with_model(query, time_range, model)

    async def _analyze_with_model(self, query, time_range, model):
        # Integrated analysis with cached data and Foundry model
        context_data = {
            "query": query,
            "time_range": time_range,
            "dataset": self.insight_cache
        }
        return model.invoke(context_data)