-- ============================================================================
-- Experiment 1: Design Star and Snowflake Schema for Movie Ticket Booking System
-- Student: Bhavesh Punjabi | Roll No: 40 | Class: D15A
-- Subject: Data Mining and Business Intelligence (DMBI)
-- ============================================================================

-- ============================================================================
-- PART 1: STAR SCHEMA IMPLEMENTATION
-- Central Fact Tables: Fact_Ticket_Sales, Fact_Revenue
-- Dimension Tables: Dim_Date, Dim_Show, Dim_Movie, Dim_Theatre, Dim_Customer,
--                   Dim_Seat, Dim_Payment, Dim_Offer
-- ============================================================================

CREATE DATABASE IF NOT EXISTS MovieBooking_DW;
USE MovieBooking_DW;

-- 1. Dim_Date
CREATE TABLE IF NOT EXISTS Dim_Date (
    date_id INT PRIMARY KEY,
    full_date DATE NOT NULL,
    day_name VARCHAR(15),
    day_of_week INT,
    day_of_month INT,
    month_name VARCHAR(15),
    month_number INT,
    quarter INT,
    year INT,
    is_weekend BOOLEAN
);

-- 2. Dim_Movie
CREATE TABLE IF NOT EXISTS Dim_Movie (
    movie_id INT PRIMARY KEY,
    movie_title VARCHAR(150) NOT NULL,
    genre VARCHAR(50),
    language VARCHAR(50),
    duration_minutes INT,
    director VARCHAR(100),
    rating_category VARCHAR(10),
    release_year INT
);

-- 3. Dim_Theatre
CREATE TABLE IF NOT EXISTS Dim_Theatre (
    theatre_id INT PRIMARY KEY,
    theatre_name VARCHAR(100) NOT NULL,
    chain_name VARCHAR(100),
    city VARCHAR(50),
    state VARCHAR(50),
    pincode VARCHAR(10),
    total_screens INT
);

-- 4. Dim_Show
CREATE TABLE IF NOT EXISTS Dim_Show (
    show_id INT PRIMARY KEY,
    show_time TIME NOT NULL,
    time_slot VARCHAR(30), -- Morning, Matinee, Evening, Night
    screen_number INT,
    screen_format VARCHAR(20) -- 2D, 3D, IMAX, 4DX
);

-- 5. Dim_Customer
CREATE TABLE IF NOT EXISTS Dim_Customer (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100),
    gender VARCHAR(10),
    age INT,
    age_group VARCHAR(20),
    city VARCHAR(50),
    membership_tier VARCHAR(20) -- Standard, Silver, Gold, Platinum
);

-- 6. Dim_Seat
CREATE TABLE IF NOT EXISTS Dim_Seat (
    seat_id INT PRIMARY KEY,
    seat_type VARCHAR(30), -- Silver, Gold, Recliner, Balcony
    seat_row VARCHAR(5),
    price_multiplier DECIMAL(3,2)
);

-- 7. Dim_Payment
CREATE TABLE IF NOT EXISTS Dim_Payment (
    payment_id INT PRIMARY KEY,
    payment_mode VARCHAR(30), -- UPI, Credit Card, Debit Card, Net Banking, Cash
    payment_gateway VARCHAR(50),
    payment_status VARCHAR(20)
);

-- 8. Dim_Offer
CREATE TABLE IF NOT EXISTS Dim_Offer (
    offer_id INT PRIMARY KEY,
    offer_code VARCHAR(30),
    offer_description VARCHAR(200),
    discount_pct DECIMAL(5,2),
    max_discount_amount DECIMAL(8,2)
);

-- FACT TABLE 1: Fact_Ticket_Sales (Star Schema)
CREATE TABLE IF NOT EXISTS Fact_Ticket_Sales (
    sales_fact_id INT PRIMARY KEY AUTO_INCREMENT,
    date_id INT,
    movie_id INT,
    theatre_id INT,
    show_id INT,
    customer_id INT,
    seat_id INT,
    tickets_count INT NOT NULL,
    base_price DECIMAL(10,2) NOT NULL,
    discount_amount DECIMAL(10,2) DEFAULT 0.0,
    convenience_fee DECIMAL(10,2) DEFAULT 0.0,
    total_sales_amount DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (date_id) REFERENCES Dim_Date(date_id),
    FOREIGN KEY (movie_id) REFERENCES Dim_Movie(movie_id),
    FOREIGN KEY (theatre_id) REFERENCES Dim_Theatre(theatre_id),
    FOREIGN KEY (show_id) REFERENCES Dim_Show(show_id),
    FOREIGN KEY (customer_id) REFERENCES Dim_Customer(customer_id),
    FOREIGN KEY (seat_id) REFERENCES Dim_Seat(seat_id)
);

-- FACT TABLE 2: Fact_Revenue (Star Schema)
CREATE TABLE IF NOT EXISTS Fact_Revenue (
    revenue_fact_id INT PRIMARY KEY AUTO_INCREMENT,
    date_id INT,
    theatre_id INT,
    payment_id INT,
    offer_id INT,
    ticket_revenue DECIMAL(12,2) NOT NULL,
    food_snack_revenue DECIMAL(12,2) DEFAULT 0.0,
    convenience_revenue DECIMAL(12,2) DEFAULT 0.0,
    tax_collected DECIMAL(12,2) DEFAULT 0.0,
    gross_revenue DECIMAL(12,2) NOT NULL,
    net_revenue DECIMAL(12,2) NOT NULL,
    FOREIGN KEY (date_id) REFERENCES Dim_Date(date_id),
    FOREIGN KEY (theatre_id) REFERENCES Dim_Theatre(theatre_id),
    FOREIGN KEY (payment_id) REFERENCES Dim_Payment(payment_id),
    FOREIGN KEY (offer_id) REFERENCES Dim_Offer(offer_id)
);

