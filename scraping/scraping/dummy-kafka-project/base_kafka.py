import json
import logging
from kafka import KafkaProducer, KafkaConsumer

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

class KafkaBase:
    """Base class with common Kafka functionality"""
    
    def __init__(self, bootstrap_servers=['localhost:9092']):
        self.bootstrap_servers = bootstrap_servers
        self.logger = logging.getLogger(self.__class__.__name__)