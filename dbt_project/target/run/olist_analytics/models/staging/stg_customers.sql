
  
  create view "olist"."main_staging"."stg_customers__dbt_tmp" as (
    with source as (
    select * from "olist"."main"."bronze_customers"
),

renamed as (
    select
        customer_id,
        customer_unique_id,
        customer_zip_code_prefix as zip_code,
        customer_city as city,
        customer_state as state
    from source
)

select * from renamed
  );
