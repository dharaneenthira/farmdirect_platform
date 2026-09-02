# FarmDirect — Direct Agricultural Marketplace Prototype

**Smart India Hackathon 2026 Prototype**  
**Problem Statement ID:** SIH26033  
**Team Name:** Shadow Stack  

---

## 1. FarmDirect Overview
FarmDirect is an advanced digital agricultural platform designed to connect smallholder and commercial farmers directly with produce buyers (retailers, wholesalers, institutional buyers, and consumers). By leveraging a decentralized direct trade model with AI-powered analytics and bilingual support, FarmDirect restores profit margins to agricultural producers while offering transparent pricing to buyers.

---

## 2. SIH26033 Problem Statement
- **Problem Statement ID:** SIH26033
- **Theme:** Smart Agriculture / Supply Chain Optimization
- **Target Domain:** Agricultural Trade, Price Transparency, Direct Farmer Monetization

---

## 3. Problem Description
Multiple intermediaries (middlemen, commission agents, regional brokers, and multi-tier traders) severely inflate consumer produce prices while reducing the actual farmgate earnings for farmers. Smallholder farmers often suffer from:
- Lack of real-time mandi price transparency.
- Asymmetric market demand information leading to distress sales.
- Inefficient regional logistics resulting in high post-harvest spoilage.
- Opaque quality grading standards dictated solely by intermediaries.

---

## 4. Proposed Solution
FarmDirect establishes a direct, transparent digital bridge between farmers and buyers:
- **Direct Trading Marketplace:** Enables farmers to publish produce listings with quality grades without broker interference.
- **AI Price Prediction & Demand Forecasting:** Empowers farmers with predictive price insights so they know *when* and *where* to sell.
- **Smart Farmer-Buyer Matching:** Algorithmic pairing based on location, produce volume, and transport efficiency (including partial order matching).
- **Price Transparency & Anomaly Detection:** Real-time benchmark price tracking and algorithmic detection of artificial price gouging or hoarding.
- **Centralized English/Tamil Localization:** First-class bilingual experience tailored for rural usability.

---

## 5. Target Users
1. **FARMER:** Smallholder & commercial agricultural producers seeking fair market value, profit simulation, and price forecasts.
2. **BUYER:** Retailers, wholesalers, hotels/restaurants, food processors, and end-consumers needing fresh produce directly from farms.
3. **ADMIN:** Platform administrators monitoring market stability, verifying users, and resolving price/transaction anomalies.

---

## 6. Technology Stack
- **Frontend:** HTML5, CSS3, Vanilla JavaScript (DOM & Fetch API)
- **Backend:** Python 3.10+, Flask, RESTful APIs
- **Database:** MySQL 8.0+, SQLAlchemy ORM
- **AI / Data Analytics:** Python, Pandas, NumPy, scikit-learn
- **Visualization:** Chart.js
- **Maps / GIS:** Leaflet.js, OpenStreetMap
- **Testing:** Pytest

---

## 7. Planned Modules
1. Authentication & Role Management (FARMER, BUYER, ADMIN)
2. Farmer Dashboard
3. Buyer Dashboard
4. Admin Command Center
5. Agricultural Marketplace
6. Crop/Product Management
7. Market Data Analysis
8. AI Price Prediction
9. AI Demand Forecasting
10. Smart Farmer-Buyer Matching
11. Price Transparency Engine
12. Farmer Profit Simulator
13. Produce Quality Grading
14. Verified Users System
15. Ratings & Reviews
16. Order Management
17. Partial Order Matching
18. Smart Logistics Routing
19. Delivery Tracking
20. Transaction Management
21. Notifications Engine
22. Transaction Traceability
23. Price Anomaly Detection
24. Suspicious Activity Detection
25. Impact Analytics

---

## 8. Planned AI Modules
- **Price Prediction:** Time-series and regression models (Random Forest, XGBoost) to forecast mandi crop prices.
- **Demand Forecasting:** Regional buyer demand projection using historical purchase data and seasonality.
- **Smart Matching:** Multi-variable matching algorithms pairing crop availability with buyer bids (including partial pooling).
- **Anomaly Detection:** Unsupervised outlier detection (Isolation Forest) identifying suspicious price spikes, fake listings, and collusive bidding.

*(Note: All AI modules are in the architecture definition phase for Step 1).*

---

## 9. English / Tamil Language Support (i18n Architecture)
FarmDirect includes a centralized internationalization engine designed from day one:
- Dynamic key lookup (`data-i18n` attributes & `t(key)` helper).
- Instant language switching between **English** and **Tamil (தமிழ்)** without reloading pages.
- Client-side preference persistence in `localStorage` (`farmdirect_lang`).
- Architecture located in:
  - `frontend/js/i18n/translations.js` (Bilingual string dictionary)
  - `frontend/js/i18n/i18n.js` (Localization engine)

