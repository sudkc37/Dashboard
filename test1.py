import streamlit as st
import pandas as pd
import plotly.express as px
import pyodbc
import time

# Set page config
st.set_page_config(page_title="Dashboard", layout="wide")

st.markdown(
    """
    <style>
        /* Remove top padding and margin */
        .title {
            text-align: center;
            margin-top: -60px; /* Adjust this value if needed */
        }
        
        /* Remove default padding from Streamlit */
        [data-testid="stAppViewContainer"] {
            padding-top: 0px;
        }
    </style>
    """,
    unsafe_allow_html=True
)



st.markdown("<h1 class='title'>Pizzza House Dashboard</h1>", unsafe_allow_html=True)


# Connect to SQL Server running in Docker
@st.cache_data(ttl=60)  # Cache data for 60 seconds
def get_city_data():
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost,1433;"
        "DATABASE=Resturant;"
        "UID=SA;"
        "PWD=YourStrongPassw0rd"
    )
    query = """
        SELECT delivery_city, COUNT(*) AS city_count
        FROM [Resturant].[dbo].[city_addresses]
        GROUP BY delivery_city
        ORDER BY city_count DESC;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

@st.cache_data(ttl=60)
def get_food_data():
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost,1433;"
        "DATABASE=Resturant;"
        "UID=SA;"
        "PWD=YourStrongPassw0rd"
    )
    query = """
        SELECT item_name, SUM(o.quantity) AS total_sold
        FROM [Resturant].[dbo].[order] o
        JOIN [Resturant].[dbo].[iteam-2] i ON o.item_id = i.item_id
        GROUP BY i.item_name
        ORDER BY total_sold DESC;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df


def get_delivery_data():
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost,1433;"
        "DATABASE=Resturant;"
        "UID=SA;"
        "PWD=YourStrongPassw0rd"
    )
    query = """
        select delivery_city, sum([Resturant].[dbo].[order].quantity * [Resturant].[dbo].[iteam-2].price) as total_revenue, COUNT([Resturant].[dbo].[order].add_id) AS delivery_count
        from [Resturant].[dbo].[order] 
        join [Resturant].[dbo].[iteam-2] on [Resturant].[dbo].[order].item_id = [Resturant].[dbo].[iteam-2].item_id
        join [Resturant].[dbo].[city_addresses] on [Resturant].[dbo].[order].cust_id = [Resturant].[dbo].[city_addresses].add_id
        where [Resturant].[dbo].[order].delivery = 1
        group by [Resturant].[dbo].[city_addresses].delivery_city;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def get_average():
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost,1433;"
        "DATABASE=Resturant;"
        "UID=SA;"
        "PWD=YourStrongPassw0rd"
    )
    query = """
        select avg([Resturant].[dbo].[order].quantity * [Resturant].[dbo].[iteam-2].price) as average_order_value
        from [Resturant].[dbo].[order]
        join [Resturant].[dbo].[iteam-2] on [Resturant].[dbo].[order].[item_id] = [Resturant].[dbo].[iteam-2].[item_id]
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df['average_order_value'].sum()

def get_totalRevenue():
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost,1433;"
        "DATABASE=Resturant;"
        "UID=SA;"
        "PWD=YourStrongPassw0rd"
    )
    query = """
        select [Resturant].[dbo].[order].quantity * [Resturant].[dbo].[iteam-2].price as average_order_value
        from [Resturant].[dbo].[order]
        join [Resturant].[dbo].[iteam-2] on [Resturant].[dbo].[order].[item_id] = [Resturant].[dbo].[iteam-2].[item_id]
         """
    df = pd.read_sql(query, conn)
    conn.close()
    return df['average_order_value'].sum()

def get_totalcustomer():
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost,1433;"
        "DATABASE=Resturant;"
        "UID=SA;"
        "PWD=YourStrongPassw0rd"
    )
    query = """
        select count(*) as customer_count
        from [Resturant].[dbo].[customers]
         """
    df = pd.read_sql(query, conn)
    conn.close()
    return df['customer_count'].sum()

