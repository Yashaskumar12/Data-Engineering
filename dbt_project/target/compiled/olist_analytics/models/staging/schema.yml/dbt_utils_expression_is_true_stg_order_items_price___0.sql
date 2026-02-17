



select
    1
from "olist"."main_staging"."stg_order_items"

where not(price >= 0)

