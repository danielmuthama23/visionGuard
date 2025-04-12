from semantic_kernel.skill_definition import sk_function
from semantic_kernel import ContextVariables

class ParkingInsightSkill:
    def __init__(self, query_processor):
        self.query_processor = query_processor
        
    @sk_function(
        description="Analyze parking patterns and generate insights",
        input_description="Natural language query about parking operations"
    )
    async def generate_insight(self, context: ContextVariables) -> str:
        query = context["input"]
        result = await self.query_processor.natural_language_query(query)
        return self._format_insight(result)

    def _format_insight(self, raw_data):
        # Convert raw data to narrative insights
        return f"""
        ## Parking Operations Insight
        **Trend**: {raw_data['trend']}
        **Recommendation**: {raw_data['recommendation']}
        **Supporting Data**: {raw_data['stats']}
        """