import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(page_title="DASHBOARD: Sales Report", 
                   page_icon=":chart_with_upwards_trend:", layout="wide")
st.title("📈 DASHBOARD: Sales Report")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)


column1, column2 = st.columns((2))
df = None  

with column1:
    uploaded_file = st.file_uploader("Upload a File", type=["csv", "xlsx", "xls"])
    if uploaded_file:
        filename = uploaded_file.name
        st.write(f"Uploaded file: {filename}")
        file_extension = filename.split('.')[-1]
        
        try:
            if file_extension == 'csv':
                df = pd.read_csv(uploaded_file)
            elif file_extension in ['xls', 'xlsx']:
                df = pd.read_excel(uploaded_file)
            else:
                st.error(f"Unsupported file format: {file_extension}")
        except Exception as e:
            st.error(f"Error loading file: {e}")


if df is not None and not df.empty:
    
 
    state_mapping = {
        'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA',
        'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA',
        'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA',
        'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
        'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS', 'Missouri': 'MO',
        'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ',
        'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH',
        'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC',
        'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT',
        'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'
    }
    df['State_code'] = df['State'].map(state_mapping)

   
    date_columns = [col for col in df.columns if pd.api.types.is_datetime64_any_dtype(df[col])]
    if date_columns:
        range_column = st.sidebar.selectbox("Select Date Column:", date_columns)
        df[range_column] = pd.to_datetime(df[range_column])
        start_date, end_date = df[range_column].min(), df[range_column].max()

        with column2:
            start = pd.to_datetime(st.date_input("Start Date", start_date))
            end = pd.to_datetime(st.date_input("End Date", end_date))

        df = df[(df[range_column] >= start) & (df[range_column] <= end)].copy()

  
    st.sidebar.header("Select Columns:")
    selected_columns = st.sidebar.multiselect("Select columns to filter by:", df.columns, max_selections=4)

    filtered_df = df.copy()
    for col in selected_columns:
        selected_values = st.sidebar.multiselect(f"Filter {col}:", df[col].unique())
        if selected_values:
            filtered_df = filtered_df[filtered_df[col].isin(selected_values)]

 
    sales_category = filtered_df.groupby(by=['Category'], as_index=False)["Sales"].sum()

    with column1:
        fig = px.bar(sales_category, x="Category", y="Sales", template="seaborn", title="Category-wise Sales")
        st.plotly_chart(fig, use_container_width=True)

    with column2:
        fig = px.pie(filtered_df, values="Sales", names="Region", hole=0.5, title="Region-wise Sales")
        st.plotly_chart(fig, use_container_width=True)


    aggregate_sales_state = filtered_df.groupby('State_code').agg({
        'Sales': 'sum',
        'Quantity': 'sum',
        'Profit': 'sum'
    }).round().reset_index()

    with column2:
        fig = px.choropleth(aggregate_sales_state, 
                            locations='State_code',
                            locationmode="USA-states",
                            color='Sales',
                            scope='usa',
                            hover_data=['Sales', 'Quantity', 'Profit'],
                            title='Sales by Filtered States')
        st.plotly_chart(fig, use_container_width=True)

    
    profit_category = filtered_df.groupby(by=['Category'], as_index=False)["Profit"].sum()
    with column1:
        fig = px.bar(profit_category, x="Category", y="Profit", template="seaborn", title="Category-wise Profit")
        st.plotly_chart(fig, use_container_width=True)

 
    sales_segment = filtered_df.groupby(by=['Segment'], as_index=False)["Sales"].sum()
    with column1:
        fig = px.pie(filtered_df, values="Sales", names="Segment", hole=0.5, title="Segment-wise Sales")
        st.plotly_chart(fig, use_container_width=True)

    
    profit_segment = filtered_df.groupby(by=['Segment'], as_index=False)["Profit"].sum()
    with column2:
        fig = px.bar(profit_segment, x="Segment", y="Profit", template="seaborn", title="Segment-wise Profit")
        st.plotly_chart(fig, use_container_width=True)


    fig = px.scatter(filtered_df, x="Sales", y="Profit", size="Quantity", title="Sales vs. Profit (Filtered Data)")
    st.plotly_chart(fig, use_container_width=True)

    fig = px.scatter(df, x="Sales", y="Profit", size="Quantity", title="Sales vs. Profit (Entire Dataset)")
    st.plotly_chart(fig, use_container_width=True)

   
    aggregate = df.groupby('State_code').agg({
        'Sales': 'sum',
        'Quantity': 'sum',
        'Profit': 'sum'
    }).round().reset_index()

    fig = px.choropleth(aggregate, 
                        locations='State_code',
                        locationmode="USA-states",
                        color='Sales',
                        scope='usa',
                        hover_data=['Sales', 'Quantity', 'Profit'],
                        title='Summary Report by State')
    st.plotly_chart(fig, use_container_width=True)


    st.header("Filtered DataFrame:")
    st.write(filtered_df)

else:
    st.warning("Please upload a valid CSV/XLSX file.")
