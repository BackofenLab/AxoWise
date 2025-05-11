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
            # Android: "03-17 16:13:38.811"
            r'^(\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3})',
            
            # Linux: "May 1 12:34:56"
            r'^(\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})',
            
            # Spark/HDFS: "20/05/01 12:34:56"
            r'^(\d{2}/\d{2}/\d{2} \d{2}:\d{2}:\d{2})',
            
            # ISO format: "2023-05-01T12:34:56.789"
            r'^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3})',
            
            # Common syslog: "2023-05-01 12:34:56"
            r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})'
        ]

        # Try to extract timestamp using the patterns
        timestamp = None
        for pattern in timestamp_date_patterns:
            match = re.search(pattern, log_message)
            if match:
                timestamp = match.group(1)
                break
        
        # Extract log level - looking for common level indicators
        log_levels = ['INFO', 'WARNING', 'WARN', 'ERROR', 'DEBUG', 'VERBOSE', 'FATAL', 'CRITICAL', 'TRACE', 'NOTICE', 'SEVERE', 'ALERT']

        log_level = None
        # Use a regex pattern that requires word boundaries to avoid partial matches
        for level in log_levels:
            pattern = r'\b' + re.escape(level) + r'\b'
            match = re.search(pattern, log_message, re.IGNORECASE)
            if match:
                # Use the original format from our list, not the matched text
                log_level = level
                break
        
        # Extract the actual message content - look for patterns like "Component: message"
        message_patterns = [
            # Component followed by colon and message
            r'[^:]+:\s+(.+)$',
            
            # Log level followed by component and message
            r'(?i)(?:WARNING|WARN|ERROR|VERBOSE|FATAL|CRITICAL|TRACE|NOTICE|SEVERE|ALERT)\s+[^:]+:\s+(.+)$'
        ]

        # Try to extract message using the patterns
        message = log_message  # Default to full log if no pattern matches
        for pattern in message_patterns:
            match = re.search(pattern, log_message)
            if match:
                message = match.group(1)
                break
        
        # Create the result with timestamp, log level, and message
        result = {
            "timestamp": timestamp,
            "message": message
        }
        
        # Only include log_level if one was found
        if log_level:
            result["log_level"] = log_level
        
        return result


    
    def send_preprocessed_log(self, preprocessed_log):
        """Send preprocessed log to output topic."""
        try:
            # Add timestamp if not present
            if 'processing_timestamp' not in preprocessed_log:
                preprocessed_log['processing_timestamp'] = time.time()
            
            # Send message to output topic
            future = self.producer.send(self.output_topic, preprocessed_log)
            
            # Block until message is sent (or timeout)
            record_metadata = future.get(timeout=10)
            
            self.logger.info(f"Preprocessed log sent to {record_metadata.topic}:{record_metadata.partition}:{record_metadata.offset}")
            return True
        except Exception as e:
            self.logger.error(f"Error sending preprocessed log to Kafka: {e}")
            return False
    
    def process_message(self, message):
        """Process a message from Kafka."""
        try:
            # Extract data from message
            topic = message.topic
            partition = message.partition
            offset = message.offset
            value = message.value
            
            self.logger.info(f"Processing message from {topic} (partition={partition}, offset={offset})")
            
            # Get log message
            log_message = value.get('message', '')
            
            # Preprocess log to extract timestamp, log level, and message
            preprocessed_log = self.preprocess_log(log_message)
            
            # Add processing timestamp
            preprocessed_log['processing_timestamp'] = time.time()
            
            # Log preprocessing result
            log_info = f"Preprocessed log: timestamp={preprocessed_log.get('timestamp')}"
            if 'log_level' in preprocessed_log:
                log_info += f", level={preprocessed_log.get('log_level')}"
            self.logger.info(log_info)
            
            # Send preprocessed log to output topic
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
            
            # Process messages continuously
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
    import time
    consumer = LogConsumer()
    consumer.run()