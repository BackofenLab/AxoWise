import json
import time
import logging
from kafka import KafkaConsumer
from elasticsearch import Elasticsearch, helpers
import datetime

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger('elasticsearch-connector')

class ElasticsearchConnector:
    """Connector to store Kafka anomaly detection results in Elasticsearch"""
    
    def __init__(self, 
                 bootstrap_servers=['localhost:9092'],
                 topic='anomaly-results',
                 elasticsearch_host='http://localhost:9200',
                 index_name='anomalies-topic',
                 group_id='elasticsearch-consumer'):
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.elasticsearch_host = elasticsearch_host
        self.index_name = index_name
        self.group_id = group_id
        self.consumer = self._create_consumer()
        self.es_client = self._create_es_client()
        self._create_index_if_not_exists()
        
    def _create_consumer(self):
        """Create and return a Kafka consumer."""
        try:
            consumer = KafkaConsumer(
                self.topic,
                bootstrap_servers=self.bootstrap_servers,
                auto_offset_reset='earliest',
                enable_auto_commit=True,
                group_id=self.group_id,
                value_deserializer=lambda x: json.loads(x.decode('utf-8')),
                session_timeout_ms=30000,
                heartbeat_interval_ms=10000
            )
            return consumer
        except Exception as e:
            logger.error(f"Error creating Kafka consumer: {e}")
            raise
    
    def _create_es_client(self):
        """Create and return an Elasticsearch client."""
        try:
            client = Elasticsearch(self.elasticsearch_host)
            logger.info(f"Elasticsearch client created successfully. Connected to: {self.elasticsearch_host}")
            return client
        except Exception as e:
            logger.error(f"Error creating Elasticsearch client: {e}")
            raise
    
    def _create_index_if_not_exists(self):
        """Create the Elasticsearch index if it doesn't exist."""
        try:
            if not self.es_client.indices.exists(index=self.index_name):
                # Define index mapping
                mappings = {
                    "mappings": {
                        "properties": {
                            "timestamp": {"type": "date"},
                            "log_timestamp": {"type": "date"},
                            "message": {"type": "text", "analyzer": "standard"},
                            "is_anomaly": {"type": "boolean"},
                            "explanation": {"type": "text", "analyzer": "standard"},
                        }
                    }
                }
                
                # Create the index
                self.es_client.indices.create(index=self.index_name, body=mappings)
                logger.info(f"Created Elasticsearch index: {self.index_name}")
            else:
                logger.info(f"Elasticsearch index {self.index_name} already exists")
        except Exception as e:
            logger.error(f"Error creating Elasticsearch index: {e}")
            raise
    
    def _prepare_document(self, result):
        """Prepare the document for indexing in Elasticsearch."""
        try:
            # Extract the original log information
            original_log = result.get('original_log', {})
            anomaly_detection = result.get('anomaly_detection', {})
            
            # Parse timestamps
            timestamp = datetime.datetime.now().isoformat()
            
            log_timestamp = None
            if 'timestamp' in original_log and original_log['timestamp']:
                try:
                    # Try to parse the timestamp into a proper date format for Elasticsearch
                    # This depends on the format of your timestamps
                    # Attempt multiple common formats
                    timestamp_formats = [
                        "%Y-%m-%d %H:%M:%S",
                        "%d-%m %H:%M:%S.%f",
                        "%b %d %H:%M:%S",
                        "%y/%m/%d %H:%M:%S",
                        "%Y-%m-%dT%H:%M:%S.%f"
                    ]
                    
                    for fmt in timestamp_formats:
                        try:
                            log_timestamp = datetime.datetime.strptime(
                                original_log['timestamp'], fmt
                            ).isoformat()
                            break
                        except ValueError:
                            continue
                except Exception as e:
                    logger.warning(f"Could not parse timestamp: {original_log.get('timestamp')}, error: {e}")
            
            # Create the document
            document = {
                "timestamp": timestamp,
                "log_timestamp": log_timestamp,
                "message": original_log.get('message', ''),
                "is_anomaly": anomaly_detection.get('is_anomaly', False),
                "explanation": anomaly_detection.get('explanation', ''),
                "raw_log": original_log,
                "raw_result": anomaly_detection
            }
            
            return document
        except Exception as e:
            logger.error(f"Error preparing document: {e}")
            # Return a basic document to prevent pipeline failure
            return {
                "timestamp": datetime.datetime.now().isoformat(),
                "message": "Error preparing document",
                "error": str(e),
                "raw_data": str(result)
            }
    
    def process_message(self, message):
        """Process a message from Kafka and store it in Elasticsearch."""
        try:
            # Extract data from message
            value = message.value
            
            # Prepare the document
            document = self._prepare_document(value)
            
            # Index the document
            response = self.es_client.index(index=self.index_name, document=document)
            
            # Log the response
            logger.info(f"Document indexed in Elasticsearch: id={response['_id']}")
            
            # Log more details if it's an anomaly
            if document.get('is_anomaly', False):
                logger.warning(
                    f"message={document.get('message')[:100]}..."
                )
            
            return True
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return False
    
    def run(self):
        """Run the Elasticsearch connector."""
        try:
            logger.info(f"Elasticsearch connector started, listening to topic: {self.topic}")
            
            # Process messages continuously
            for message in self.consumer:
                self.process_message(message)
                
        except KeyboardInterrupt:
            logger.info("Elasticsearch connector terminated by user")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
        finally:
            self.close()
    
    def close(self):
        """Close the consumer and Elasticsearch client."""
        if hasattr(self, 'consumer'):
            self.consumer.close()
            logger.info("Consumer closed")
        if hasattr(self, 'es_client'):
            self.es_client.close()
            logger.info("Elasticsearch client closed")

if __name__ == "__main__":
    connector = ElasticsearchConnector()
    connector.run()