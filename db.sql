

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





