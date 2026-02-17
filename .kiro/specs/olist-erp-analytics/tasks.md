# Implementation Plan: Olist ERP Analytics System

## Overview

This implementation plan breaks down the Olist ERP Analytics System into discrete, actionable tasks. The system will be built in phases: (1) Data Ingestion infrastructure, (2) Bronze layer loading, (3) dbt project setup, (4) Silver layer transformations, (5) Gold layer dimensional models, (6) Data quality testing, (7) SCD Type 2 snapshots, and (8) Power BI dashboard development.

Each task builds incrementally on previous work, with checkpoints to validate functionality before proceeding.

## Tasks

- [x] 1. Set up project structure and development environment
  - Create directory structure for Python ingestion scripts, dbt project, and documentation
  - Set up Python virtual environment with required packages (snowflake-connector-python, pandas, python-dotenv, pytest, hypothesis)
  - Create .env.template file for Snowflake credentials
  - Create .gitignore file to exclude credentials and virtual environment
  - Initialize Git repository
  - _Requirements: 10.1, 10.8_

- [ ] 2. Implement Snowflake connection and configuration management
  - [x] 2.1 Create config.py with SnowflakeConfig class
    - Implement configuration class to load Snowflake credentials from environment variables
    - Include fields for account, user, password, warehouse, database, schema, role
    - Add validation for required configuration fields
    - _Requirements: 10.8_
  
  - [ ] 2.2 Create logger.py with IngestionLogger class
    - Implement logging class with methods for log_start, log_success, log_error, log_summary
    - Configure file-based logging with rotation
    - Add timestamp formatting for all log entries
    - _Requirements: 12.7, 1.11_
  
  - [ ]* 2.3 Write unit tests for configuration and logging
    - Test configuration loading from environment variables
    - Test logging output format and file creation
    - Test error logging with various error types
    - _Requirements: 10.8, 12.7_

