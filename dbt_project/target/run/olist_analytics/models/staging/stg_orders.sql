
  
  create view "olist"."main_staging"."stg_orders__dbt_tmp" as (
    with source as (
    select * from "olist"."main"."bronze_orders"
),

renamed as (
    select
        order_id,
        customer_id,
        order_status,
        order_purchase_timestamp as order_purchase_at,
        order_approved_at,
        order_delivered_carrier_date as order_delivered_carrier_at,
        order_delivered_customer_date as order_delivered_customer_at,
        order_estimated_delivery_date as order_estimated_delivery_at
    from source
)

select * from renamed
  );
