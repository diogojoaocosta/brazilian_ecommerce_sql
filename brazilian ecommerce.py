# %%
# **Brazilian e-commerce**
# This notebook will be used to practice SQL commands, using the sqldf function from the pandasql package.  
# The schema of the data can be found at https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce/data

# %%
import pandas as pd
import numpy as np
from pandasql import sqldf
import matplotlib.pyplot as plt

# %%
customers = pd.read_csv("olist_customers_dataset.csv")
geolocation = pd.read_csv("olist_geolocation_dataset.csv")
order_items = pd.read_csv("olist_order_items_dataset.csv")
order_payments = pd.read_csv("olist_order_payments_dataset.csv")
order_reviews = pd.read_csv("olist_order_reviews_dataset.csv")
orders = pd.read_csv("olist_orders_dataset.csv")
products = pd.read_csv("olist_products_dataset.csv")
sellers = pd.read_csv("olist_sellers_dataset.csv")

# %%
orders.head(5)

# %%
# Check how many order status there are
order_status = sqldf(
    """
    SELECT order_status, COUNT(DISTINCT order_id) AS nr_orders 
    FROM orders 
    GROUP BY order_status 
    ORDER BY COUNT(DISTINCT order_id) DESC
    """)
order_status

# %%
# Plot how many orders there have been per year
orders['order_purchase_datetime'] = pd.to_datetime(orders['order_purchase_timestamp'])
orders['order_purchase_date'] = orders['order_purchase_datetime'].dt.date
orders['order_purchase_year'] = orders['order_purchase_datetime'].dt.year
yearly_orders = sqldf(
    """
    SELECT order_purchase_year as Year, COUNT(DISTINCT order_id) as Orders
    FROM orders
    GROUP BY order_purchase_year
    ORDER BY order_purchase_year
    """)
yearly_orders['Year'] = yearly_orders['Year'].astype(int)

plt.figure(figsize=(10, 5))
bars = plt.bar(yearly_orders['Year'], yearly_orders['Orders'], color='skyblue')

for bar in bars:
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2, 
        height, 
        f'{height}', 
        ha='center', 
        va='bottom', 
        fontsize=10
    )

plt.title('Yearly Orders', fontsize=16)
plt.xlabel('Year', fontsize=14)
plt.ylabel('Number of Orders', fontsize=14)
plt.xticks(yearly_orders['Year'], fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()
plt.show()

# %%
# Q.: Are there records that are not common in both tables: orders & order_items?
check_orders_product_detail = sqldf(
    """
    SELECT SUM(CASE WHEN O.order_id IS NULL OR OI.order_id IS NULL THEN 1 ELSE 0 END) AS null_count
    FROM orders O
        FULL JOIN order_items OI ON O.order_id = OI.order_id
    """)
print(check_orders_product_detail)
# There are 775 records that only exist on the orders or order_items table