# Requirements Document

## Introduction

This document specifies the requirements for a complete B2B ERP analytics system using the Olist Brazilian E-Commerce dataset. The system demonstrates a modern data stack architecture with Python-based data ingestion, Snowflake data warehousing, dbt transformations following the Medallion architecture, and Power BI dashboards for business intelligence.

## Glossary

- **Bronze_Layer**: Raw data storage layer in Snowflake containing unprocessed CSV data
- **Silver_Layer**: Staging layer with cleaned, standardized data
- **Gold_Layer**: Analytics-ready layer with dimensional models (star schema)
- **Ingestion_System**: Python-based data loading system using snowflake-connector-python
- **dbt_Transformation_System**: Data transformation pipeline using dbt (data build tool)
- **Star_Schema**: Dimensional modeling approach with fact and dimension tables
- **SCD_Type_2**: Slowly Changing Dimension Type 2 for tracking historical changes
- **Medallion_Architecture**: Data architecture pattern with Bronze, Silver, and Gold layers
- **Power_BI_System**: Business intelligence dashboarding system
- **Olist_Dataset**: Brazilian e-commerce dataset with 9 CSV files
- **Data_Quality_System**: dbt testing framework for data validation

## Requirements

### Requirement 1: Data Ingestion to Bronze Layer

**User Story:** As a data engineer, I want to load all Olist CSV files into Snowflake's Bronze layer, so that raw data is available for downstream transformations.

#### Acceptance Criteria

1. WHEN the Ingestion_System processes the orders CSV file, THE Ingestion_System SHALL create a bronze_orders table in Snowflake
2. WHEN the Ingestion_System processes the order_items CSV file, THE Ingestion_System SHALL create a bronze_order_items table in Snowflake
3. WHEN the Ingestion_System processes the products CSV file, THE Ingestion_System SHALL create a bronze_products table in Snowflake
4. WHEN the Ingestion_System processes the sellers CSV file, THE Ingestion_System SHALL create a bronze_sellers table in Snowflake
5. WHEN the Ingestion_System processes the customers CSV file, THE Ingestion_System SHALL create a bronze_customers table in Snowflake
6. WHEN the Ingestion_System processes the order_payments CSV file, THE Ingestion_System SHALL create a bronze_order_payments table in Snowflake
7. WHEN the Ingestion_System processes the order_reviews CSV file, THE Ingestion_System SHALL create a bronze_order_reviews table in Snowflake
8. WHEN the Ingestion_System processes the geolocation CSV file, THE Ingestion_System SHALL create a bronze_geolocation table in Snowflake
9. WHEN the Ingestion_System processes the product_category_translation CSV file, THE Ingestion_System SHALL create a bronze_product_category_translation table in Snowflake
10. WHEN any CSV file is loaded, THE Ingestion_System SHALL preserve all original columns and data types from the source
11. WHEN a CSV file load fails, THE Ingestion_System SHALL log the error with file name and row number
12. WHEN all CSV files are successfully loaded, THE Ingestion_System SHALL report the row count for each table

### Requirement 2: Silver Layer Staging Transformations

**User Story:** As a data engineer, I want to create cleaned and standardized staging tables in the Silver layer, so that data is prepared for dimensional modeling.

#### Acceptance Criteria

1. WHEN the dbt_Transformation_System processes Bronze_Layer tables, THE dbt_Transformation_System SHALL create staging tables with standardized column names using snake_case
2. WHEN the dbt_Transformation_System encounters null values in non-nullable fields, THE dbt_Transformation_System SHALL apply appropriate default values or filtering
3. WHEN the dbt_Transformation_System processes date columns, THE dbt_Transformation_System SHALL cast them to TIMESTAMP or DATE types
4. WHEN the dbt_Transformation_System processes numeric columns, THE dbt_Transformation_System SHALL cast them to appropriate numeric types (DECIMAL, INTEGER)
5. WHEN the dbt_Transformation_System processes string columns, THE dbt_Transformation_System SHALL trim whitespace and standardize casing where appropriate
6. WHEN the dbt_Transformation_System creates staging models, THE dbt_Transformation_System SHALL prefix table names with "stg_"
7. WHEN the dbt_Transformation_System completes Silver_Layer transformations, THE dbt_Transformation_System SHALL generate documentation for all staging models

### Requirement 3: Gold Layer Dimensional Models

**User Story:** As a data analyst, I want a star schema in the Gold layer with fact and dimension tables, so that I can efficiently query business metrics.

#### Acceptance Criteria

