"""
Single DAG for Kafka log analysis pipeline using the main.py script
"""
from datetime import datetime, timedelta
import os
import subprocess
import json
import time
import signal
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

PROJECT_DIR = "/mnt/workspace/momina-work/dummy-kafka-project"  

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
    'start_date': datetime(2025, 5, 18),
    'email_on_failure': False,
}

dag = DAG(
    'kafka_log_analysis_pipeline',
    default_args=default_args,
    description='Run the Kafka log analysis pipeline using main.py',
    schedule=None, 
    catchup=False,
    tags=['kafka', 'logs', 'anomaly-detection'],
)

# start a component and save its PID
def start_component(component_script):
    def _start_component(**kwargs):
        
        # store PIDs in a file for easy cleanup
        pid_dir = os.path.join(PROJECT_DIR, "airflow_pids")
        pid_file = os.path.join(pid_dir, "pids.txt")
        
        os.makedirs(pid_dir, exist_ok=True)
        
        process = subprocess.Popen(
            f"cd {PROJECT_DIR} && python {component_script}",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            preexec_fn=os.setsid  # use process group for easier termination
        )
        
        time.sleep(5)
        
        if process.poll() is not None:
            stderr = process.stderr.read().decode('utf-8')
            raise Exception(f"Failed to start {component_script}: {stderr}")
        
        pgid = os.getpgid(process.pid)
        with open(pid_file, "a") as f:
            f.write(f"{component_script}:{pgid}\n")
        
        print(f"Started {component_script} with PGID {pgid}")
        
        kwargs['ti'].xcom_push(key=f'{component_script}_pgid', value=pgid)
        return pgid
    
    return _start_component

# clean up all processes started by this DAG
def cleanup_processes(**kwargs):
    
    pid_dir = os.path.join(PROJECT_DIR, "airflow_pids")
    pid_file = os.path.join(pid_dir, "pids.txt")
    
    if not os.path.exists(pid_file):
        print("No PID file found, nothing to clean up")
        return
    
    with open(pid_file, "r") as f:
        lines = f.readlines()
    
    for line in lines:
        try:
            script, pgid = line.strip().split(":")
            pgid = int(pgid)
            print(f"Terminating process group {pgid} ({script})")
            os.killpg(pgid, signal.SIGTERM)
        except Exception as e:
            print(f"Error terminating process: {e}")
    
    # remove the PID file after cleanup
    try:
        os.remove(pid_file)
    except Exception as e:
        print(f"Error removing PID file: {e}")
    
    print("Cleanup completed")

# check if Kafka topics have messages
def check_kafka_topics(**kwargs):

    topics_to_check = ["logs-topic", "preprocessed-logs", "anomaly-results"]
    results = {}
    
    for topic in topics_to_check:
        result = subprocess.run(
            f"docker exec kafka kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic {topic} --from-beginning --max-messages 1 --timeout-ms 5000",
            shell=True, capture_output=True, text=True
        )
        
        has_messages = bool(result.stdout.strip())
        results[topic] = has_messages
        print(f"Topic {topic}: {'Has messages' if has_messages else 'No messages'}")
    
    kwargs['ti'].xcom_push(key='topic_check_results', value=results)
    
    return all(results.values())

# generate a summary report
def generate_summary(**kwargs):
    
    summary_dir = os.path.join(PROJECT_DIR, "summaries")
    os.makedirs(summary_dir, exist_ok=True)
    summary_file = os.path.join(summary_dir, f"pipeline_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
    
    with open(summary_file, "w") as f:
        f.write(f"=== KAFKA LOG ANALYSIS PIPELINE SUMMARY ===\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("KAFKA TOPICS:\n")
        
        for topic in ["logs-topic", "preprocessed-logs", "anomaly-results"]:
            try:
                result = subprocess.run(
                    f"kafka-run-class.sh kafka.tools.GetOffsetShell --broker-list localhost:9092 --topic {topic} --time -1",
                    shell=True, capture_output=True, text=True
                )
                
                lines = result.stdout.strip().split('\n')
                total_messages = 0
                
                for line in lines:
                    if ':' in line:
                        parts = line.split(':')
                        if len(parts) >= 3:
                            offset = int(parts[2])
                            total_messages += offset
                
                f.write(f"  - {topic}: {total_messages} messages\n")
            except Exception as e:
                f.write(f"  - {topic}: Error getting message count - {str(e)}\n")
        
        f.write("\n")
        
        f.write("ELASTICSEARCH:\n")
        try:
            # document count for the anomalies index
            result = subprocess.run(
                "curl -s 'http://localhost:9200/anomalies-topic/_count'",
                shell=True, capture_output=True, text=True
            )
            
            try:
                response = json.loads(result.stdout)
                count = response.get('count', 'Unknown')
                f.write(f"  - Total anomalies indexed: {count}\n")
            except:
                f.write(f"  - Error parsing Elasticsearch response\n")
                f.write(f"  - Raw response: {result.stdout[:100]}...\n")
        except Exception as e:
            f.write(f"  - Error querying Elasticsearch: {str(e)}\n")
    
    print(f"Summary report generated: {summary_file}")
    return summary_file


# tasks to start each component
start_producer = PythonOperator(
    task_id='start_log_producer',
    python_callable=start_component('log_producer.py'),
    dag=dag,
)

start_consumer = PythonOperator(
    task_id='start_log_consumer',
    python_callable=start_component('log_consumer.py'),
    dag=dag,
)

start_anomaly_detector = PythonOperator(
    task_id='start_anomaly_detector',
    python_callable=start_component('anomaly_detector.py'),
    dag=dag,
)

start_es_connector = PythonOperator(
    task_id='start_es_connector',
    python_callable=start_component('elasticsearch_connector.py'),
    dag=dag,
)

wait_for_processing = BashOperator(
    task_id='wait_for_processing',
    bash_command='sleep 20',  # wait for processing
    dag=dag,
)

# check if data is flowing through the topics
check_topics = PythonOperator(
    task_id='check_kafka_topics',
    python_callable=check_kafka_topics,
    dag=dag,
)

summary_report = PythonOperator(
    task_id='generate_summary_report',
    python_callable=generate_summary,
    dag=dag,
)

# cleanup all processes
cleanup = PythonOperator(
    task_id='cleanup_processes',
    python_callable=cleanup_processes,
    dag=dag,
)

# Define task dependencies
start_producer >> start_consumer >> start_anomaly_detector >> start_es_connector
start_es_connector >> wait_for_processing >> check_topics >> summary_report >> cleanup