def get_sales_per_day():
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost,1433;"
        "DATABASE=Resturant;"
        "UID=SA;"
        "PWD=YourStrongPassw0rd"
    )
    query = """
    SELECT 
    CONVERT(date, [Resturant].[dbo].[order].created_at) AS order_date,
    SUM([Resturant].[dbo].[order].quantity * [Resturant].[dbo].[iteam-2].price) AS sales
    FROM 
    [Resturant].[dbo].[order]
    JOIN [Resturant].[dbo].[iteam-2] ON [Resturant].[dbo].[order].[item_id] = [Resturant].[dbo].[iteam-2].[item_id]
    GROUP BY CONVERT(date, [Resturant].[dbo].[order].created_at)
    ORDER BY order_date;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

st.cache_data(ttl=60)  # Cache data for 60 seconds
def get_rating_data():
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost,1433;"
        "DATABASE=Resturant;"
        "UID=SA;"
        "PWD=YourStrongPassw0rd"
    )
    query = """
        select DATEPART(year, created_at) as year,
        DATEPART(week, created_at)  as week,
        avg(case when rating > 0 then rating end) as avg_rating
        from [Resturant].[dbo].[review]
        where rating > 0
        group by DATEPART(year, created_at), DATEPART(week, created_at)
        order by year, week;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Fetch data
df_city = get_city_data()
df_food = get_food_data()
df_delivery = get_delivery_data()
df_average = get_average()
df_totalRevenue = get_totalRevenue()
df_totalcustomer = get_totalcustomer()
df_daily_sales = get_sales_per_day()
df_rating = get_rating_data()

print(df_totalRevenue)
col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1:
    st.metric("Total Revenue", f"${df_totalRevenue}")  

with col2:
    st.metric("Total Delivery Orders", f"{df_delivery['delivery_count'].sum():,.0f}")

with col3:
    st.metric("Total Customers", f"{df_totalcustomer}")

with col4:
    st.metric("Average Per Ticket", f"${df_average:,.02f}")

with col5:
    st.metric("Gross Margin", f"{((df_totalRevenue - (0.733*df_totalRevenue))/df_totalRevenue)*100:,.02f}%")

with col6:
    st.metric("Net Profit", f"{((df_totalRevenue - (0.862*df_totalRevenue))/df_totalRevenue)*100:,.02f}%")

    
# Split into two columns
col1, col2 = st.columns(2)
with col1:
    fig_city = px.bar(df_city, x="delivery_city", y="city_count", title="Number of Customers by City", template="seaborn")
    fig_city.update_layout(title_x=0.4)
    st.plotly_chart(fig_city, use_container_width=True)
    
# Plot Food Category Sales
with col2:
    #fig_food = px.bar(df_food, x="item_name", y="total_sold", title="Total Sold Items by Food Category", template="seaborn")
    #st.plotly_chart(fig_food, use_container_width=True)
    fig_food = px.pie(df_food, values="total_sold", names="item_name", title="Total Sold Items by Food Category", template="seaborn")
    fig_food.update_layout(title_x=0.4, width=300)
    st.plotly_chart(fig_food, use_container_width=True)

col1, col2, col3 = st.columns(3)

with col1:
    fig_city = px.bar(df_delivery, 
                      x="delivery_city", 
                      y=["total_revenue", "delivery_count"], 
                      title="Delivery Orders and Revenue by City", 
                      template="seaborn", 
                      labels={"delivery_city": "City", 
                              "total_revenue": "Total Revenue", 
                              "delivery_count": "Delivery Count"},
                      barmode='group') 
    fig_city.update_layout(title_x=0.3)
    
    st.plotly_chart(fig_city, use_container_width=True)


df_rating["color"] = df_rating["avg_rating"].apply(lambda x: "poor" if x < 5 else "average" if x < 7 else "green")
with col2:
    fig_rating = px.bar(df_rating, x="week", y="avg_rating", title="Average Rating Trends", template="seaborn",
                        color="color", color_discrete_map={"red": "red", "yellow": "yellow", "green": "green"},
                        )
    fig_rating.update_layout(title_x=0.4)
    st.plotly_chart(fig_rating, use_container_width=True)

with col3:
    fig_daily_sales = px.line(df_daily_sales, x="order_date", y="sales", title="Sales Trends", template="seaborn")
    fig_daily_sales.update_layout(title_x=0.4)
    st.plotly_chart(fig_daily_sales, use_container_width=True)



time.sleep(60)
st.rerun()