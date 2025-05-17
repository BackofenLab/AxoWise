from datetime import datetime
import re
import time
from base_kafka import KafkaBase, json, logging
from kafka import KafkaProducer, KafkaConsumer

class LogConsumer(KafkaBase):
    """Consumer class to read logs from Kafka and process them"""
    
    def __init__(self, bootstrap_servers=['localhost:9092'], 
                 input_topic='logs-topic', 
                 output_topic='preprocessed-logs',
                 group_id='log-processor'):
        super().__init__(bootstrap_servers)
        self.input_topic = input_topic
        self.output_topic = output_topic
        self.group_id = group_id
        self.consumer = self._create_consumer()
        self.producer = self._create_producer()
    
    def _create_consumer(self):
        """Create and return a Kafka consumer."""
        try:
            consumer = KafkaConsumer(
                self.input_topic,
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
            self.logger.error(f"Error creating Kafka consumer: {e}")
            raise
    
    def _create_producer(self):
        """Create and return a Kafka producer for forwarding preprocessed logs."""
        try:
            producer = KafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                acks='all',
                retries=3
            )
            return producer
        except Exception as e:
            self.logger.error(f"Error creating Kafka producer: {e}")
            raise
 
    def preprocess_log(self, log_message):
        """
        Extract timestamp, log level, and message content from any log type.
        """
        # Common timestamp patterns across different log formats
        timestamp_date_patterns = [
            r'^(\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3})',
            
            r'^(\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})',
            
            r'^(\d{2}/\d{2}/\d{2} \d{2}:\d{2}:\d{2})',
            
            r'^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3})',
            
            r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})'
        ]

        timestamp = None
        for pattern in timestamp_date_patterns:
            match = re.search(pattern, log_message)
            if match:
                timestamp = match.group(1)
                break
        
        # Extract log level - looking for common level indicators
        log_levels = ['INFO', 'WARNING', 'WARN', 'ERROR', 'DEBUG', 'VERBOSE', 'FATAL', 'CRITICAL', 'TRACE', 'NOTICE', 'SEVERE', 'ALERT']

        log_level = None
        for level in log_levels:
            pattern = r'\b' + re.escape(level) + r'\b'
            match = re.search(pattern, log_message, re.IGNORECASE)
            if match:
                log_level = level
                break
        
        # Extract the actual message content - look for patterns like "Component: message"
        message_patterns = [
            r'[^:]+:\s+(.+)$',
            r'(?i)(?:WARNING|WARN|ERROR|VERBOSE|FATAL|CRITICAL|TRACE|NOTICE|SEVERE|ALERT)\s+[^:]+:\s+(.+)$'
        ]

        message = log_message
        for pattern in message_patterns:
            match = re.search(pattern, log_message)
            if match:
                message = match.group(1)
                break
        
        result = {
            "timestamp": timestamp,
            "message": message
        }
        
        if log_level:
            result["log_level"] = log_level
        
        return result


    def send_preprocessed_log(self, preprocessed_log):
        """Send preprocessed log to output topic."""
        try:
            if 'processing_timestamp' not in preprocessed_log:
                preprocessed_log['processing_timestamp'] = time.time()
            
            future = self.producer.send(self.output_topic, preprocessed_log)
            
            record_metadata = future.get(timeout=10)
            
            self.logger.info(f"Preprocessed log sent to {record_metadata.topic}:{record_metadata.partition}:{record_metadata.offset}")
            return True
        except Exception as e:
            self.logger.error(f"Error sending preprocessed log to Kafka: {e}")
            return False
    
    def process_message(self, message):
        """Process a message from Kafka."""
        try:
            topic = message.topic
            partition = message.partition
            offset = message.offset
            value = message.value
            
            self.logger.info(f"Processing message from {topic} (partition={partition}, offset={offset})")
            
            log_message = value.get('message', '')
            
            preprocessed_log = self.preprocess_log(log_message)
            
            preprocessed_log['processing_timestamp'] = time.time()
            
            log_info = f"Preprocessed log: timestamp={preprocessed_log.get('timestamp')}"
            if 'log_level' in preprocessed_log:
                log_info += f", level={preprocessed_log.get('log_level')}"
            self.logger.info(log_info)
            
            self.send_preprocessed_log(preprocessed_log)
            
            return True
        except Exception as e:
            self.logger.error(f"Error processing message: {e}")
            return False
    
    def run(self):
        """Main function - continuously consume logs from Kafka, preprocess, and forward."""
        try:
            self.logger.info(f"Kafka consumer created successfully, listening to topic: {self.input_topic}")
            self.logger.info(f"Preprocessed logs will be sent to topic: {self.output_topic}")
            
            for message in self.consumer:
                self.process_message(message)
                
        except KeyboardInterrupt:
            self.logger.info("Consumer terminated by user")
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
        finally:
            self.close()
    
    def close(self):
        """Close the consumer and producer."""
        if hasattr(self, 'consumer'):
            self.consumer.close()
            self.logger.info("Consumer closed")
        if hasattr(self, 'producer'):
            self.producer.close()
            self.logger.info("Producer closed")

if __name__ == "__main__":
    consumer = LogConsumer()
    consumer.run()
