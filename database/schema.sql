USE market_dashboard;

CREATE TABLE Assets(
ticker VARCHAR(10) PRIMARY KEY,
name VARCHAR(100) NOT NULL,
asset_type ENUM('crypto', 'stock') NOT NULL
);

CREATE TABLE Prices(
price_date DATE,
open_price DECIMAL(18,8) NOT NULL,
high_price DECIMAL(18,8) NOT NULL,
low_price DECIMAL(18,8) NOT NULL,
close_price DECIMAL(18,8) NOT NULL,
volume BIGINT NOT NULL,
ticker VARCHAR(10) NOT NULL,
PRIMARY KEY (ticker, price_date),
FOREIGN KEY (ticker) REFERENCES Assets(ticker)
);