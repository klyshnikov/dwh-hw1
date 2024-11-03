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

sudo docker exec -it postgres_master bash

# ==========================
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE Table bookings
(
    book_ref char(6) PRIMARY KEY,
    book_date timestamptz,
    total_amount numeric(10, 2)
);

CREATE TABLE tickets
(
    ticket_no char(13) PRIMARY KEY,
    book_ref char(6) REFERENCES bookings(book_ref),
    passenger_id varchar(20),
    passenger_name text,
    contact_data jsonb
);

CREATE TABLE airports
(
    airport_code char(3) primary key,
    airport_name text,
    city text,
    coordinates_lon float8,
    coordinates_lat float8,
    timezone text
);

CREATE TABLE aircafts
(
    aircraft_code char(3) primary key,
    model jsonb,
    range integer
);

CREATE TABLE seats
(
    aircraft_code char(3) references aircafts(aircraft_code),
    seat_no char(4) primary key,
    fare_conditions varchar(10)
);

CREATE TABLE flights
(
    flight_id serial PRIMARY KEY,
    flight_no char(6),
    scheduled_departure timestamptz,
    scheduled_arrival timestamptz,
    departure_airport char(3) references airports(airport_code),
    arrival_airport char(3) references airports(airport_code),
    status varchar(20),
    aircraft_code varchar(3) references aircafts(aircraft_code),
    actual_departure timestamptz,
    actual_arrival timestamptz
);

CREATE TABLE ticket_flights
(
    ticket_no char(13) REFERENCES tickets(ticket_no),
    flight_id serial REFERENCES flights(flight_id),
    fare_conditions numeric (12, 2),
    amount numeric(10, 2),
    PRIMARY KEY (ticket_no, flight_id)
);

CREATE TABLE boarding_passes
(
    ticket_no char(13),
    flight_id integer,
    boarding_no integer,
    seat_no varchar(4),
    foreign key (ticket_no, flight_id) references ticket_flights(ticket_no, flight_id)
);

EOSQL

exit

#==================================



