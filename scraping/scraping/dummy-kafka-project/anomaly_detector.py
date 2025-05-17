from base_kafka import KafkaBase, json, logging
import time
from kafka import KafkaConsumer, KafkaProducer
import ollama

class AnomalyDetector(KafkaBase):
    """Detects anomalies in logs using an LLM via Ollama."""
    
    def __init__(self, bootstrap_servers=['localhost:9092'], 
                 input_topic='preprocessed-logs', 
                 output_topic='anomaly-results',
                 group_id='anomaly-detector',
                 model="llama3.1:8b"):
        super().__init__(bootstrap_servers)
        self.input_topic = input_topic
        self.output_topic = output_topic
        self.group_id = group_id
        self.model = model
        self.consumer = self._create_consumer()
        self.producer = self._create_producer()
    
    def _create_consumer(self):
        """Create and return a Kafka consumer."""
        try:
            from kafka import KafkaConsumer
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
            from kafka import KafkaProducer
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
        Use LLM (Ollama with llama3.1:8b) to detect anomalies in the log.
        """
        try:
            # Construct the prompt for the LLM
            timestamp = log_data.get('timestamp', 'No timestamp')
            message = log_data.get('message', '')
            
            # Add log level if available
            log_level_text = ""
            if 'log_level' in log_data:
                log_level_text = f"Log Level: {log_data['log_level']}\n"
            
            prompt = f"""Analyze this log message and determine if it indicates an anomaly or issue:
                Timestamp: {timestamp}
                {log_level_text}Message: {message}
                
                Is this log message indicating a problem, error, or unusual behavior? 
                Respond with a JSON object with the following fields:
                - is_anomaly: boolean (true if this is an anomaly, false otherwise)
                - explanation: short explanation of why this is or isn't an anomaly

                Your response should be valid JSON with no additional text."""

            self.logger.info(f"Calling LLM for log analysis")
            response = ollama.chat(model=self.model, messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ])
            
            response_text = response.get('message', {}).get('content', '')
            self.logger.info(f"LLM response received, length: {len(response_text)}")
            
            try:
                json_start = response_text.find('{')
                json_end = response_text.rfind('}') + 1
                
                if json_start >= 0 and json_end > json_start:
                    json_part = response_text[json_start:json_end]
                    result = json.loads(json_part)
                else:
                    raise ValueError("No JSON content found in response")
                
                if 'is_anomaly' not in result:
                    result['is_anomaly'] = False
                if 'explanation' not in result:
                    result['explanation'] = "No explanation provided by LLM"
                
                return result
                
            except json.JSONDecodeError as e:
                self.logger.error(f"Failed to parse LLM response as JSON: {e}")
                self.logger.error(f"Raw response: {response_text}")
                return {
                    "is_anomaly": False,
                    "explanation": f"Error parsing LLM response: {str(e)}",
                    "raw_response": response_text
                }
                
        except Exception as e:
            self.logger.error(f"Error in anomaly detection: {e}")
            return {
                "is_anomaly": False,
                "explanation": f"Error in anomaly detection: {str(e)}",
                "error": str(e)
            }
    
    def process_message(self, message):
        """Process a preprocessed log message and detect anomalies."""
        try:
            topic = message.topic
            partition = message.partition
            offset = message.offset
            log_data = message.value
            
            self.logger.info(f"Processing preprocessed log from {topic} (partition={partition}, offset={offset})")
            
            anomaly_result = self.detect_anomaly(log_data)
            
            result = {
                "original_log": log_data,
                "anomaly_detection": anomaly_result,
                "processing_timestamp": time.time()
            }
            
            self.send_result(result)
            
            if anomaly_result.get('is_anomaly', False):
                severity = anomaly_result.get('severity', 'UNKNOWN')
                explanation = anomaly_result.get('explanation', 'No explanation provided')
                self.logger.warning(f"ANOMALY DETECTED ({severity}): {explanation}")
            
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
            return True
        except Exception as e:
            self.logger.error(f"Error sending anomaly result to Kafka: {e}")
            return False
    
    def run(self):
        """Run the anomaly detector."""
        try:
            self.logger.info(f"Anomaly detector started with model {self.model}, listening to topic: {self.input_topic}")
            self.logger.info(f"Results will be sent to topic: {self.output_topic}")
            
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
