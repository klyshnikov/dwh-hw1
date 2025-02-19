#!/bin/bash

sudo docker-compose down

# Удаляем эти папки, т.к там могут быть данные из прошлых запусков
sudo rm -rf data  
sudo rm -rf data-slave

# заходим в master и выполяем инициализацию внутри контейнера
sudo docker-compose up -d postgres_master
sleep 10
sudo docker exec -it postgres_master sh /etc/postgresql/init-script/master_init.sh
 
# После того, как скопировали конфиги, рестартнем, чтобы подтянулись
sudo docker-compose restart postgres_master

# Тут выжно скопировать конфиги в data-slave, т.к в реплике должы быть такие-же настройки (иначе все падает)
sudo cp init-script/slave-config/postgresql.auto.conf data-slave
sudo cp init-script/config/pg_hba.conf data-slave
sudo cp init-script/config/postgresql.conf data-slave

# Поднимаем slave
sudo docker-compose up -d postgres_slave

# Выолняем скрипт, который в мастере создает таблицы и зполняет их. В реплике все подтягивается.
sudo docker exec -it postgres_master sh /etc/postgresql/init-script/master_db_init.sh

sudo docker compose up -d zookeeper1
sudo docker compose up -d broker1
sudo docker compose up -d debezium1
sudo docker compose up -d debezium-ui1
sudo docker compose up -d rest-proxy1

sudo docker compose up -d postgres_dwh
sudo docker compose up --build -d dmp_service

python3 create-config.py
sudo curl -X POST --location "http://localhost:8083/connectors" -H "Content-Type: application/json" -H "Accept: application/json" -d @connector.json

python3 consumer.py

sudo echo hw3




