-- TYPE YOUR SQL QUERY BELOW

-- PART 1: Create a SQL query that maps out the daily average users before and after the feature change

-- Find julian day number of feature change // 2458271
SELECT MIN(ROUND(JULIANDAY(DATETIME(TIMESTAMP, 'unixepoch', 'localtime')) - 0.5))
AS feature_change_day_number
from card_change_history;

-- Creating table for daily user count

CREATE TABLE IF NOT EXISTS daily_user_count (
    day_number INTEGER PRIMARY KEY,
    user_count INTEGER
);

DELETE FROM daily_user_count; -- to clear previous data

INSERT INTO daily_user_count 
SELECT day_number, COUNT(*) AS user_count FROM 
(
    SELECT ROUND(JULIANDAY(DATETIME(login_timestamp, 'unixepoch', 'localtime')) - 0.5) 
    AS day_number 
    FROM login_history
)
GROUP BY day_number 
ORDER BY 2 DESC;

-- Daily average users before feature change // 14
SELECT ROUND(AVG(user_count) - 0.5)
FROM daily_user_count
WHERE day_number >= 2458271.0;

-- Daily average users after feature change // 4
SELECT ROUND(AVG(user_count) - 0.5)
FROM daily_user_count
WHERE day_number < 2458271.0;


-- PART 2: Create a SQL query that indicates the number of status changes by card

CREATE TABLE IF NOT EXISTS card_status_change_count (
  cardID INTEGER PRIMARY KEY,
  status_change_count INTEGER
);

DELETE FROM card_status_change_count; -- to clear previous data

INSERT INTO card_status_change_count
SELECT cardID, COUNT(*) AS status_change_count FROM 
(
    SELECT cardID
    FROM card_change_history
    WHERE oldStatus is not NULL
)
GROUP BY cardID
ORDER BY 2 DESC;
