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