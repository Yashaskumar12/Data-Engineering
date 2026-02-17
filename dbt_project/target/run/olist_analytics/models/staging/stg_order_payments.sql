
  
  create view "olist"."main_staging"."stg_order_payments__dbt_tmp" as (
    with source as (
    select * from "olist"."main"."bronze_order_payments"
),

renamed as (
    select
        order_id,
        payment_sequential,
        payment_type,
        payment_installments,
        payment_value
    from source
)

select * from renamed
  );