- [ ] 3. Implement CSV ingestion engine
  - [x] 3.1 Create ingestion_engine.py with CSVIngestionEngine class
    - Implement __init__ method to accept SnowflakeConfig
    - Implement connect() method with connection error handling and retry logic
    - Implement close() method to properly close Snowflake connection
    - _Requirements: 12.1_
  
  - [x] 3.2 Implement schema inference and table creation
    - Implement infer_schema() method to analyze pandas DataFrame and generate Snowflake data types
    - Use VARCHAR as default/fallback type for safety
    - Implement create_table_from_csv() method to generate and execute CREATE TABLE statement
    - _Requirements: 1.10_
  
  - [x] 3.3 Implement CSV loading logic
    - Implement file reading with pandas (handle encoding issues)
    - Implement Snowflake PUT command to stage CSV file
    - Implement COPY INTO command to load data from stage
    - Add row count validation after load
    - _Requirements: 1.10, 1.12_
  
  - [x] 3.4 Implement error handling and resilience
    - Add try-except blocks for file not found, connection errors, data type errors
    - Implement continue-on-error logic (don't halt on single file failure)
    - Log all errors with contextual information (file name, row number, error message)
    - _Requirements: 1.11, 12.2, 12.5_
  
  - [x] 3.5 Implement load_all_files() orchestration method
    - Accept file mapping dictionary (CSV filename → table name)
    - Iterate through all files and call create_table_from_csv for each
    - Collect results (success/failure, row counts) for all files
    - Return summary dictionary with results
    - _Requirements: 1.12_
  
  - [ ]* 3.6 Write property test for CSV to table mapping
    - **Property 1: CSV File to Table Mapping**
    - **Validates: Requirements 1.1-1.9**
    - Use hypothesis to test that any CSV file creates corresponding table
  
  - [ ]* 3.7 Write property test for column preservation
    - **Property 2: Column Preservation**
    - **Validates: Requirements 1.10**
    - Test that all source CSV columns appear in Bronze table
  
  - [ ]* 3.8 Write property test for ingestion resilience
    - **Property 5: Ingestion Resilience**
    - **Validates: Requirements 12.5**
    - Test that failure of one file doesn't stop processing of others

- [ ] 4. Create main ingestion script and load Bronze layer
  - [x] 4.1 Create main.py ingestion script
    - Define FILE_MAPPING dictionary with all 9 Olist CSV files
    - Instantiate SnowflakeConfig, IngestionLogger, and CSVIngestionEngine
    - Call load_all_files() with FILE_MAPPING
    - Log summary of results (successful loads, failures, row counts)
    - _Requirements: 1.1-1.9, 1.12_
  
  - [x] 4.2 Create Snowflake Bronze database and schema
    - Write SQL script to create BRONZE database
    - Create PUBLIC schema in BRONZE database
    - Grant appropriate permissions to service account
    - _Requirements: 1.1-1.9_
  
  - [x] 4.3 Execute ingestion for all 9 CSV files
    - Run main.py to load all Olist CSV files into Bronze layer
    - Verify all 9 tables created: bronze_orders, bronze_order_items, bronze_products, bronze_sellers, bronze_customers, bronze_order_payments, bronze_order_reviews, bronze_geolocation, bronze_product_category_translation
    - Verify row counts match source CSV files
    - _Requirements: 1.1-1.9, 1.12_

- [x] 5. Checkpoint - Validate Bronze layer ingestion
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 6. Initialize dbt project for transformations
  - [ ] 6.1 Create dbt project structure
    - Run `dbt init dbt_olist_analytics` to create project
    - Create models/staging/ directory for Silver layer models
    - Create models/marts/ directory for Gold layer models
    - Create models/snapshots/ directory for SCD Type 2
    - Create tests/ directory for custom data tests
    - Create macros/ directory for reusable SQL
    - _Requirements: 10.2_
  
  - [ ] 6.2 Configure dbt profiles and project settings
    - Create profiles.yml with Snowflake connection settings
    - Configure dbt_project.yml with project name, version, model paths
    - Set up environment-specific profiles (dev, staging, prod)
    - Configure target schemas: SILVER for staging, GOLD for marts
    - _Requirements: 10.4, 10.6_
  
  - [ ] 6.3 Define Bronze layer sources in sources.yml
    - Create models/staging/sources.yml
    - Define source for BRONZE database
    - List all 9 Bronze tables as source tables
    - Add source freshness checks
    - _Requirements: 2.1_

- [ ] 7. Implement Silver layer staging models
  - [ ] 7.1 Create stg_orders.sql staging model
    - Select from bronze_orders source
    - Cast timestamp columns using TRY_TO_TIMESTAMP
    - Filter out records with null order_id
    - Add model documentation in schema.yml
    - _Requirements: 2.1, 2.2, 2.3, 2.6_
  
  - [ ] 7.2 Create stg_order_items.sql staging model
    - Select from bronze_order_items source
    - Cast price and freight_value to DECIMAL using TRY_TO_NUMBER
    - Cast shipping_limit_date to TIMESTAMP
    - Filter out records with null order_id, product_id, or seller_id
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.6_
  
  - [ ] 7.3 Create stg_products.sql staging model
    - Select from bronze_products source
    - Cast numeric columns (weight, dimensions) to INTEGER
    - Trim whitespace from product_category_name
    - Filter out records with null product_id
    - _Requirements: 2.1, 2.2, 2.4, 2.5, 2.6_
  
  - [ ] 7.4 Create stg_sellers.sql staging model
    - Select from bronze_sellers source
    - Trim whitespace from city and state columns
    - Filter out records with null seller_id
    - _Requirements: 2.1, 2.2, 2.5, 2.6_
  
  - [ ] 7.5 Create stg_customers.sql staging model
    - Select from bronze_customers source
    - Trim whitespace from city and state columns
    - Filter out records with null customer_id
    - _Requirements: 2.1, 2.2, 2.5, 2.6_
  
  - [ ] 7.6 Create stg_order_payments.sql staging model
    - Select from bronze_order_payments source
    - Cast payment_value to DECIMAL
    - Filter out records with null order_id
    - _Requirements: 2.1, 2.2, 2.4, 2.6_
  
  - [ ] 7.7 Create stg_order_reviews.sql staging model
    - Select from bronze_order_reviews source
    - Cast review_score to INTEGER
    - Cast timestamp columns to TIMESTAMP
    - Filter out records with null review_id
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.6_
  
  - [ ] 7.8 Create stg_geolocation.sql staging model
    - Select from bronze_geolocation source
    - Cast lat/lng to DECIMAL
    - Trim whitespace from city and state
    - _Requirements: 2.1, 2.2, 2.4, 2.5, 2.6_
  
  - [ ] 7.9 Create staging schema.yml with model documentation
    - Document all staging models with descriptions
    - Document all columns with descriptions
    - Add basic schema tests (unique, not_null) for primary keys
    - _Requirements: 2.7, 11.5_
  
  - [ ]* 7.10 Write property test for staging table naming convention
    - **Property 6: Staging Table Naming Convention**
    - **Validates: Requirements 2.6**
    - Test that all staging tables start with "stg_"
  
  - [ ]* 7.11 Write property test for column name standardization
    - **Property 7: Column Name Standardization**
    - **Validates: Requirements 2.1**
    - Test that all staging columns use snake_case

- [ ] 8. Implement Gold layer dimension tables
  - [ ] 8.1 Create generate_surrogate_key macro
    - Create macros/generate_surrogate_key.sql
    - Use dbt_utils.generate_surrogate_key or implement MD5 hash-based key generation
    - _Requirements: 3.7_
  
  - [ ] 8.2 Create dim_products.sql dimension model
    - Join stg_products with bronze_product_category_translation for English category names
    - Calculate product metrics (total_orders, total_revenue, avg_price) from stg_order_items
    - Generate product_key surrogate key
    - Include all product attributes and calculated metrics
    - _Requirements: 3.3, 3.7_
  
  - [ ] 8.3 Create dim_sellers.sql dimension model
    - Select from stg_sellers
    - Calculate seller metrics (total_orders, total_sales, avg_order_value, avg_rating, review_count)
    - Join with stg_order_items for sales metrics
    - Join with stg_order_reviews for rating metrics
    - Generate seller_key surrogate key
    - _Requirements: 3.2, 3.7, 3.9_
  
  - [ ] 8.4 Create dim_customers.sql dimension model
    - Select from stg_customers
    - Calculate customer metrics (total_orders, first_order_date, last_order_date)
    - Join with stg_orders for order metrics
    - Generate customer_key surrogate key
    - _Requirements: 3.4, 3.7_
  
  - [ ] 8.5 Create marts schema.yml with dimension documentation
    - Document all dimension models
    - Document all columns including surrogate keys and calculated metrics
    - Add schema tests for surrogate keys (unique, not_null)
    - _Requirements: 11.5_
  
  - [ ]* 8.6 Write property test for surrogate key presence
    - **Property 11: Surrogate Key Presence**
    - **Validates: Requirements 3.7**
    - Test that all dimension tables have surrogate key columns
  
  - [ ]* 8.7 Write property test for primary key uniqueness
    - **Property 14: Primary Key Uniqueness**
    - **Validates: Requirements 4.7, 6.1**
    - Test that all dimension primary keys are unique
  
  - [ ]* 8.8 Write property test for primary key not null
    - **Property 15: Primary Key Not Null**
    - **Validates: Requirements 4.8, 6.2**
    - Test that all dimension primary keys are not null

- [ ] 9. Implement Gold layer fact tables
  - [ ] 9.1 Create fct_b2b_sales.sql fact table
    - Join stg_orders, stg_order_items, and aggregate stg_order_payments
    - Include foreign keys: order_id, product_id, seller_id, customer_id
    - Include measures: price, freight_value, total_item_value, total_payment_value
    - Include order timestamps and status
    - Generate sales_key surrogate key
    - _Requirements: 3.1, 3.6, 3.8_
  
  - [ ] 9.2 Create fct_logistics.sql fact table
    - Select from stg_orders with delivery timestamps
    - Aggregate freight_value from stg_order_items
    - Calculate delivery metrics: handling_time_days, shipping_time_days, total_delivery_time_days
    - Calculate is_on_time_delivery flag (delivered_date <= estimated_date)
    - Filter to only delivered orders
    - Generate logistics_key surrogate key
    - _Requirements: 3.5, 3.6, 3.10_
  
  - [ ] 9.3 Add fact table documentation to marts schema.yml
    - Document both fact tables with descriptions
    - Document all columns including foreign keys and measures
    - Add schema tests for foreign keys (not_null, relationships to dimensions)
    - _Requirements: 11.5_
  
  - [ ]* 9.4 Write property test for foreign key presence
    - **Property 12: Foreign Key Presence in Fact Tables**
    - **Validates: Requirements 3.6**
    - Test that fact tables include all required foreign key columns
  
  - [ ]* 9.5 Write property test for referential integrity
    - **Property 13: Referential Integrity**
    - **Validates: Requirements 4.2-4.6, 6.3**
    - Test that all foreign keys reference existing dimension records

- [ ] 10. Implement data quality tests
  - [ ] 10.1 Add dbt schema tests to staging models
    - Add unique and not_null tests for primary keys in all staging models
    - Add relationships tests for foreign keys (order_items → orders, etc.)
    - Add accepted_values tests for order_status and payment_type
    - _Requirements: 6.1, 6.2, 6.3, 6.7, 6.8_
  
  - [ ] 10.2 Create custom data test for revenue non-negativity
    - Create tests/assert_positive_revenue.sql
    - Test that all revenue fields (price, freight_value, total_item_value) are >= 0
    - _Requirements: 6.6_
  
  - [ ] 10.3 Add data type validation tests
    - Add tests to verify date columns contain valid dates (not null or valid timestamp)
    - Add tests to verify numeric columns contain valid numbers
    - _Requirements: 6.4, 6.5_
  
  - [ ]* 10.4 Write property test for revenue non-negativity
    - **Property 21: Revenue Non-Negativity**
    - **Validates: Requirements 6.6**
    - Test that all revenue calculations are non-negative
  
  - [ ]* 10.5 Write property test for order status domain validation
    - **Property 22: Order Status Domain Validation**
    - **Validates: Requirements 6.7**
    - Test that all order_status values are from accepted list
  
  - [ ]* 10.6 Write property test for payment type domain validation
    - **Property 23: Payment Type Domain Validation**
    - **Validates: Requirements 6.8**
    - Test that all payment_type values are from accepted list

- [ ] 11. Implement SCD Type 2 snapshot for order status
  - [ ] 11.1 Create order_status_snapshot.sql snapshot
    - Create snapshots/order_status_snapshot.sql
    - Configure snapshot with unique_key='order_id' and strategy='check' on order_status column
    - Select order_id, order_status, and relevant timestamps from stg_orders
    - _Requirements: 5.6_
  
  - [ ] 11.2 Run snapshot and verify SCD Type 2 behavior
    - Run `dbt snapshot` to create initial snapshot
    - Manually update order_status in Bronze layer for testing
    - Run `dbt snapshot` again to capture changes
    - Verify new records created with dbt_valid_from, dbt_valid_to, dbt_scd_id
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_
  
  - [ ] 11.3 Add snapshot documentation
    - Document snapshot in schema.yml
    - Explain SCD Type 2 behavior and metadata columns
    - _Requirements: 11.5_
  
  - [ ]* 11.4 Write property test for SCD current record uniqueness
    - **Property 17: SCD Current Record Uniqueness**
    - **Validates: Requirements 5.7**
    - Test that only one record per order has is_current = TRUE
  
  - [ ]* 11.5 Write property test for SCD temporal validity
    - **Property 18: SCD Temporal Validity**
    - **Validates: Requirements 5.2-5.5**
    - Test that current records have valid_to = NULL and historical records have valid_to set

- [ ] 12. Checkpoint - Validate dbt transformations and tests
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 13. Generate and publish dbt documentation
  - [ ] 13.1 Run dbt docs generate
    - Execute `dbt docs generate` to create documentation artifacts
    - Verify documentation includes all models, columns, tests, and lineage
    - _Requirements: 10.5, 11.1_
  
  - [ ] 13.2 Review documentation completeness
    - Verify all models have descriptions
    - Verify all columns have descriptions
    - Verify lineage graphs show data flow from Bronze → Silver → Gold
    - Verify test results are included
    - _Requirements: 11.2, 11.3, 11.4_
  
  - [ ] 13.3 Create README for dbt project
    - Document project structure and purpose
    - Document setup instructions (profiles.yml configuration)
    - Document execution instructions (dbt run, dbt test, dbt snapshot)
    - Document model dependencies and lineage
    - _Requirements: 11.6_

- [ ] 14. Create Power BI data model and connections
  - [ ] 14.1 Set up Snowflake connection in Power BI
    - Open Power BI Desktop
    - Create new Snowflake connection using DirectQuery mode
    - Configure connection to GOLD database
    - Authenticate with service account credentials
    - _Requirements: 10.3, 7.8_
  
  - [ ] 14.2 Import Gold layer tables into Power BI
    - Import fct_b2b_sales, fct_logistics, dim_products, dim_sellers, dim_customers
    - Verify DirectQuery mode is active (no data import)
    - _Requirements: 7.8_
  
  - [ ] 14.3 Create relationships in Power BI data model
    - Create relationship: fct_b2b_sales[product_id] → dim_products[product_id]
    - Create relationship: fct_b2b_sales[seller_id] → dim_sellers[seller_id]
    - Create relationship: fct_b2b_sales[customer_id] → dim_customers[customer_id]
    - Create relationship: fct_logistics[customer_id] → dim_customers[customer_id]
    - Create Date table and relate to order_purchase_timestamp
    - _Requirements: 7.8_
  
  - [ ] 14.4 Create DAX measures for Executive Dashboard
    - Create Total Revenue measure: SUM(fct_b2b_sales[total_item_value])
    - Create Total Orders measure: DISTINCTCOUNT(fct_b2b_sales[order_id])
    - Create Average Order Value measure: DIVIDE([Total Revenue], [Total Orders])
    - Create Revenue YoY Growth measure using SAMEPERIODLASTYEAR
    - Add descriptions to all measures
    - _Requirements: 7.1, 7.2, 7.3, 11.7_
  
  - [ ] 14.5 Create DAX measures for Supply Chain Dashboard
    - Create Delivery Accuracy % measure: (on_time_deliveries / total_deliveries) * 100
    - Create Average Handling Time measure: AVERAGE(fct_logistics[handling_time_days])
    - Create Average Shipping Cost measure: AVERAGE(fct_logistics[total_freight_value])
    - Create Late Deliveries measure: COUNT where is_on_time_delivery = 0
    - Add descriptions to all measures
    - _Requirements: 8.1, 8.2, 8.3, 8.8, 11.7_
  
  - [ ] 14.6 Create DAX measures for Vendor Performance Dashboard
    - Create Seller SLA Compliance % measure
    - Create Average Customer Satisfaction measure: AVERAGE(dim_sellers[avg_rating])
    - Add descriptions to all measures
    - _Requirements: 9.2, 9.3, 11.7_

- [ ] 15. Build Executive Sales Overview Dashboard
  - [ ] 15.1 Create dashboard page and add KPI cards
    - Create new report page named "Executive Sales Overview"
    - Add KPI card for Total Revenue
    - Add KPI card for Total Orders
    - Add KPI card for Average Order Value
    - Add KPI card for Revenue YoY Growth
    - _Requirements: 7.1, 7.2, 7.3_
  
  - [ ] 15.2 Add revenue trend and geographic visualizations
    - Add line chart showing revenue trends over time (by month)
    - Add map visualization showing revenue by customer state
    - _Requirements: 7.4, 7.5_
  
  - [ ] 15.3 Add category and product performance visualizations
    - Add bar chart showing revenue by product category
    - Add table showing top 10 products by revenue
    - _Requirements: 7.6, 7.7_
  
  - [ ] 15.4 Configure filters and interactivity
    - Add date range slicer
    - Add product category slicer
    - Verify cross-filtering works across all visuals
    - _Requirements: 7.9_

- [ ] 16. Build Supply Chain War Room Dashboard
  - [ ] 16.1 Create dashboard page and add KPI cards
    - Create new report page named "Supply Chain War Room"
    - Add KPI card for Delivery Accuracy %
    - Add KPI card for Average Handling Time
    - Add KPI card for Average Shipping Cost
    - _Requirements: 8.1, 8.2, 8.3_
  
  - [ ] 16.2 Add delivery performance visualizations
    - Add histogram showing distribution of delivery times
    - Add scatter plot showing handling time vs shipping cost
    - Add line chart showing delivery accuracy trends over time
    - _Requirements: 8.4, 8.5, 8.7_
  
  - [ ] 16.3 Add late delivery analysis
    - Add table showing orders with late deliveries (order_id, customer, days late)
    - Configure drill-through page for order details
    - _Requirements: 8.6, 8.9_

- [ ] 17. Build B2B Vendor Performance Dashboard
  - [ ] 17.1 Create dashboard page and add KPI cards
    - Create new report page named "B2B Vendor Performance"
    - Add KPI card for Total Sellers
    - Add KPI card for Average SLA Compliance %
    - Add KPI card for Average Customer Satisfaction
    - _Requirements: 9.2, 9.3_
  
  - [ ] 17.2 Add seller performance visualizations
    - Add table showing seller leaderboard (ranked by total revenue)
    - Add bar chart showing seller performance by category
    - Add scatter plot showing seller revenue vs customer rating
    - _Requirements: 9.1, 9.4, 9.5_
  
  - [ ] 17.3 Add SLA violation analysis
    - Add table showing sellers with SLA violations
    - Add seller filter to enable drill-down
    - _Requirements: 9.6, 9.8_

- [ ] 18. Final checkpoint - End-to-end validation
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 19. Create project documentation and README
  - [ ] 19.1 Create main project README
    - Document project overview and architecture
    - Document technology stack (Python, Snowflake, dbt, Power BI)
    - Document Medallion architecture (Bronze, Silver, Gold layers)
    - Include architecture diagram
    - _Requirements: 11.6_
  
  - [ ] 19.2 Document setup and execution instructions
    - Document Python environment setup
    - Document Snowflake configuration
    - Document dbt setup and execution
    - Document Power BI connection setup
    - Include troubleshooting section
    - _Requirements: 11.6_
  
  - [ ] 19.3 Document data model and relationships
    - Document all 9 source CSV files and their schemas
    - Document Bronze, Silver, and Gold layer schemas
    - Document star schema relationships
    - Include entity-relationship diagram
    - _Requirements: 11.6_

## Notes

- Tasks marked with `*` are optional property-based tests and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation at key milestones
- Property tests validate universal correctness properties using hypothesis for Python and dbt tests for SQL
- Unit tests validate specific examples and edge cases
- Python implementation uses Python 3.9+ with modern data engineering libraries
- dbt implementation uses dbt Core 1.5+ with dbt-snowflake adapter
- Power BI implementation uses DirectQuery for real-time data access
