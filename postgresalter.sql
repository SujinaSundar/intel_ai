SELECT * from companies
SELECT * FROM news_metadata
SELECT * FROM stock_prices
SELECT current_database();

SELECT COUNT(*)
FROM stock_prices;

SELEC
SELECT DISTINCT trade_date
FROM stock_prices
ORDER BY trade_date DESC;

SELECT
    c.company_name,
    COUNT(s.id) AS records
FROM companies c
LEFT JOIN stock_prices s
ON c.id = s.company_id
GROUP BY c.company_name
ORDER BY c.company_name;

TRUNCATE TABLE stock_prices;

SELECT COUNT(*) FROM stock_prices;

DELETE FROM stock_prices
WHERE company_id = 1;


SELECT DISTINCT trade_date
FROM stock_prices
ORDER BY trade_date;

SELECT * FROM stock_prices


SELECT
    company_id,
    trade_date,
    COUNT(*)
FROM stock_prices
GROUP BY company_id, trade_date
HAVING COUNT(*) > 1;


SELECT MAX(trade_date)
FROM stock_prices;


SELECT COUNT(*)
FROM news_metadata;

SELECT inet_server_addr(), inet_server_port();

SELECT MIN(trade_date), MAX(trade_date)
FROM stock_prices;

SELECT table_schema, table_name
FROM information_schema.tables
WHERE table_name = 'sentiment_scores';

SELECT column_name
FROM information_schema.columns
WHERE table_name = 'sentiment_scores';

DROP TABLE sentiment_scores;

SELECT column_name
FROM information_schema.columns
WHERE table_name = 'news_metadata';

ALTER TABLE news_metadata
ADD COLUMN is_processed BOOLEAN DEFAULT FALSE;

UPDATE news_metadata
SET is_processed = FALSE
WHERE is_processed IS NULL;

ALTER TABLE sentiment_scores
ADD COLUMN news_id INTEGER;

ALTER TABLE sentiment_scores
ADD CONSTRAINT fk_sentiment_news
FOREIGN KEY (news_id)
REFERENCES news_metadata(id);

ALTER TABLE sentiment_scores
ADD CONSTRAINT uq_sentiment_news
UNIQUE(news_id);