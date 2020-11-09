-- #1
SELECT availisp
FROM location
WHERE (l_locname = 'Merced')
EXCEPT
SELECT availisp
FROM location
WHERE (l_locname = 'Tokyo');

-- #2
SELECT sum(devicecount)
FROM house
WHERE (h_locname = 'San Diego');

-- #3
SELECT DISTINCT d_devname
FROM
    devices,
    network
WHERE (n_address = d_address) AND 
    (n_speed > 100);

-- #4
SELECT co_ispname
FROM 
    contractsoff,
    network
WHERE (co_conname = n_conname) AND 
    (n_price < 100) AND 
    (n_speed = 1000);

-- #5
SELECT d_devname
FROM 
    devices,
    house
WHERE (d_address = h_address) AND 
    (d_devtype = 'laptop') AND 
    (d_devname LIKE 'C%')

-- #6
SELECT DISTINCT h_address, cpl_conname, co_ispname, cpl_locname, s_speed
FROM
    contractsoff,
    contractsperloc,
    speed,
    house
WHERE (co_conname = cpl_conname) AND 
    (cpl_locname = s_locname) AND 
    (h_locname = cpl_locname) AND 
    (h_address = (SELECT h_address 
                FROM house LIMIT 1))
ORDER BY h_address;

-- #7
select co_ispname, avg(n_speed), avg(n_price) 
from network, contractsoff
where co_conname = n_conname
group by co_ispname

-- #8
select h_locname, max(speed) 
from 
    (select h_locname, avg(n_speed) as speed, avg(n_price) 
     from network, house 
     where (h_address = n_address)
     group by h_locname
    )SQ

-- #9
select h_address , count(cpl_conname) 
from contractsperloc, house
where cpl_locname = h_locname
group by h_address