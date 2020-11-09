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
    (d_devname LIKE 'C%');

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
group by co_ispname;

-- #8
select h_locname, max(speed) 
from 
    (select h_locname, avg(n_speed) as speed, avg(n_price) 
     from network, house 
     where (h_address = n_address)
     group by h_locname
    )SQ;

-- #9
select h_address , count(cpl_conname) 
from contractsperloc, house
where cpl_locname = h_locname
group by h_address;

-- #10
SELECT n_conname
FROM(
SELECT n_conname, MAX(n_price)
FROM network
)SQ;

-- #11
SELECT n_conname
FROM(
SELECT n_conname, MIN(n_price)
FROM network
)SQ;

-- #12
SELECT n_conname
FROM(
    SELECT n_conname, MAX(num)
    FROM(
        SELECT n_conname, COUNT(*) AS num
        FROM network
        GROUP BY n_conname
    )SQ1
)SQ2;

-- #13
SELECT s_locname, AVG(s_speed)
FROM speed
GROUP BY s_locname;

-- #14
SELECT h_locname
FROM(
    SELECT h_locname, MAX(c)
    FROM(
        SELECT h_locname, IFNULL(COUNT(d_devtype), 0) AS c
        FROM 
            devices,
            house
        WHERE (d_address = h_address) AND 
            (d_devtype = 'phone')
        GROUP BY h_locname
    )SQ
)SQ1;