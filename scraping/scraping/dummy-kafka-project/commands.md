#### to create and run zookeeper container
* docker run -d --name zookeeper --network {network_name} -p 2181:2181 -e ZOOKEEPER_CLIENT_PORT=2181 confluentinc/cp-zookeeper:latest

#### to create and start kafka container
* docker run -d --name kafka --network {network_name} -p 9092:9092 -e KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181 -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092 -e KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1 confluentinc/cp-kafka:latest

#### to create and start elasticsearch container
* docker run -d --name elasticsearch --network {network_name} -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" -e "xpack.security.enabled=false" docker.elastic.co/elasticsearch/elasticsearch:8.10.4

#### to create and run Kibana container (to visualize elasticsearch results)
* docker run -d --name kibana --network {network_name} -p 5601:5601 -e "ELASTICSEARCH_HOSTS=http://elasticsearch:9200" docker.elastic.co/kibana/kibana:9.0.0

#### to execute a container
* Docker exec -it {container_name} bash
  
#### to see list of topics in kafka container
* kafka-topics.sh --bootstrap-server localhost:9092 --list
  
#### to create a new topic
* kafka-topics.sh --bootstrap-server localhost:9092 --topic {topic_name} --create
  
#### to check logs of a topic
* kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic {topic_name} --from-beginning

#### to create network
* docker network create {network_name}
  
#### start Kibana
* Run command on local terminal to access kibana: ssh -L 5601:localhost:5601 ubuntu@{remote_server}
* See logs: Go to localhost:5601 > Analytics > Discover > Dropdown: logs-data
