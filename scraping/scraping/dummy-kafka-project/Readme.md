#### About:
This is a dummy project for Kafka and elasticsearch implementation. In this project, logs are given as input to LLM which detects anomalies in the logs.

#### Step 1:
Download logs from https://github.com/logpai/loghub and put them in a `logs` directory.

#### Step 2: creates all the required containers
Run `docker compose up -d`

#### Step 3: 
Run `python main.py`

#### Step 4:
Go to `localhost:5601` to view logs in Kibana

!!! If `localhost:5601` does not work, run `ssh -L 5601:localhost:5601 ubuntu@{remote-server}` on local terminal

In sidebar, scroll down to $Stack Management$:

![Screenshot 2025-05-11 223520](https://github.com/user-attachments/assets/f1e01312-371c-45c3-897d-c6075d64c578)


Go to $Index Management$:

![Screenshot 2025-05-11 223631](https://github.com/user-attachments/assets/d5cc1a42-e004-4400-9c79-a0c1135ffccf)


Go to $anomalies-topic$:

![Screenshot 2025-05-11 223729](https://github.com/user-attachments/assets/19ee58aa-0ce5-49e3-9f38-99578e87a49b)


Click on $Discover Index$ to view the logs:

![Screenshot 2025-05-11 223745](https://github.com/user-attachments/assets/83e92853-4208-454b-baf3-4fddb5bc48e8)
