-- drop table if exists energy_usage, temp_daily;

CREATE TABLE energy_usage (
    id INT(11) NOT NULL AUTO_INCREMENT,
    time_stamp DATETIME NOT NULL,
    location VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    energy_usage DECIMAL(10, 2) NOT NULL,
    electric_or_gas bool not null, -- 0 is electric 1 is gas
    PRIMARY KEY (id),
    -- index makes retreival faster so alway retreive by timestamp or location
    INDEX (time_stamp),
    INDEX (location)
);

create table temp_daily (
	id int(11) not null auto_increment primary key,
    time_stamp datetime not null,
    heating_usage DECIMAL(10, 2) NOT NULL,
    cooling_usage DECIMAL(10, 2) NOT NULL,
    index (time_stamp)
);
