# FarmDirect Architecture Overview

**Problem Statement ID:** SIH26033  
**Team:** Shadow Stack  

## High-Level Architecture

FarmDirect is designed as a decoupled 3-tier web application to eliminate intermediaries, optimize agricultural supply chains, and empower Indian farmers with direct market access and AI decision support.

```text
[ Frontend (HTML5/CSS3/Vanilla JS + i18n) ]
                     │
             HTTP / REST APIs
                     ▼
[ Flask REST API Backend (Python / SQLAlchemy) ]
        │                       │
        ▼                       ▼
[ MySQL Database ]    [ AI Analytics Engine ]
```

## Layer Responsibilities

### 1. Frontend (`/frontend`)
- UI layout, landing page, and future role dashboards (Farmer, Buyer, Admin).
- Centralized English (en) / Tamil (ta) localization via dynamic translation dictionary (`i18n.js`).
- Clean presentation using standard vanilla HTML5/CSS3/JavaScript without heavy external frameworks.

### 2. Backend API (`/backend`)
- Flask application factory with modular Blueprints for clean routing.
- SQLAlchemy ORM database abstraction layer targeting MySQL.
- Standardized REST response structures and error handling middleware.
- Environment variable configuration isolating secrets.

### 3. AI / Data Analytics (`/ai`)
- Modular structure prepared for price forecasting, demand forecasting, smart matching algorithms, and anomaly detection.
- Data processing pipelines utilizing NumPy, Pandas, and scikit-learn.

### 4. Database (`/database`)
- Standard SQL DDL scripts (`schema.sql`) and sample dataset seeds (`seed.sql`).
- Relational integrity enforcing entity boundaries across Users, Products, Orders, Transactions, and Analytics.
