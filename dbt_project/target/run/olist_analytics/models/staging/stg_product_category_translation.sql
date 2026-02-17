
  
  create view "olist"."main_staging"."stg_product_category_translation__dbt_tmp" as (
    with source as (
    select * from "olist"."main"."bronze_product_category_translation"
),

renamed as (
    select
        product_category_name,
        product_category_name_english
    from source
)

select * from renamed
  );
