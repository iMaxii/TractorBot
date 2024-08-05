CREATE TABLE IF NOT EXISTS users (
    user_id BIGINT PRIMARY KEY,
    points INT
);

CREATE TABLE IF NOT EXISTS deaths (
    user_id BIGINT REFERENCES users(user_id),
    death_id TEXT,
    count INT
);
