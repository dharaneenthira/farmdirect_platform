-- =============================================================================
-- FarmDirect Platform Seed Data Script
-- Problem Statement ID: SIH26033 | Team: Shadow Stack
-- Description: Realistic demo seed data for farmer, buyer, and admin users and profiles.
-- NOTE: Passwords are stored only as Werkzeug-generated hashes.
-- No plaintext passwords are stored in this seed file.
-- =============================================================================

USE farmdirect_db;

-- 1. Insert Demo Users
INSERT INTO users (id, full_name, email, phone, password_hash, role, district, state, is_active)
VALUES
(1, 'Ramesh Kumar', 'farmer.ramesh@example.com', '+919876543210', 'scrypt:32768:8:1$u0fSWHroX6gssmff$e4560a0735578daa4a42093cf63123a69930e8c0e537e38979b0ad8f441cac4c862ac21628d6bdf234476e4310b5361ea6bd36b9dfa530da85d4232c324e2b0c', 'farmer', 'Coimbatore', 'Tamil Nadu', TRUE),
(2, 'Agro Wholesale Corp', 'buyer.agro@example.com', '+919876543211', 'scrypt:32768:8:1$iGIQ5TuwkONIdkzK$82a056a43d9db6a3307ffd5e5e80f5f597ff3e00390b2f36f134ef5d3b108476f30bb14204005f8965d597eee990b2f564939d1fcb132e49c02f6af4ebe5efba', 'buyer', 'Chennai', 'Tamil Nadu', TRUE),
(3, 'System Administrator', 'admin.portal@example.com', '+919876543212', 'scrypt:32768:8:1$crjXl8skwUotEGKP$888d44bf008daf477082329a87845d2504756d4d3127b0be11a2d7153ffb391cb6beaed82c5ccc2f798ae1084c87b82b49ec1d7bc0b905d891bb4c2c1355327f', 'admin', 'Central Office', 'Tamil Nadu', TRUE)
ON DUPLICATE KEY UPDATE full_name=VALUES(full_name), password_hash=VALUES(password_hash);

-- 2. Insert Farmer Profile
INSERT INTO farmer_profiles (id, user_id, farm_name, crop_types, land_area, location, verification_status)
VALUES
(1, 1, 'Green Valley Organic Farm', 'Tomatoes, Onions, Paddy', 12.50, 'Pollachi Road, Coimbatore', 'verified')
ON DUPLICATE KEY UPDATE farm_name=VALUES(farm_name), verification_status=VALUES(verification_status);

-- 3. Insert Buyer Profile
INSERT INTO buyer_profiles (id, user_id, business_name, business_type, verification_status)
VALUES
(1, 2, 'Agro Wholesale Corp Pvt Ltd', 'Wholesaler / Processing Plant', 'verified')
ON DUPLICATE KEY UPDATE business_name=VALUES(business_name), verification_status=VALUES(verification_status);

-- 4. Insert Admin Profile
INSERT INTO admin_profiles (id, user_id, department, permissions)
VALUES
(1, 3, 'Platform Oversight', 'ALL_PERMISSIONS')
ON DUPLICATE KEY UPDATE department=VALUES(department), permissions=VALUES(permissions);

-- 5. Insert Initial Audit Logs
INSERT INTO audit_logs (user_id, action, entity_type, entity_id, ip_address)
VALUES
(3, 'SYSTEM_INIT', 'SYSTEM', 0, '127.0.0.1'),
(1, 'FARMER_REGISTRATION', 'user', 1, '127.0.0.1'),
(2, 'BUYER_REGISTRATION', 'user', 2, '127.0.0.1');

-- 6. Insert Sample Products
INSERT INTO products (id, farmer_id, name, category, description, quantity, unit, asking_price, location, status)
VALUES
(1, 1, 'Organic Fresh Tomatoes', 'Vegetables', 'Farm-fresh organic red tomatoes harvested daily.', 500.00, 'kg', 35.00, 'Coimbatore', 'active'),
(2, 1, 'Premium Sona Masoori Paddy', 'Grains', 'High quality raw paddy direct from farm.', 1000.00, 'kg', 42.50, 'Coimbatore', 'active')
ON DUPLICATE KEY UPDATE name=VALUES(name), asking_price=VALUES(asking_price);
