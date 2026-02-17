
  
  create view "olist"."main_staging"."stg_geolocation__dbt_tmp" as (
    with source as (
    select * from "olist"."main"."bronze_geolocation"
),

renamed as (
    select
        geolocation_zip_code_prefix as zip_code,
        geolocation_lat as latitude,
        geolocation_lng as longitude,
        geolocation_city as city,
        geolocation_state as state
    from source
)

select * from renamed
  );
