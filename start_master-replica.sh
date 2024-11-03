#!/bin/bash

sudo docker stop postgres_master
sudo docker stop postgres_slave

sudo docker-compose up -d postgres_master
sudo docker exec -it postgres_master bash

# ========== Execute commands in master=================
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER replicator WITH REPLICATION ENCRYPTED PASSWORD 'my_replicator_password';
    SELECT * FROM pg_create_physical_replication_slot('replication_slot_slave1');
EOSQL

pg_basebackup -D /var/lib/postgresql/data-slave -S replication_slot_slave1 -X stream -P -U replicator -Fp -R

cp /etc/postgresql/init-script/slave-config/* /var/lib/postgresql/data-slave
cp /etc/postgresql/init-script/config/* /var/lib/postgresql/data

exit
# =======================================================
 
sudo docker-compose restart postgres_master


sudo cp init-script/slave-config/postgresql.auto.conf data-slave
sudo cp init-script/config/pg_hba.conf data-slave
sudo cp init-script/config/postgresql.conf data-slave

sudo docker-compose up -d postgres_slave


