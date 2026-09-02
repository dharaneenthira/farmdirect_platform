-- =============================================================================
-- FarmDirect Platform Database Schema Blueprint
-- Problem Statement ID: SIH26033 | Team: Shadow Stack
-- Database Engine: MySQL 8.0+
-- Description: Architecture definition for planned entities.
-- NOTE: STEP 1 Foundation - Table definitions prepared for future execution.
-- =============================================================================

CREATE DATABASE IF NOT EXISTS farmdirect_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE farmdirect_db;

-- 1. Users Entity Architecture
-- Stores core authentication & role metadata (FARMER, BUYER, ADMIN)
-- CREATE TABLE IF NOT EXISTS users (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     full_name VARCHAR(100) NOT NULL,
--     phone_number VARCHAR(15) UNIQUE NOT NULL,
--     email VARCHAR(120) UNIQUE,
--     password_hash VARCHAR(255) NOT NULL,
--     role ENUM('FARMER', 'BUYER', 'ADMIN') NOT NULL,
--     is_verified BOOLEAN DEFAULT FALSE,
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
-- );

-- 2. Farmer Profiles Entity Architecture
-- CREATE TABLE IF NOT EXISTS farmer_profiles (...);

-- 3. Buyer Profiles Entity Architecture
-- CREATE TABLE IF NOT EXISTS buyer_profiles (...);

-- 4. Products Entity Architecture
-- CREATE TABLE IF NOT EXISTS products (...);

-- 5. Market Prices Entity Architecture
-- CREATE TABLE IF NOT EXISTS market_prices (...);

-- 6. Price Predictions Entity Architecture
-- CREATE TABLE IF NOT EXISTS price_predictions (...);

-- 7. Demand Forecasts Entity Architecture
-- CREATE TABLE IF NOT EXISTS demand_forecasts (...);

-- 8. Matches Entity Architecture
-- CREATE TABLE IF NOT EXISTS matches (...);

-- 9. Orders & Order Items Entity Architecture
-- CREATE TABLE IF NOT EXISTS orders (...);
-- CREATE TABLE IF NOT EXISTS order_items (...);

-- 10. Deliveries Entity Architecture
-- CREATE TABLE IF NOT EXISTS deliveries (...);

-- 11. Transactions Entity Architecture
-- CREATE TABLE IF NOT EXISTS transactions (...);

-- 12. Reviews & Ratings Architecture
-- CREATE TABLE IF NOT EXISTS reviews (...);
-- CREATE TABLE IF NOT EXISTS ratings (...);

-- 13. Notifications Architecture
-- CREATE TABLE IF NOT EXISTS notifications (...);

-- 14. Admin Activity Audit Architecture
-- CREATE TABLE IF NOT EXISTS admin_activity (...);
