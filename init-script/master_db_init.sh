#!/bin/bash

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL

DROP TABLE IF EXISTS bookings CASCADE;
DROP TABLE IF EXISTS tickets CASCADE;
DROP TABLE IF EXISTS airports CASCADE;
DROP TABLE IF EXISTS aircafts CASCADE;
DROP TABLE IF EXISTS seats CASCADE;
DROP TABLE IF EXISTS flights CASCADE;
DROP TABLE IF EXISTS ticket_flights CASCADE;
DROP TABLE IF EXISTS boarding_passes CASCADE;


CREATE Table IF NOT EXISTS bookings
(
    book_ref char(6) PRIMARY KEY,
    book_date timestamptz,
    total_amount numeric(10, 2)
);

CREATE TABLE IF NOT EXISTS tickets
(
    ticket_no char(13) PRIMARY KEY,
    book_ref char(6) REFERENCES bookings(book_ref),
    passenger_id varchar(20),
    passenger_name text,
    contact_data jsonb
);

CREATE TABLE IF NOT EXISTS airports
(
    airport_code char(3) primary key,
    airport_name text,
    city text,
    coordinates_lon float8,
    coordinates_lat float8,
    timezone text
);

CREATE TABLE IF NOT EXISTS aircafts
(
    aircraft_code char(3) primary key,
    model jsonb,
    range integer
);

CREATE TABLE IF NOT EXISTS seats
(
    aircraft_code char(3) references aircafts(aircraft_code),
    seat_no char(4) primary key,
    fare_conditions varchar(10)
);

CREATE TABLE IF NOT EXISTS flights
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

CREATE TABLE IF NOT EXISTS ticket_flights
(
    ticket_no char(13) REFERENCES tickets(ticket_no),
    flight_id serial REFERENCES flights(flight_id),
    fare_conditions numeric (12, 2),
    amount numeric(10, 2),
    PRIMARY KEY (ticket_no, flight_id)
);

CREATE TABLE IF NOT EXISTS boarding_passes
(
    ticket_no char(13),
    flight_id integer,
    boarding_no integer,
    seat_no varchar(4),
    foreign key (ticket_no, flight_id) references ticket_flights(ticket_no, flight_id)
);




insert into aircafts (aircraft_code, model, range)
values ('737', '{}', 800);

insert into aircafts (aircraft_code, model, range)
values ('777', '{}', 200);

insert into aircafts (aircraft_code, model, range)
values ('320', '{}', 0);

insert into aircafts (aircraft_code, model, range)
values ('321', '{}', 0);




insert into airports (airport_code, airport_name, city, coordinates_lon, coordinates_lat, timezone)
values ('SVO', 'Sheremetego', 'MOSCOW', 55.5, 56.6, '+3');

insert into airports (airport_code, airport_name, city, coordinates_lon, coordinates_lat, timezone)
values ('DME', 'DOMODEDOVO', 'MOSCOW', 56.5, 56.6, '+3');

insert into airports (airport_code, airport_name, city, coordinates_lon, coordinates_lat, timezone)
values ('VKO', 'VNUKOVO', 'MOSCOW', 55.5, 54.6, '+3');





insert into bookings (book_ref, book_date, total_amount)
values ('b1', '2024-11-03 11:11:11', 1000);

insert into bookings (book_ref, book_date, total_amount)
values ('b2', '2024-11-03 11:11:11', 100);

insert into bookings (book_ref, book_date, total_amount)
values ('b3', '2024-11-03 11:11:11', 35);

insert into bookings (book_ref, book_date, total_amount)
values ('b4', '2024-11-03 11:11:11', 123);

insert into bookings (book_ref, book_date, total_amount)
values ('b5', '2024-11-03 11:11:11', 321);

insert into bookings (book_ref, book_date, total_amount)
values ('b6', '2024-11-03 11:11:11', 800);






insert into tickets (ticket_no, book_ref, passenger_id, passenger_name, contact_data)
values ('1', 'b1', '1', 'gendalf', '{}');

insert into tickets (ticket_no, book_ref, passenger_id, passenger_name, contact_data)
values ('2', 'b2', '1', 'gendalf', '{}');

insert into tickets (ticket_no, book_ref, passenger_id, passenger_name, contact_data)
values ('3', 'b3', '2', 'saruman', '{}');

insert into tickets (ticket_no, book_ref, passenger_id, passenger_name, contact_data)
values ('4', 'b4', '2', 'saruman', '{}');

insert into tickets (ticket_no, book_ref, passenger_id, passenger_name, contact_data)
values ('5', 'b5', '2', 'saruman', '{}');






insert into seats (aircraft_code, seat_no, fare_conditions)
values ('737', '023A', 'just water');

insert into seats (aircraft_code, seat_no, fare_conditions)
values ('777', '023B', 'just water');

insert into seats (aircraft_code, seat_no, fare_conditions)
values ('320', '023C', 'just water');

insert into seats (aircraft_code, seat_no, fare_conditions)
values ('321', '023D', 'just water');






insert into flights (flight_id, flight_no, scheduled_departure, scheduled_arrival, departure_airport, arrival_airport, status, aircraft_code, actual_departure, actual_arrival)
values (1, 'AER821', '2024-11-03 11:11:11', '2024-11-03 11:11:11', 'DME', 'VKO', 'on air', '737', '2024-11-03 11:11:11', '2024-11-03 11:11:11');

insert into flights (flight_id, flight_no, scheduled_departure, scheduled_arrival, departure_airport, arrival_airport, status, aircraft_code, actual_departure, actual_arrival)
values (2, 'AER822', '2024-11-03 11:11:11', '2024-11-03 11:11:11', 'DME', 'SVO', 'on air', '777', '2024-11-03 11:11:11', '2024-11-03 11:11:11');

insert into flights (flight_id, flight_no, scheduled_departure, scheduled_arrival, departure_airport, arrival_airport, status, aircraft_code, actual_departure, actual_arrival)
values (3, 'AER823', '2024-11-03 11:11:11', '2024-11-03 11:11:11', 'SVO', 'VKO', 'on air', '737', '2024-11-03 11:11:11', '2024-11-03 11:11:11');

insert into flights (flight_id, flight_no, scheduled_departure, scheduled_arrival, departure_airport, arrival_airport, status, aircraft_code, actual_departure, actual_arrival)
values (4, 'AER824', '2024-11-03 11:11:11', '2024-11-03 11:11:11', 'VKO', 'DME', 'on air', '321', '2024-11-03 11:11:11', '2024-11-03 11:11:11');

insert into flights (flight_id, flight_no, scheduled_departure, scheduled_arrival, departure_airport, arrival_airport, status, aircraft_code, actual_departure, actual_arrival)
values (5, 'AER825', '2024-11-03 11:11:11', '2024-11-03 11:11:11', 'DME', 'VKO', 'on air', '320', '2024-11-03 11:11:11', '2024-11-03 11:11:11');






insert into ticket_flights (ticket_no, flight_id, fare_conditions, amount)
values ('1', 1, 5, 1);

insert into ticket_flights (ticket_no, flight_id, fare_conditions, amount)
values ('2', 2, 5, 1);

insert into ticket_flights (ticket_no, flight_id, fare_conditions, amount)
values ('3', 3, 5, 1);

insert into ticket_flights (ticket_no, flight_id, fare_conditions, amount)
values ('4', 4, 5, 1);

insert into ticket_flights (ticket_no, flight_id, fare_conditions, amount)
values ('5', 5, 5, 1);

EOSQL