-- ============================================================================
-- PART 2: SNOWFLAKE SCHEMA NORMALIZED EXTENSIONS
-- Normalized sub-dimensions:
-- Dim_Theatre -> Dim_Location (City, State, Country, Pincode)
-- Dim_Movie   -> Dim_Genre, Dim_Language
-- ============================================================================

CREATE TABLE IF NOT EXISTS Dim_Location_Snowflake (
    location_id INT PRIMARY KEY,
    city VARCHAR(50) NOT NULL,
    state VARCHAR(50) NOT NULL,
    country VARCHAR(50) DEFAULT 'India',
    pincode VARCHAR(10)
);

CREATE TABLE IF NOT EXISTS Dim_Theatre_Snowflake (
    theatre_id INT PRIMARY KEY,
    theatre_name VARCHAR(100) NOT NULL,
    chain_name VARCHAR(100),
    location_id INT,
    total_screens INT,
    FOREIGN KEY (location_id) REFERENCES Dim_Location_Snowflake(location_id)
);

CREATE TABLE IF NOT EXISTS Dim_Genre_Snowflake (
    genre_id INT PRIMARY KEY,
    genre_name VARCHAR(50) NOT NULL,
    target_audience VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS Dim_Language_Snowflake (
    language_id INT PRIMARY KEY,
    language_name VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS Dim_Movie_Snowflake (
    movie_id INT PRIMARY KEY,
    movie_title VARCHAR(150) NOT NULL,
    genre_id INT,
    language_id INT,
    duration_minutes INT,
    release_year INT,
    FOREIGN KEY (genre_id) REFERENCES Dim_Genre_Snowflake(genre_id),
    FOREIGN KEY (language_id) REFERENCES Dim_Language_Snowflake(language_id)
);

-- ============================================================================
-- PART 3: SAMPLE DATA POPULATION & OLAP ANALYTICAL QUERIES
-- ============================================================================

-- Sample Inserts for Star Schema
INSERT INTO Dim_Date VALUES 
(20261101, '2026-11-01', 'Sunday', 7, 1, 'November', 11, 4, 2026, TRUE),
(20261102, '2026-11-02', 'Monday', 1, 2, 'November', 11, 4, 2026, FALSE);

INSERT INTO Dim_Movie VALUES 
(101, 'Sky Warriors', 'Action', 'English', 145, 'J. Cameron', 'UA', 2026),
(102, 'Love in Paris', 'Romance', 'Hindi', 130, 'K. Johar', 'U', 2026),
(103, 'Laugh Out Loud', 'Comedy', 'Hindi', 120, 'R. Hirani', 'U', 2026);

INSERT INTO Dim_Theatre VALUES 
(201, 'PVR Phoenix Mall', 'PVR Cinemas', 'Mumbai', 'Maharashtra', '400013', 8),
(202, 'INOX Megaplex', 'INOX', 'Pune', 'Maharashtra', '411001', 6);

INSERT INTO Dim_Show VALUES 
(301, '10:30:00', 'Morning', 1, '2D'),
(302, '18:45:00', 'Evening', 2, 'IMAX 3D');

INSERT INTO Dim_Customer VALUES 
(401, 'Bhavesh Punjabi', 'Male', 21, '18-25', 'Mumbai', 'Gold'),
(402, 'Jiya Punjabi', 'Female', 20, '18-25', 'Mumbai', 'Silver');

INSERT INTO Dim_Seat VALUES 
(501, 'Silver', 'D', 1.00),
(502, 'Recliner', 'H', 1.50);

INSERT INTO Fact_Ticket_Sales (date_id, movie_id, theatre_id, show_id, customer_id, seat_id, tickets_count, base_price, discount_amount, convenience_fee, total_sales_amount)
VALUES 
(20261101, 101, 201, 302, 401, 502, 2, 800.00, 80.00, 40.00, 760.00),
(20261101, 102, 201, 301, 402, 501, 3, 750.00, 0.00, 60.00, 810.00);

-- OLAP Analytical Query 1: Total Revenue by Movie and City (Drill-Down / Roll-Up)
SELECT 
    m.movie_title,
    t.city,
    SUM(s.tickets_count) AS total_tickets_sold,
    SUM(s.total_sales_amount) AS gross_sales_amount
FROM Fact_Ticket_Sales s
JOIN Dim_Movie m ON s.movie_id = m.movie_id
JOIN Dim_Theatre t ON s.theatre_id = t.theatre_id
GROUP BY m.movie_title, t.city;

-- OLAP Analytical Query 2: Weekend vs Weekday Sales Performance
SELECT 
    d.is_weekend,
    COUNT(s.sales_fact_id) AS total_transactions,
    SUM(s.total_sales_amount) AS revenue
FROM Fact_Ticket_Sales s
JOIN Dim_Date d ON s.date_id = d.date_id
GROUP BY d.is_weekend;
