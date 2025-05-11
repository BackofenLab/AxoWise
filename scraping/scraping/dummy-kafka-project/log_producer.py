import time
import random
import os
from pathlib import Path
from kafka import KafkaProducer
from base_kafka import KafkaBase, json, logging

class LogProducer(KafkaBase):
    """Producer class to read logs and send to Kafka"""
    
    def __init__(self, bootstrap_servers=['localhost:9092'], topic='logs-topic'):
        super().__init__(bootstrap_servers)
        self.topic = topic
        self.producer = self._create_producer()
        
    def _create_producer(self):
        """Create and return a Kafka producer."""
        try:
            # Create producer that serializes messages as JSON
            producer = KafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                acks='all',  # Wait for all replicas
                retries=3,   # Retry on failure
            )
            return producer
        except Exception as e:
            self.logger.error(f"Error creating Kafka producer: {e}")
            raise
    
    def send_message(self, message):
        """Send a message to the Kafka topic."""
        try:
            # Add timestamp to message if not present
            if 'timestamp' not in message:
                message['timestamp'] = time.time()
            
            # Send message to topic
            future = self.producer.send(self.topic, message)
            
            # Block until message is sent (or timeout)
            record_metadata = future.get(timeout=10)
            
            self.logger.info(f"Message sent to {record_metadata.topic}:{record_metadata.partition}:{record_metadata.offset}")
            return True
        except Exception as e:
            self.logger.error(f"Error sending message to Kafka: {e}")
            return False
            
    def get_log_files(self, logs_dir='logs'):
        """
        Recursively find all .log files in the logs directory structure.
        Returns a dictionary mapping log types to lists of log file paths.
        """
        log_files = {}
        logs_path = Path(logs_dir)
        
        if not logs_path.exists():
            self.logger.error(f"Logs directory '{logs_dir}' does not exist")
            return log_files
        
        # Iterate through each subdirectory (which represents a log type)
        for log_type_dir in logs_path.iterdir():
            if log_type_dir.is_dir():
                log_type = log_type_dir.name  # Use directory name as the log type
                log_files[log_type] = []
                
                # Find all .log files in this directory
                for file_path in log_type_dir.glob('*.log'):
                    if file_path.is_file():
                        log_files[log_type].append(file_path)
                        
        return log_files
    
    def read_log_lines(self, log_files):
        """
        Read log lines from all files.
        Returns a dictionary mapping log types to lists of log lines.
        """
        log_lines = {}
        
        for log_type, file_paths in log_files.items():
            log_lines[log_type] = []
            
            for file_path in file_paths:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        # Strip newlines and add non-empty lines
                        log_lines[log_type].extend([line.strip() for line in lines if line.strip()])
                        self.logger.info(f"Read {len(lines)} lines from {file_path}")
                except Exception as e:
                    self.logger.error(f"Error reading log file {file_path}: {e}")
        
        return log_lines
        
    def run(self):
        """Continuously send logs to Kafka."""
        try:
            self.logger.info("Kafka producer created successfully")
            
            # Get all log files by type
            log_files = self.get_log_files()
            if not log_files:
                self.logger.error("No log files found. Exiting.")
                return
            
            # Read all log lines from files
            log_lines_by_type = self.read_log_lines(log_files)
            
            # Track the last position in each log type's list
            log_positions = {log_type: 0 for log_type in log_lines_by_type.keys()}
            
            # Send messages continuously
            count = 0
            while True:
                # Select a random log type that has logs
                available_types = [lt for lt, lines in log_lines_by_type.items() if lines]
                if not available_types:
                    self.logger.error("No log lines available. Exiting.")
                    break
                    
                log_type = random.choice(available_types)
                log_lines = log_lines_by_type[log_type]
                
                # Get next log line in a round-robin fashion
                position = log_positions[log_type] % len(log_lines)
                log_message = log_lines[position]
                log_positions[log_type] += 1
                
                # Create message with metadata
                message = {
                    "type": log_type,
                    "message": log_message,
                    "source": f"file-logs-{count}",
                    "file_source": True
                }
                
                # Send to topic
                self.send_message(message)
                
                # Increment counter
                count += 1
                
                # Wait a bit (random interval between 1-3 seconds)
                delay = random.uniform(1, 3)
                time.sleep(delay)
                
        except KeyboardInterrupt:
            self.logger.info("Producer terminated by user")
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
        finally:
            self.close()
    
    def close(self):
        """Close the producer."""
        if hasattr(self, 'producer'):
            self.producer.close()
            self.logger.info("Producer closed")

if __name__ == "__main__":
    producer = LogProducer()
    producer.run()