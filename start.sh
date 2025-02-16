#!/bin/bash

# Останавлваем docker и все контейнеры
sudo docker-compose down

# Удаляем эти папки, т.к там могут быть данные из прошлых запусков
sudo rm -rf data  
sudo rm -rf data-slave

# заходим в master и выполяем инициализацию внутри контейнера
sudo docker-compose up
sleep 10
sudo docker exec -it postgres_master sh /etc/postgresql/init-script/master_init.sh
 
# После того, как скопировали конфиги, рестартнем, чтобы подтянулись
sudo docker-compose restart postgres_master

# Тут выжно скопировать конфиги в data-slave, т.к в реплике должы быть такие-же настройки (иначе все падает)
sudo cp init-script/slave-config/postgresql.auto.conf data-slave
sudo cp init-script/config/pg_hba.conf data-slave
sudo cp init-script/config/postgresql.conf data-slave

# Поднимаем slave
sudo docker-compose restart postgres_slave

# Выолняем скрипт, который в мастере создает таблицы и зполняет их. В реплике все подтягивается.
sudo docker exec -it postgres_master sh /etc/postgresql/init-script/master_db_init.sh

