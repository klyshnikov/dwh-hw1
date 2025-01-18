-- Booking
CREATE TABLE hub_booking (
    hub_booking_key CHAR(32) PRIMARY KEY,
    hub_booking_bk CHAR(32),
    hub_load_dts DATE,
    hub_rec_src VARCHAR(12)
);

CREATE TABLE sat_booking (
    hub_booking_key CHAR(32),
    sat_load_dts DATE,
    hash_diff CHAR(32),
    sat_rec_src VARCHAR(12),
    book_date TIMESTAMP WITH TIME ZONE,
    total_amount NUMERIC(10, 2),
    PRIMARY KEY (hub_booking_key, sat_load_dts),
    CONSTRAINT fk_booking FOREIGN KEY (hub_booking_key) REFERENCES hub_booking(hub_booking_key)
);

-- Boarding
CREATE TABLE hub_boarding (
    hub_boarding_key CHAR(32) PRIMARY KEY,
    hub_boarding_bk CHAR(32),
    hub_load_dts DATE,
    hub_rec_src VARCHAR(12)
);

CREATE TABLE sat_boarding (
    hub_boarding_key CHAR(32),
    sat_load_dts DATE,
    hash_diff CHAR(32),
    sat_rec_src VARCHAR(12),
    boarding_no INTEGER,
    seat_no VARCHAR(4),
    PRIMARY KEY (hub_boarding_key, sat_load_dts),
    CONSTRAINT fk_boarding FOREIGN KEY (hub_boarding_key) REFERENCES hub_boarding(hub_boarding_key)
);

-- Ticket
CREATE TABLE hub_ticket (
    hub_ticket_key CHAR(32) PRIMARY KEY,
    hub_ticket_bk CHAR(32),
    hub_load_dts DATE,
    hub_rec_src VARCHAR(12)
);

CREATE TABLE sat_tickets (
    hub_ticket_key CHAR(32),
    sat_load_dts DATE,
    hash_diff CHAR(32),
    sat_rec_src VARCHAR(12),
    ticket_no CHAR(13),
    passenger_id VARCHAR(20),
    passenger_name TEXT,
    contact_data JSONB,
    PRIMARY KEY (hub_ticket_key, sat_load_dts),
    CONSTRAINT fk_tickets FOREIGN KEY (hub_ticket_key) REFERENCES hub_ticket(hub_ticket_key)
);

-- Flight
CREATE TABLE hub_flight (
    hub_flight_key CHAR(32) PRIMARY KEY,
    hub_flight_bk CHAR(32),
    hub_load_dts DATE,
    hub_rec_src VARCHAR(12)
);

CREATE TABLE sat_flight (
    hub_flight_key CHAR(32),
    sat_load_dts DATE,
    hash_diff CHAR(32),
    sat_rec_src VARCHAR(12),
    flight_no CHAR(6),
    scheduled_departure TIMESTAMP WITH TIME ZONE,
    scheduled_arrive TIMESTAMP WITH TIME ZONE,
    status VARCHAR(20),
    actual_departure TIMESTAMP WITH TIME ZONE,
    actual_arrival TIMESTAMP WITH TIME ZONE,
    PRIMARY KEY (hub_flight_key, sat_load_dts),
    CONSTRAINT fk_flight FOREIGN KEY (hub_flight_key) REFERENCES hub_flight(hub_flight_key)
);

-- Airport
CREATE TABLE hub_airport (
    hub_airport_key CHAR(32) PRIMARY KEY,
    hub_airport_bk CHAR(32),
    hub_load_dts DATE,
    hub_rec_src VARCHAR(12)
);

CREATE TABLE sat_airport (
    hub_airport_key CHAR(32),
    sat_load_dts DATE,
    hash_diff CHAR(32),
    sat_rec_src VARCHAR(12),
    airport_code CHAR(3),
    airport_name TEXT,
    city TEXT,
    coordinates_lon DOUBLE PRECISION,
    coordinates_lat DOUBLE PRECISION,
    timezone TEXT,
    PRIMARY KEY (hub_airport_key, sat_load_dts),
    CONSTRAINT fk_airport FOREIGN KEY (hub_airport_key) REFERENCES hub_airport(hub_airport_key)
);

-- Aircraft
CREATE TABLE hub_aircraft (
    hub_aircraft_key CHAR(32) PRIMARY KEY,
    hub_aircraft_bk CHAR(32),
    hub_load_dts DATE,
    hub_rec_src VARCHAR(12)
);

CREATE TABLE sat_aircraft (
    hub_aircraft_key CHAR(32),
    sat_load_dts DATE,
    hash_diff CHAR(32),
    sat_rec_src VARCHAR(12),
    aircraft_code CHAR(3),
    model JSONB,
    range INTEGER,
    PRIMARY KEY (hub_aircraft_key, sat_load_dts),
    CONSTRAINT fk_aircraft FOREIGN KEY (hub_aircraft_key) REFERENCES hub_aircraft(hub_aircraft_key)
);

