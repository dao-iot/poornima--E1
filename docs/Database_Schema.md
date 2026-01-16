Database Schema – Local Data Logger (SQLite)
Overview

The system uses an SQLite database for local storage of EV sensor data.
The database is designed for time-series data, supports fast queries, and ensures data persistence during network failures.

Database Name
test_data.db

Table: sensor_readings
Purpose

Stores real-time EV sensor readings with timestamp, quality status, and unit information.

Table Structure
CREATE TABLE sensor_readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp INTEGER NOT NULL,
    device_id TEXT NOT NULL,
    sensor_type TEXT NOT NULL,
    value REAL NOT NULL,
    unit TEXT NOT NULL,
    quality TEXT DEFAULT 'GOOD'
);

Column Description
Column Name	Data Type	Description
id	INTEGER	Unique record ID (auto-increment)
timestamp	INTEGER	Unix epoch time in milliseconds
device_id	TEXT	Unique EV device identifier
sensor_type	TEXT	Type of sensor (RPM, voltage, speed, etc.)
value	REAL	Sensor reading value
unit	TEXT	Measurement unit (V, A, °C, km/h)
quality	TEXT	Data quality status (GOOD / WARNING / ERROR)
Indexes

Indexes are used to improve query performance on time-series data.

CREATE INDEX idx_timestamp
ON sensor_readings(timestamp);

CREATE INDEX idx_sensor_type
ON sensor_readings(sensor_type);

Key Features

Supports batch inserts for efficiency

Optimized for time-based queries

Enables fast retrieval of latest readings

Works with circular buffer cleanup logic

Suitable for edge-based IoT systems

Conclusion

This SQLite schema is simple, efficient, and aligned with TASK E1 requirements, making it suitable for reliable local data logging in EV IoT applications.