# ai_processing/rag_system/insight_generator.py
import threading
from semantic_kernel import ContextVariables
from semantic_kernel.skill_definition import sk_function

class ParkingInsightGenerator:
    def __init__(self, query_processor, vector_store):
        self.query_processor = query_processor
        self.vector_store = vector_store
        self.insight_thread = threading.Thread(target=self._generate_insights)
        self.running = True
        self.insight_thread.start()

    def stop(self):
        self.running = False
        self.insight_thread.join()

    def _generate_insights(self):
        while self.running:
            try:
                # Generate hourly insights
                data = self.vector_store.context_cache
                context = ContextVariables()
                context["input"] = "Analyze recent parking trends"
                insights = asyncio.run(
                    self.query_processor.process_query(context)
                )
                self._store_insights(insights)
                self._update_foundry_models(insights)
            except Exception as e:
                print(f"Insight generation error: {str(e)}")
            time.sleep(3600)  # Hourly analysis

    @sk_function(
        description="Identify peak parking hours",
        input_description="Time range for analysis"
    )
    async def identify_peaks(self, time_range: str) -> dict:
        context = ContextVariables()
        context["input"] = f"Show peak hours from last {time_range}"
        return await self.query_processor.process_query(context)

    def _store_insights(self, insights):
        # Store in Cosmos DB
        doc = {
            "id": f"insight_{datetime.utcnow().isoformat()}",
            "insights": insights,
            "timestamp": datetime.utcnow()
        }
        self.vector_store.client.upsert_documents(documents=[doc])

    def _update_foundry_models(self, insights):
        # Update AI Foundry models with new data
        dataset = self.foundry_client.register_dataset({
            "name": "parking_insights",
            "data": insights
        })
        print(f"Updated AI Foundry dataset: {dataset.id}")