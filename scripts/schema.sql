
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS banks;

CREATE TABLE banks (
    bank_id SERIAL PRIMARY KEY,
    bank_name VARCHAR(100) UNIQUE NOT NULL,
    app_name VARCHAR(100)
);

CREATE TABLE reviews (
    review_id VARCHAR(50) PRIMARY KEY,
    bank_id INT REFERENCES banks(bank_id),
    review_text TEXT,
    rating INT,
    review_date DATE,
    sentiment_label VARCHAR(20),
    sentiment_score FLOAT,
    identified_themes TEXT,
    source VARCHAR(50) DEFAULT 'Google Play'
);