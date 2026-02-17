
# Setting Up dbt Cloud with Snowflake

Since we are using **Snowflake** as our warehouse, follow these steps to connect dbt Cloud.

## 1. Configure dbt Cloud Project
1. Log in to [dbt Cloud](https://cloud.getdbt.com/).
2. Create new project: `Olist Analytics`.
3. **Choose Connection**: Select **Snowflake**.
4. **Settings**:
   * **Account**: The identifier part of your URL (e.g., `xy12345.us-east-1`).
   * **Database**: `OLIST_BRONZE` (Matches what we created in Colab).
   * **Warehouse**: `COMPUTE_WH`.
   * **Role**: `ACCOUNTADMIN` (or custom role if you made one).
   * **Auth**: Username/Password.
5. **Test Connection**: Ensure it passes.

## 2. Connect GitHub
1. Connect to the GitHub repository: `Yashaskumar12/Data-Engineering`.

## 3. Updates for Snowflake Syntax
Snowflake uses slightly different syntax than DuckDB/BigQuery. We need to update `dbt_project.yml` and `sources.yml`.

**Update `dbt_project.yml`:**
```yaml
name: 'olist_analytics'
version: '1.0.0'
config-version: 2

profile: 'olist_project'

model-paths: ["models"]
# ... other paths ...

models:
  olist_analytics:
    # Config for Snowflake
    staging:
      materialized: view
      schema: staging
    marts:
      materialized: table
      schema: marts
```

**Update `models/staging/sources.yml`:**
Update database/schema to match Snowflake uppercasing:
```yaml
version: 2

sources:
  - name: olist
    database: OLIST_BRONZE      # <--- Matches Colab script
    schema: PUBLIC              # Default schema
    tables:
      - name: bronze_orders     # dbt handles case insensitivity usually, but check identifier
      # ... other tables ...
```
