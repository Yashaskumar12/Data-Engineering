
# Setting Up dbt Cloud with Databricks

Since we are using **Databricks** as our warehouse, follow these steps to connect dbt Cloud.

## 1. Configure dbt Cloud Project
1. Log in to [dbt Cloud](https://cloud.getdbt.com/).
2. Create new project: `Olist Analytics`.
3. **Choose Connection**: Select **Databricks**.
4. **Settings**:
   * **Server Hostname**: `community.cloud.databricks.com`
   * **HTTP Path**: (Copy from Compute -> JDBC/ODBC tab).
   * **Catalog**: `hive_metastore` (Default for Community Edition).
   * **Schema**: `default` (or whatever you created).
   * **Token**: Your Personal Access Token.
5. **Test Connection**: Ensure it passes.

## 2. Connect GitHub
1. Connect to the GitHub repository: `Yashaskumar12/Data-Engineering`.

## 3. Updates for Databricks Syntax
Databricks uses Spark SQL syntax (mostly standard ANSI SQL).

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
    # Config for Databricks
    staging:
      materialized: view
      schema: default # Stages usually in same schema or separate
    marts:
      materialized: table
      schema: default
```

**Update `models/staging/sources.yml`:**
```yaml
version: 2

sources:
  - name: olist
    database: hive_metastore    # <--- Catalog
    schema: default             # <--- Schema
    tables:
      - name: bronze_orders
      # ... other tables ...
```
