use smartfarm;

CREATE TABLE parm_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sensor_name VARCHAR(20),
    input_time DATETIME,
    temperature INT,
    light INT,
    humidity INT
);

show databases;
