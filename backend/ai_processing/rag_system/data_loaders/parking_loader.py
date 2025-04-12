import threading
import time
import logging
from queue import Queue
from azure.cosmos import CosmosClient, exceptions
from dotenv import load_dotenv
import os

# Initialize logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ParkingDataLoader(threading.Thread):
    def __init__(self, cosmos_conn_str):
        super().__init__(daemon=True)
        self.queue = Queue()
        self.running = True
        self._validate_connection_string(cosmos_conn_str)
        
        try:
            self.client = CosmosClient.from_connection_string(cosmos_conn_str)
            self.container = self.client.get_container_client("ParkingDB", "VehicleEvents")
            logger.info("Successfully connected to Cosmos DB")
        except exceptions.CosmosHttpResponseError as e:
            logger.error(f"Cosmos DB connection failed: {str(e)}")
            raise

    def _validate_connection_string(self, conn_str):
        """Validate Cosmos DB connection string format"""
        if not conn_str:
            raise ValueError("COSMOS_DB_CONN_STR environment variable is not set")
            
        required_parts = ['AccountEndpoint', 'AccountKey']
        if not all(part in conn_str for part in required_parts):
            raise ValueError(
                "Invalid Cosmos DB connection string format. "
                "Should be: 'AccountEndpoint=https://<uri>;AccountKey=<key>;'"
            )

    def run(self):
        logger.info("Starting data loader thread")
        while self.running:
            try:
                self._process_items()
            except exceptions.CosmosHttpResponseError as e:
                logger.error(f"Cosmos DB operation failed: {str(e)}")
                self._handle_cosmos_error(e)
            except Exception as e:
                logger.error(f"Unexpected error: {str(e)}")
            finally:
                time.sleep(60)

    def _process_items(self):
        """Process unprocessed items from Cosmos DB"""
        items = self.container.query_items(
            query="SELECT * FROM c WHERE c.processed = false",
            enable_cross_partition_query=True
        )
        
        for item in items:
            try:
                self.queue.put(item)
                self._mark_processed(item)
                logger.debug(f"Processed item: {item['id']}")
            except Exception as e:
                logger.error(f"Failed to process item {item['id']}: {str(e)}")

    def _mark_processed(self, item):
        """Mark item as processed with optimistic concurrency"""
        if 'etag' not in item:
            raise ValueError("Item missing etag for concurrency control")
            
        updated_item = {**item, "processed": True}
        self.container.replace_item(item['id'], updated_item, etag=item['etag'])

    def _handle_cosmos_error(self, error):
        """Handle Cosmos DB specific errors"""
        if error.status_code == 401:
            logger.critical("Authentication error - check connection string")
            self.stop()
        elif error.status_code >= 500:
            logger.warning("Server error - retrying in 5 minutes")
            time.sleep(300)
        else:
            logger.error(f"Cosmos DB error: {str(error)}")

    def stop(self):
        """Gracefully stop the data loader"""
        logger.info("Stopping data loader")
        self.running = False
        self.client.close()
        logger.info("Cosmos DB connection closed")

if __name__ == "__main__":
    # Load environment variables first
    load_dotenv()
    conn_str = os.getenv("COSMOS_DB_CONN_STR")
    
    try:
        loader = ParkingDataLoader(conn_str)
        loader.start()
        
        # Keep main thread alive
        while loader.is_alive():
            time.sleep(1)
            
    except (ValueError, exceptions.CosmosHttpResponseError) as e:
        logger.critical(f"Failed to initialize: {str(e)}")
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt")
        loader.stop()