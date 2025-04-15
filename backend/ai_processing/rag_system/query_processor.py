# ai_processing/rag_system/query_processor.py
import asyncio
from semantic_kernel import Kernel
from semantic_kernel.planning import ActionPlanner
from semantic_kernel.skill_definition import sk_function

class EnhancedQueryProcessor:
    def __init__(self, vector_store, foundry_client):
        self.kernel = Kernel()
        self.planner = ActionPlanner(self.kernel)
        self.vector_store = vector_store
        self.foundry_client = foundry_client
        self._register_skills()

    def _register_skills(self):
        self.kernel.import_skill({
            "vector_search": self.vector_search,
            "foundry_analysis": self.foundry_analysis
        }, "parking_skills")

    @sk_function(
        description="Search parking data vectors",
        input_description="Query embedding vector"
    )
    async def vector_search(self, query: str) -> list:
        return await self.vector_store.semantic_search(query)

    @sk_function(
        description="Analyze data using AI Foundry models",
        input_description="Dataset and analysis parameters"
    )
    async def foundry_analysis(self, context: dict) -> dict:
        model = self.foundry_client.get_insight_model(context["model_name"])
        return model.analyze(context["dataset"])

    async def process_query(self, natural_language_query: str) -> dict:
        plan = await self.planner.create_plan_async(natural_language_query)
        result = await plan.invoke_async()
        return self._format_result(result)

    def _format_result(self, raw_result):
        return {
            "insight": raw_result.get("analysis", ""),
            "stats": raw_result.get("statistics", {}),
            "recommendations": raw_result.get("actions", [])
        }