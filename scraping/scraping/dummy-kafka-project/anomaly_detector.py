from base_kafka import KafkaBase, json, logging
import time
from kafka import KafkaConsumer, KafkaProducer

class AnomalyDetector(KafkaBase):
    """Detects anomalies in logs using an LLM."""
    
    def __init__(self, bootstrap_servers=['localhost:9092'], 
                 input_topic='preprocessed-logs', 
                 output_topic='anomaly-results',
                 group_id='anomaly-detector'):
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
        """Create and return a Kafka producer."""
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
    
    def detect_anomaly(self, log_data):
        """
        Use LLM to detect anomalies in the log.
        This is a placeholder - you would implement your LLM call here.
        """
        # PLACEHOLDER: In a real implementation, you would:
        # 1. Call your LLM API with the log data
        # 2. Process the response
        # 3. Return structured anomaly information
        
        # For demonstration, we'll implement a simple rule-based detection
        is_anomaly = False
        explanation = "No anomaly detected"
        
        # Check if the log has already been identified as a potential issue
        if log_data.get('potential_issue', False):
            is_anomaly = True
            explanation = f"Detected potential {log_data.get('issue_type', 'unknown')} issue"
        
        # Check log level
        if log_data.get('log_level') in ['ERROR', 'FATAL', 'WARNING']:
            is_anomaly = True
            explanation = f"{log_data.get('log_level')} level log indicates anomaly"
        
        # Look for error-related keywords in the message
        error_keywords = ['crash', 'exception', 'failure', 'failed', 'error', 'timeout']
        message = log_data.get('message', '').lower()
        if any(keyword in message for keyword in error_keywords):
            is_anomaly = True
            explanation = "Error keywords detected in log message"
        
        return {
            "is_anomaly": is_anomaly,
            "explanation": explanation
        }
    
    def process_message(self, message):
        """Process a preprocessed log message and detect anomalies."""
        try:
            # Extract data from message
            topic = message.topic
            partition = message.partition
            offset = message.offset
            log_data = message.value
            
            self.logger.info(f"Processing preprocessed log from {topic} (partition={partition}, offset={offset})")
            
            # Skip unparsed logs
            if not log_data.get('parsed', False) and 'raw_message' in log_data:
                self.logger.warning(f"Skipping unparsed log: {log_data.get('raw_message')[:50]}...")
                return False
            
            # Detect anomalies
            anomaly_result = self.detect_anomaly(log_data)
            
            # Create result message
            result = {
                "original_log": log_data,
                "anomaly_detection": anomaly_result
            }
            
            # Send result to output topic
            self.send_result(result)
            
            return True
        except Exception as e:
            self.logger.error(f"Error processing message: {e}")
            return False
    
    def send_result(self, result):
        """Send anomaly detection result to output topic."""
        try:
            future = self.producer.send(self.output_topic, result)
            record_metadata = future.get(timeout=10)
            
            self.logger.info(f"Anomaly result sent to {record_metadata.topic}:{record_metadata.partition}:{record_metadata.offset}")
            
            # Log the anomaly if detected
            if result.get('anomaly_detection', {}).get('is_anomaly', False):
                self.logger.warning(f"ANOMALY DETECTED: {result['anomaly_detection']['explanation']}")
            
            return True
        except Exception as e:
            self.logger.error(f"Error sending anomaly result to Kafka: {e}")
            return False
    
    def run(self):
        """Run the anomaly detector."""
        try:
            self.logger.info(f"Anomaly detector started, listening to topic: {self.input_topic}")
            self.logger.info(f"Results will be sent to topic: {self.output_topic}")
            
            # Process messages continuously
            for message in self.consumer:
                self.process_message(message)
                
        except KeyboardInterrupt:
            self.logger.info("Anomaly detector terminated by user")
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
    detector = AnomalyDetector()
    detector.run()