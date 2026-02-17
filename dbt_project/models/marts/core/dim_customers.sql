
with customers as (
    select * from {{ ref('stg_customers') }}
),

geolocation as (
    select * from {{ ref('stg_geolocation') }}
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