-- Seat
CREATE TABLE hub_seat (
    hub_seat_key CHAR(32) PRIMARY KEY,
    hub_seat_bk CHAR(32),
    hub_load_dts DATE,
    hub_rec_src VARCHAR(12)
);

CREATE TABLE sat_seat (
    hub_seat_key CHAR(32),
    sat_load_dts DATE,
    hash_diff CHAR(32),
    sat_rec_src VARCHAR(12),
    seat_no VARCHAR(4),
    fare_condition VARCHAR(10),
    PRIMARY KEY (hub_seat_key, sat_load_dts),
    CONSTRAINT fk_seat FOREIGN KEY (hub_seat_key) REFERENCES hub_seat(hub_seat_key)
);

-- Links
CREATE TABLE lnk_ticket_include_booking (
    lnk_ticket_include_booking_key CHAR(32) PRIMARY KEY,
    hub_ticket_key CHAR(32),
    hub_booking_key CHAR(32),
    lnk_load_dts DATE,
    lnk_rec_src VARCHAR(12),
    CONSTRAINT fk_tib_ticket FOREIGN KEY (hub_ticket_key) REFERENCES hub_ticket(hub_ticket_key),
    CONSTRAINT fk_tib_booking FOREIGN KEY (hub_booking_key) REFERENCES hub_booking(hub_booking_key)
);

CREATE TABLE lnk_boarding_matched_with_ticket (
    lnk_boarding_matched_with_ticket CHAR(32) PRIMARY KEY,
    hub_boarding_key CHAR(32),
    hub_ticket_key CHAR(32),
    lnk_load_dts DATE,
    lnk_rec_src VARCHAR(12),
    CONSTRAINT fk_bmt_boarding FOREIGN KEY (hub_boarding_key) REFERENCES hub_boarding(hub_boarding_key),
    CONSTRAINT fk_bmt_ticket FOREIGN KEY (hub_ticket_key) REFERENCES hub_ticket(hub_ticket_key)
);

CREATE TABLE lnk_ticket_is_on_flight (
    lnk_ticket_is_on_flight CHAR(32) PRIMARY KEY,
    hub_ticket_key CHAR(32),
    hub_flight_key CHAR(32),
    lnk_load_dts DATE,
    lnk_rec_src VARCHAR(12),
    fare_conditions NUMERIC(10, 2),
    amount NUMERIC(10, 2),
    CONSTRAINT fk_tif_ticket FOREIGN KEY (hub_ticket_key) REFERENCES hub_ticket(hub_ticket_key),
    CONSTRAINT fk_tif_flight FOREIGN KEY (hub_flight_key) REFERENCES hub_flight(hub_flight_key)
);

CREATE TABLE lnk_flight_departure_airport (
    lnk_flight_departure_airport CHAR(32) PRIMARY KEY,
    hub_flight_key CHAR(32),
    hub_airport_key CHAR(32),
    lnk_load_dts DATE,
    lnk_rec_src VARCHAR(12),
    CONSTRAINT fk_fda_flight FOREIGN KEY (hub_flight_key) REFERENCES hub_flight(hub_flight_key),
    CONSTRAINT fk_fda_airport FOREIGN KEY (hub_airport_key) REFERENCES hub_airport(hub_airport_key)
);

CREATE TABLE lnk_flight_arrive_airport (
    lnk_flight_arrive_airport CHAR(32) PRIMARY KEY,
    hub_flight_key CHAR(32),
    hub_airport_key CHAR(32),
    lnk_load_dts DATE,
    lnk_rec_src VARCHAR(12),
    CONSTRAINT fk_faa_flight FOREIGN KEY (hub_flight_key) REFERENCES hub_flight(hub_flight_key),
    CONSTRAINT fk_faa_airport FOREIGN KEY (hub_airport_key) REFERENCES hub_airport(hub_airport_key)
);

CREATE TABLE lnk_flight_aircraft (
    lnk_flight_aircraft CHAR(32) PRIMARY KEY,
    hub_flight_key CHAR(32),
    hub_aircraft_key CHAR(32),
    lnk_load_dts DATE,
    lnk_rec_src VARCHAR(12),
    CONSTRAINT fk_fa_flight FOREIGN KEY (hub_flight_key) REFERENCES hub_flight(hub_flight_key),
    CONSTRAINT fk_fa_aircraft FOREIGN KEY (hub_aircraft_key) REFERENCES hub_aircraft(hub_aircraft_key)
);

CREATE TABLE lnk_seat_on_aircraft (
    lnk_seat_on_aircraft CHAR(32) PRIMARY KEY,
    hub_seat_key CHAR(32),
    hub_aircraft_key CHAR(32),
    lnk_load_dts DATE,
    lnk_rec_src VARCHAR(12),
    CONSTRAINT fk_soa_seat FOREIGN KEY (hub_seat_key) REFERENCES hub_seat(hub_seat_key),
    CONSTRAINT fk_soa_aircraft FOREIGN KEY (hub_aircraft_key) REFERENCES hub_aircraft(hub_aircraft_key)
);