---

## 10. High-Level Architecture
```text
[ Frontend (HTML5 / Vanilla JS / CSS3 + i18n) ]
                       │
              REST APIs (JSON)
                       ▼
[ Flask Backend API (Python / SQLAlchemy) ]
         │                        │
         ▼                        ▼
[ MySQL Database ]     [ AI Analytics Engine ]
```

---

## 11. Project Structure
```text
FarmDirect-SIH26033/
│
├── frontend/
│   ├── index.html
│   ├── pages/
│   │   ├── auth/
│   │   ├── farmer/
│   │   ├── buyer/
│   │   ├── admin/
│   │   ├── marketplace/
│   │   ├── orders/
│   │   └── errors/
│   ├── components/
│   ├── css/
│   │   ├── base/
│   │   ├── components/
│   │   ├── layouts/
│   │   └── pages/
│   ├── js/
│   │   ├── api/
│   │   ├── auth/
│   │   ├── components/
│   │   ├── utils/
│   │   └── i18n/
│   │       ├── translations.js
│   │       └── i18n.js
│   └── assets/
│       ├── images/
│       └── icons/
│
├── backend/
│   ├── app.py
│   ├── routes/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── middleware/
│   ├── utils/
│   ├── config/
│   └── db/
│
├── ai/
│   ├── price_prediction/
│   ├── demand_forecasting/
│   ├── smart_matching/
│   ├── anomaly_detection/
│   └── common/
│
├── database/
│   ├── schema.sql
│   └── seed.sql
│
├── docs/
│   ├── architecture/
│   ├── api/
│   └── database/
│
├── tests/
│
├── .env.example
├── .gitignore
└── README.md
```

---

## 12. Local Setup Instructions

### Prerequisites
- Python 3.10 or higher installed.
- MySQL 8.0 or higher (or MariaDB) server running.
- Modern web browser (Chrome, Edge, Firefox).

### Step 1: Database Setup (MySQL)
1. Start your MySQL service and log in to MySQL command line:
   ```bash
   mysql -u root -p
   ```
2. Create the database:
   ```sql
   CREATE DATABASE IF NOT EXISTS farmdirect_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```
3. Initialize tables schema and seed demo data:
   ```bash
   mysql -u root -p farmdirect_db < database/schema.sql
   mysql -u root -p farmdirect_db < database/seed.sql
   ```

### Step 2: Environment Configuration
Copy `.env.example` to `.env` and fill in your local MySQL credentials:
```bash
cp .env.example .env
```
Ensure your `.env` contains:
```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=farmdirect_db
DB_USER=root
DB_PASSWORD=your_mysql_password
DATABASE_URL=mysql+pymysql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}
```

### Step 3: Backend Setup & Server Execution
1. Install backend dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
2. Start the Flask Backend Server:
   ```bash
   python backend/app.py
   ```
3. Verify backend health endpoint in browser or terminal:
   ```bash
   GET http://127.0.0.1:5000/api/health
   ```
   Expected Response:
   ```json
   {
       "status": "success",
       "backend": "running",
       "database": "connected"
   }
   ```

### Step 4: Running Automated Tests (Pytest)
Run the test suite (uses safe isolated SQLite test environment):
```bash
python -m pytest tests/
```

### Step 5: Frontend Setup & Run
Serve the `frontend` directory using any HTTP server:
```bash
python -m http.server 8000 --directory frontend
```
Navigate to `http://localhost:8000` to interact with the FarmDirect landing page.

---

## 13. Development Rules
1. Maintain strict modularity across Frontend, Backend, Database, and AI folders.
2. Keep code clean and understandable for student developer team members.
3. Do NOT hardcode secrets, API keys, or database credentials. Always use `.env`.
4. Do NOT implement fake business logic or claim features are completed when they are only planned.
5. All text in the UI must use dynamic i18n keys from `translations.js`.

---

## 14. Future Implementation Roadmap
- **Phase 1 (Current Step 1):** Clean project foundation, Flask API architecture, dynamic i18n framework, landing page, and documentation.
- **Phase 2 (Step 2):** Authentication, Role-based access control (RBAC), and User Profiles.
- **Phase 3 (Step 3):** Product listings, Mandi price data ingestion, and Agricultural Marketplace.
- **Phase 4 (Step 4):** AI Price Prediction and Demand Forecasting pipelines.
- **Phase 5 (Step 5):** Order management, partial matching, smart logistics, and payment settlement.
