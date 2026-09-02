# FarmDirect Entity Relationship & Database Design

**Problem Statement ID:** SIH26033

## Planned Entities

1. **users**: Primary user accounts (FARMER, BUYER, ADMIN).
2. **farmer_profiles**: Detailed agricultural data (location, farm size, crops grown, verification status).
3. **buyer_profiles**: Detailed buyer data (business type, location, purchasing history).
4. **products**: Crop inventory listings created by farmers.
5. **market_prices**: Historical & real-time mandi prices across regions.
6. **price_predictions**: ML generated crop price forecasts.
7. **demand_forecasts**: ML generated regional demand projections.
8. **matches**: Algorithmic pairing between farmer crop listings and buyer demands.
9. **orders**: Purchase commitments between buyers and farmers.
10. **order_items**: Itemized breakdown of produce quantity, unit price, and quality grade.
11. **deliveries**: Smart logistics dispatch, status, and tracking coordinates.
12. **transactions**: Direct payment records, escrows, and payouts.
13. **reviews**: Buyer and farmer feedback.
14. **ratings**: Multi-criteria produce quality & fulfillment ratings.
15. **notifications**: In-app and SMS user alerts.
16. **admin_activity**: Operational audit logs.