1. THE dbt_Transformation_System SHALL create a fct_b2b_sales fact table joining orders, order_items, and sellers
2. THE dbt_Transformation_System SHALL create a dim_sellers dimension table with seller performance metrics
3. THE dbt_Transformation_System SHALL create a dim_products dimension table with product catalog and category information
4. THE dbt_Transformation_System SHALL create a dim_customers dimension table with customer information
5. THE dbt_Transformation_System SHALL create a fct_logistics fact table with delivery performance metrics
6. WHEN the dbt_Transformation_System creates fact tables, THE dbt_Transformation_System SHALL include foreign keys to all relevant dimension tables
7. WHEN the dbt_Transformation_System creates dimension tables, THE dbt_Transformation_System SHALL include surrogate keys as primary keys
8. WHEN the dbt_Transformation_System creates the fct_b2b_sales table, THE dbt_Transformation_System SHALL include measures for revenue, quantity, freight_value, and price
9. WHEN the dbt_Transformation_System creates the dim_sellers table, THE dbt_Transformation_System SHALL include calculated metrics for total_sales, order_count, and average_rating
10. WHEN the dbt_Transformation_System creates the fct_logistics table, THE dbt_Transformation_System SHALL include metrics for delivery_time, estimated_delivery_time, and delivery_accuracy

### Requirement 4: Data Relationships and Referential Integrity

**User Story:** As a data engineer, I want proper foreign key relationships enforced in the Gold layer, so that data integrity is maintained across the star schema.

#### Acceptance Criteria

1. WHEN the dbt_Transformation_System creates fct_b2b_sales, THE dbt_Transformation_System SHALL include order_id referencing orders
2. WHEN the dbt_Transformation_System creates fct_b2b_sales, THE dbt_Transformation_System SHALL include product_id referencing dim_products
3. WHEN the dbt_Transformation_System creates fct_b2b_sales, THE dbt_Transformation_System SHALL include seller_id referencing dim_sellers
4. WHEN the dbt_Transformation_System creates fct_b2b_sales, THE dbt_Transformation_System SHALL include customer_id referencing dim_customers
5. WHEN the dbt_Transformation_System creates fct_logistics, THE dbt_Transformation_System SHALL include order_id referencing orders
6. THE Data_Quality_System SHALL test that all foreign keys in fact tables have matching records in dimension tables
7. THE Data_Quality_System SHALL test that primary keys in dimension tables are unique
8. THE Data_Quality_System SHALL test that primary keys in dimension tables are not null

### Requirement 5: Slowly Changing Dimensions for Order Status

**User Story:** As a data analyst, I want to track historical changes to order status over time, so that I can analyze order lifecycle patterns.

#### Acceptance Criteria

1. WHEN an order status changes, THE dbt_Transformation_System SHALL create a new snapshot record with the updated status
2. WHEN the dbt_Transformation_System creates a snapshot record, THE dbt_Transformation_System SHALL set the valid_from timestamp to the change timestamp
3. WHEN the dbt_Transformation_System creates a snapshot record, THE dbt_Transformation_System SHALL set the valid_to timestamp of the previous record to the change timestamp
4. WHEN the dbt_Transformation_System creates a snapshot record, THE dbt_Transformation_System SHALL set is_current flag to TRUE for the new record
5. WHEN the dbt_Transformation_System creates a snapshot record, THE dbt_Transformation_System SHALL set is_current flag to FALSE for the previous record
6. THE dbt_Transformation_System SHALL implement SCD_Type_2 using dbt snapshots functionality
7. THE Data_Quality_System SHALL test that only one record per order has is_current set to TRUE

### Requirement 6: Data Quality Testing

**User Story:** As a data engineer, I want comprehensive data quality tests on all models, so that data issues are caught before reaching dashboards.

#### Acceptance Criteria

1. THE Data_Quality_System SHALL test that primary keys are unique across all dimension tables
2. THE Data_Quality_System SHALL test that primary keys are not null across all dimension tables
3. THE Data_Quality_System SHALL test that foreign keys in fact tables reference existing dimension records
4. THE Data_Quality_System SHALL test that date fields contain valid dates
5. THE Data_Quality_System SHALL test that numeric fields contain valid numbers
6. THE Data_Quality_System SHALL test that revenue calculations are non-negative
7. THE Data_Quality_System SHALL test that order_status values are from an accepted list
8. THE Data_Quality_System SHALL test that payment_type values are from an accepted list
9. WHEN any data quality test fails, THE Data_Quality_System SHALL report the test name, table name, and failure count
10. WHEN all data quality tests pass, THE Data_Quality_System SHALL log a success message

### Requirement 7: Executive Sales Overview Dashboard

**User Story:** As an executive, I want a sales overview dashboard showing revenue KPIs and trends, so that I can monitor business performance.

#### Acceptance Criteria

1. THE Power_BI_System SHALL display total revenue as a KPI card
2. THE Power_BI_System SHALL display total order count as a KPI card
3. THE Power_BI_System SHALL display average order value as a KPI card
4. THE Power_BI_System SHALL display a line chart showing revenue trends over time
5. THE Power_BI_System SHALL display a map visualization showing revenue by geographic region
6. THE Power_BI_System SHALL display a bar chart showing revenue by product category
7. THE Power_BI_System SHALL display a table showing top 10 products by revenue
8. WHEN the Power_BI_System queries Snowflake, THE Power_BI_System SHALL use DirectQuery mode for real-time data
9. WHEN a user applies filters, THE Power_BI_System SHALL update all visualizations accordingly

