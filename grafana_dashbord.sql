select count(a)
from (
  select distinct f1.arrival_airport a
  from flights f1
  where f1.actual_arrival > NOW() - interval '1 month'
) tmp1
full outer join (
  select distinct f2.departure_airport d
  from flights f2
  where f2.actual_arrival > NOW() - interval '1 month'
) tmp2 on tmp1.a = tmp2.d;


select a_datepart as flight_day, a+d as active_airports
from (
  select count(distinct f1.arrival_airport) a, date_part('day', f1.actual_arrival) a_datepart
  from flights f1
  where f1.actual_arrival > NOW() - interval '1 month'
  group by date_part('day', f1.actual_arrival)
) tmp1
full outer join (
  select count(distinct f2.departure_airport) d, date_part('day', f2.actual_arrival) d_datepart
  from flights f2
  where f2.actual_arrival > NOW() - interval '1 month'
  group by date_part('day', f2.actual_arrival)
) tmp2 on a_datepart = d_datepart;


select a as airport, a_count+d_count as flight_count
from (
  select count(t1.arrival_airport) a_count, t1.arrival_airport a
  from flights t1
  where t1.actual_arrival > NOW() - interval '1 month'
  group by t1.arrival_airport
) tmp1
full outer join (
  select count(t2.departure_airport) d_count, t2.departure_airport d
  from flights t2
  where t2.actual_arrival > NOW() - interval '1 month'
  group by t2.departure_airport
) tmp2 on d=a;




select a as airport, a_count+d_count as passengers_count
from (select arrival_airport a, count(arrival_airport) a_count from 
(SELECT t.ticket_no, f.actual_arrival, f.arrival_airport FROM tickets t
join ticket_flights tf on t.ticket_no = tf.ticket_no
join flights f on f.flight_id = tf.flight_id) tmp1
group by arrival_airport) firsttable
full outer join
(select departure_airport d, count(departure_airport) d_count from 
(SELECT t1.ticket_no, f1.actual_arrival, f1.departure_airport FROM tickets t1
join ticket_flights tf1 on t1.ticket_no = tf1.ticket_no
join flights f1 on f1.flight_id = tf1.flight_id) tmp1
group by departure_airport) ojtable on ojtable.d = firsttable.a


