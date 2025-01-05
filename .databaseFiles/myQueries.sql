

-- INSERT INTO id7-tusers(username,password) VALUES ("","");

-- SELECT * FROM extension;

CREATE TABLE log_entries_9f3b2 (
    id SERIAL PRIMARY KEY,
    developer VARCHAR(255) NOT NULL,
    project VARCHAR(255) NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    time_worked DECIMAL(5, 2) NOT NULL,
    repo VARCHAR(255) NOT NULL,
    developer_notes TEXT,
    developer_code TEXT NOT NULL
);