### Requirement 8: Supply Chain War Room Dashboard

**User Story:** As a supply chain manager, I want a logistics dashboard showing delivery performance, so that I can identify and resolve operational issues.

#### Acceptance Criteria

1. THE Power_BI_System SHALL display delivery accuracy percentage as a KPI card
2. THE Power_BI_System SHALL display average handling time as a KPI card
3. THE Power_BI_System SHALL display average shipping cost as a KPI card
4. THE Power_BI_System SHALL display a histogram showing distribution of delivery times
5. THE Power_BI_System SHALL display a scatter plot showing handling time vs shipping cost
6. THE Power_BI_System SHALL display a table showing orders with late deliveries
7. THE Power_BI_System SHALL display a line chart showing delivery accuracy trends over time
8. WHEN the Power_BI_System calculates delivery accuracy, THE Power_BI_System SHALL use the formula: (on_time_deliveries / total_deliveries) * 100
9. WHEN a user clicks on a late delivery, THE Power_BI_System SHALL show order details in a drill-through page

### Requirement 9: B2B Vendor Performance Dashboard

**User Story:** As a marketplace manager, I want a vendor performance dashboard showing seller metrics, so that I can manage seller relationships and SLAs.

#### Acceptance Criteria

1. THE Power_BI_System SHALL display a leaderboard table ranking sellers by total revenue
2. THE Power_BI_System SHALL display seller SLA compliance percentage as a KPI card
3. THE Power_BI_System SHALL display average customer satisfaction score as a KPI card
4. THE Power_BI_System SHALL display a bar chart showing seller performance by category
5. THE Power_BI_System SHALL display a scatter plot showing seller revenue vs customer rating
6. THE Power_BI_System SHALL display a table showing sellers with SLA violations
7. WHEN the Power_BI_System calculates SLA compliance, THE Power_BI_System SHALL use delivery time commitments
8. WHEN a user selects a seller, THE Power_BI_System SHALL filter all visualizations to that seller's data

### Requirement 10: System Integration and Version Control

**User Story:** As a data engineer, I want all code versioned in Git and integrated across the data stack, so that changes are tracked and the system is maintainable.

#### Acceptance Criteria

1. THE Ingestion_System SHALL store Python scripts in a Git repository
2. THE dbt_Transformation_System SHALL store all dbt models, tests, and configurations in a Git repository
3. THE Power_BI_System SHALL connect to Snowflake using service account credentials
4. WHEN the dbt_Transformation_System runs, THE dbt_Transformation_System SHALL connect to Snowflake using the dbt-snowflake adapter
5. WHEN the dbt_Transformation_System completes successfully, THE dbt_Transformation_System SHALL generate documentation accessible via dbt docs serve
6. THE dbt_Transformation_System SHALL use environment-specific profiles for development, staging, and production
7. WHEN code changes are committed to Git, THE system SHALL include descriptive commit messages
8. THE Ingestion_System SHALL use environment variables for Snowflake credentials

### Requirement 11: Documentation and Metadata

**User Story:** As a data analyst, I want comprehensive documentation for all data models, so that I can understand table structures and business logic.

#### Acceptance Criteria

1. THE dbt_Transformation_System SHALL generate documentation for all models using dbt docs
2. WHEN the dbt_Transformation_System generates documentation, THE documentation SHALL include column descriptions for all tables
3. WHEN the dbt_Transformation_System generates documentation, THE documentation SHALL include lineage graphs showing data flow
4. WHEN the dbt_Transformation_System generates documentation, THE documentation SHALL include test results for all models
5. THE dbt_Transformation_System SHALL include schema.yml files documenting all models and columns
6. THE Ingestion_System SHALL include README files documenting setup and execution instructions
7. THE Power_BI_System SHALL include descriptions for all measures and calculated columns

### Requirement 12: Error Handling and Logging

**User Story:** As a data engineer, I want comprehensive error handling and logging across all systems, so that I can troubleshoot issues efficiently.

#### Acceptance Criteria

1. WHEN the Ingestion_System encounters a connection error, THE Ingestion_System SHALL log the error with timestamp and retry the connection
2. WHEN the Ingestion_System encounters a data type mismatch, THE Ingestion_System SHALL log the error with file name, column name, and row number
3. WHEN the dbt_Transformation_System encounters a model failure, THE dbt_Transformation_System SHALL log the error with model name and SQL error message
4. WHEN the dbt_Transformation_System encounters a test failure, THE dbt_Transformation_System SHALL log the test name and failure count
5. IF the Ingestion_System fails to load a CSV file, THEN THE Ingestion_System SHALL continue processing remaining files
6. IF a dbt model fails, THEN THE dbt_Transformation_System SHALL halt execution and report all failed models
7. THE Ingestion_System SHALL write logs to a dedicated log file with rotation
8. THE dbt_Transformation_System SHALL output logs to console and optionally to a log file
