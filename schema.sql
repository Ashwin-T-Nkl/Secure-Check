
CREATE TABLE police_stops (
    stop_id INT AUTO_INCREMENT PRIMARY KEY,
    stop_date DATE,
    stop_time TIME,
    country_name VARCHAR(50),
    driver_gender VARCHAR(10),
    driver_age INT,
    driver_race VARCHAR(30),
    violation VARCHAR(100),
    search_conducted VARCHAR(10),
    search_type VARCHAR(50),
    stop_outcome VARCHAR(50),
    is_arrested VARCHAR(10),
    stop_duration VARCHAR(20),
    drugs_related_stop VARCHAR(10)
);


