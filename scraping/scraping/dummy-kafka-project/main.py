import time
import threading
import logging
from log_producer import LogProducer
from log_consumer import LogConsumer
from anomaly_detector import AnomalyDetector
from elasticsearch_connector import ElasticsearchConnector

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger("kafka-pipeline")

def run_component(component):
    """Run a component in a separate thread."""
    try:
        component.run()
    except Exception as e:
        logger.error(f"Error running {component.__class__.__name__}: {e}")

def main():
    """Run the full Kafka pipeline."""
    logger.info("Starting Kafka log processing pipeline")
    
    # create components
    producer = LogProducer(topic='logs-topic')
    consumer = LogConsumer(input_topic='logs-topic', output_topic='preprocessed-logs')
    detector = AnomalyDetector(input_topic='preprocessed-logs', output_topic='anomaly-results')
    es_connector = ElasticsearchConnector(topic='anomaly-results', index_name='anomalies-topic')

    
    # create threads
    producer_thread = threading.Thread(target=run_component, args=(producer,))
    consumer_thread = threading.Thread(target=run_component, args=(consumer,))
    detector_thread = threading.Thread(target=run_component, args=(detector,))
    es_thread = threading.Thread(target=run_component, args=(es_connector,))
    
    # Set as daemon threads so they exit when the main program exits
    producer_thread.daemon = True
    consumer_thread.daemon = True
    detector_thread.daemon = True
    es_thread.daemon = True
    
    # Start threads
    logger.info("Starting producer thread")
    producer_thread.start()
    
    time.sleep(2)
    
    logger.info("Starting consumer thread")
    consumer_thread.start()
    
    time.sleep(2)
    
    logger.info("Starting anomaly detector thread")
    detector_thread.start()

    time.sleep(2)
    
    logger.info("Starting Elasticsearch connector thread")
    es_thread.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Pipeline terminated by user")

if __name__ == "__main__":
    main()