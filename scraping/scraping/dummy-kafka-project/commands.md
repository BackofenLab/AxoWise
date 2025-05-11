#### to execute container
* Docker exec -it {container_name} bash
  
#### to see list of topics in kafka container
* kafka-topics.sh --bootstrap-server localhost:9092 --list
  
#### to create a new topic
* kafka-topics.sh --bootstrap-server localhost:9092 --topic {topic_name} --create
  
### to check logs of a topic
* kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic {topic_name} --from-beginning
  
#### to create Kibana container (to visualize elasticsearch results)
* docker run -d --name kibana --network {network_name} -p 5601:5601 -e "ELASTICSEARCH_HOSTS=http://elasticsearch:9200" docker.elastic.co/kibana/kibana:9.0.0
  
#### start Kibana
* Run on local terminal to access kibana: ssh -L 5601:localhost:5601 ubuntu@{remote_server}
* See logs: Localhost:5601 > Analytics > Discover > logs-data
