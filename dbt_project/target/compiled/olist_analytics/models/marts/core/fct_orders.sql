with orders as (
    select * from "olist"."main_staging"."stg_orders"
),

order_items as (
    select * from "olist"."main_staging"."stg_order_items"
),

order_payments as (
    select * from "olist"."main_staging"."stg_order_payments"
),

-- Aggregating items per order
order_items_agg as (
    select
        order_id,
        count(order_item_id) as total_items,
        sum(price) as total_item_value,
        sum(freight_value) as total_freight_value
    from order_items
    group by 1
),

-- Aggregating payments per order
order_payments_agg as (
    select
        order_id,
        sum(payment_value) as total_payment_value,
        string_agg(distinct payment_type, ', ') as payment_types
    from order_payments
    group by 1
),

final as (
    select
        o.order_id,
        o.customer_id,
        o.order_status,
        o.order_purchase_at,
        o.order_approved_at,
        o.order_delivered_carrier_at,
        o.order_delivered_customer_at,
        o.order_estimated_delivery_at,
        
        -- Metrics from items
        coalesce(i.total_items, 0) as number_of_items,
        coalesce(i.total_item_value, 0) as item_value,
        coalesce(i.total_freight_value, 0) as freight_value,
        
        -- Metrics from payments
        coalesce(p.total_payment_value, 0) as total_amount,
        p.payment_types,
        
        -- Calculated fields
        (o.order_delivered_customer_at - o.order_purchase_at) as delivery_time_interval,
        case 
            when o.order_delivered_customer_at > o.order_estimated_delivery_at then true 
            else false 
        end as is_delayed
        
    from orders o
    left join order_items_agg i on o.order_id = i.order_id
    left join order_payments_agg p on o.order_id = p.order_id
)

select * from final