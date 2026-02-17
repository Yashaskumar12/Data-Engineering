
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  



select
    1
from "olist"."main_marts"."fct_orders"

where not(item_value >= 0)


  
  
      
    ) dbt_internal_test