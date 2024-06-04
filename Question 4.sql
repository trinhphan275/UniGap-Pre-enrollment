-- 1. Count number of unique client order and number of orders by order month.
SELECT 
    DATE_FORMAT(date_order, '%b.%Y') AS order_month,
    COUNT(DISTINCT client_id) AS unique_clients,
    COUNT(*) AS orders_count
FROM orders
GROUP BY DATE_FORMAT(date_order, '%b.%Y')
ORDER BY STR_TO_DATE(order_month, '%b.%Y');



-- 2. Get list of client who have more than 10 orders in this year.
SELECT client_id, COUNT(*) AS orders_count
FROM orders
WHERE YEAR(date_order) = YEAR(CURDATE())
GROUP BY client_id
HAVING COUNT(*) > 10;

-- 3. From the above list of client: get information of first and second last order of client (Order date, good type, and amount)
WITH client_orders AS (
    SELECT 
        client_id, 
        order_id,
        date_order,
        good_type,
        good_amount,
        ROW_NUMBER() OVER (PARTITION BY client_id ORDER BY date_order) AS order_seq,
        ROW_NUMBER() OVER (PARTITION BY client_id ORDER BY date_order DESC) AS order_seq_desc
    FROM order
    WHERE client_id IN (
        SELECT client_id
        FROM orders
        WHERE YEAR(date_order) = YEAR(CURDATE())
        GROUP BY client_id
        HAVING COUNT(*) > 10
    )
)
SELECT client_id, order_id, date_order, good_type, good_amount
FROM client_orders
WHERE order_seq = 1 OR order_seq_desc = 2;

-- 4. Calculate total good amount and Count number of Order which were delivered in Sep.2019
SELECT 
    SUM(o.good_amount) AS total_good_amount,
    COUNT(o.order_id) AS orders_count
FROM orders o
JOIN order_delivery od ON o.order_id = od.order_id
WHERE DATE_FORMAT(od.date_delivery, '%b.%Y') = 'Sep.2019';
