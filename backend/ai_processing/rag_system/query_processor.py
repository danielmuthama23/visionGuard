from semantic_kernel import Kernel
from semantic_kernel.planning import ActionPlanner

class RAGQueryProcessor:
    def __init__(self, vector_store, foundry_client):
        self.kernel = Kernel()
        self.planner = ActionPlanner(self.kernel)
        self.vector_store = vector_store
        self.foundry_client = foundry_client
        
        # Register skills
        self.kernel.import_skill(ParkingInsightSkill(vector_store), "ParkingInsights")
        
    async def natural_language_query(self, query):
        # Semantic Kernel planning
        plan = await self.planner.create_plan_async(query)
        
        # Execute plan with Foundry integration
        result = await plan.invoke_async(
            variables={
                "query": query,
                "foundry_data": self._get_foundry_context()
            }
        )
        return result

    def _get_foundry_context(self):
        # Retrieve operational data from AI Foundry
        return self.foundry_client.get_insight_model("parking-analytics-v2")