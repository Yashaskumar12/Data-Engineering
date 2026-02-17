



select
    1
from "olist"."main_staging"."stg_order_payments"

where not(payment_value >= 0)

