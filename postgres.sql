SELECT * from companies
SELECT * FROM news_metadata
SELECT * FROM stock_prices
SELECT current_database();

SELECT COUNT(*)
FROM stock_prices;

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

SELECT inet_server_addr(),
       inet_server_port(),
       current_database();

SELECT * FROM document_chunks
SELECT *
FROM sentiment_scores
LIMIT 10;

SELECT COUNT(*) FROM news_metadata;

SELECT COUNT(*) FROM news_metadata WHERE is_processed = FALSE;

SELECT COUNT(*) FROM sentiment_scores;

ALTER TABLE sentiment_scores
ADD COLUMN sentiment_label VARCHAR;

ALTER TABLE sentiment_scores
ADD COLUMN confidence_score FLOAT;

SELECT * FROM document_chunks

ALTER TABLE document_chunks
ADD COLUMN is_embedded BOOLEAN DEFAULT FALSE;
