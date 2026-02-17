
# Setting Up dbt Cloud with BigQuery

Since we are using **Google BigQuery** as our warehouse, follow these steps to connect dbt Cloud.

## 1. Create Service Account (in Google Cloud Console)
1. Go to **IAM & Admin** > **Service Accounts**.
2. Click **Create Service Account**.
   * Name: `dbt-cloud-user`
3. **Grant Access**:
   * Role: `BigQuery Data Editor`
   * Role: `BigQuery User`
4. **Create Key**:
   * Click the new service account > **Keys** tab.
   * **Add Key** > **Create new key** > **JSON**.
   * This will download a `.json` file. **KEEP THIS SAFE!**

## 2. Configure dbt Cloud Project
1. Log in to [dbt Cloud](https://cloud.getdbt.com/).
2. Create new project.
3. **Choose Connection**: Select **BigQuery**.
4. **Settings**:
   * **Upload JSON Key**: Upload the file you downloaded in Step 1.
   * **Dataset**: `dbt_production` (dbt will create this).
   * **Location**: `US` (Must match where you loaded data in Colab).
5. **Test Connection**: Ensure it passes.

## 3. Connect GitHub
1. Connect to the GitHub repository you pushed earlier (`olist-dbt-analytics`).

## 4. Updates for BigQuery Syntax
Since we were using DuckDB locally, we need to make 2 small changes to `dbt_project.yml` in dbt Cloud IDE:

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
    # Config for BigQuery
    staging:
      materialized: view
      schema: staging
    marts:
      materialized: table
      schema: marts
```

**Update `models/staging/sources.yml`:**
In dbt Cloud IDE, update the database field:
```yaml
version: 2

sources:
  - name: olist
    database: YOUR_PROJECT_ID  # <--- Update this!
    schema: olist_bronze       # Matches the dataset created in Colab
    tables:
      - name: bronze_orders
      # ... other tables ...
```
