
  
    
    

    create  table
      "olist"."main_marts"."dim_customers__dbt_tmp"
  
    as (
      with customers as (
    select * from "olist"."main_staging"."stg_customers"
),

geolocation as (
    select * from "olist"."main_staging"."stg_geolocation"
),

-- We might want to join exact location data later, but for now 
-- a simple dimension table from staging is a good start.
final as (
    select
        customer_id,
        customer_unique_id,
        zip_code,
        city,
        state
    from customers
)

select * from final
    );
  
  