import streamlit as st
import pandas as pd
import plotly.express as px

# ✅ Set page configuration (First command in Streamlit)
st.set_page_config(page_title="Air Passenger Dashboard", layout="wide")

# 🎨 Custom CSS for Background & Airplane Positioning
st.markdown(
    """
    <style>
        /* Gradient Background */
        .stApp {
            background: linear-gradient(to right, #ff66b2, #6600cc); /* Pink & Purple */
            color: white;
        }
        
        /* Text and UI Components */
        h1, h2, h3, h4, h5, h6, .stTextInput, .stSelectbox, .stButton {
            color: white !important;
        }

        /* Airplane Icons Positioned Correctly */
        .airplane-left {
            position: fixed;
            top: 5%;
            left: 2%;
            font-size: 50px;
            transform: rotate(-20deg);
            z-index: 1; /* Keeps it behind charts */
        }
        .airplane-right {
            position: fixed;
            top: 5%;
            right: 2%;
            font-size: 50px;
            transform: rotate(20deg);
            z-index: 1; /* Keeps it behind charts */
        }
        
        /* Adjust Bar Chart Spacing */
        .css-1kyxreq {
            margin-top: 50px !important;
        }
    </style>
    <div class="airplane-left">✈️</div>
    <div class="airplane-right">✈️</div>
    """,
    unsafe_allow_html=True
)

# 📌 Load the dataset (Fixing incorrect file path format)
file_path = "https://raw.githubusercontent.com/Loyallamichael1/Air_Passenger_Dashboard/main/AirP.csv" 

try:
    df = pd.read_csv(file_path)
except Exception as e:
    st.error(f"❌ Error: Unable to load dataset. Check file path or format.\n\n{e}")
    st.stop()

# 📌 Convert 'Month' to datetime format for time series analysis
if 'Month' in df.columns:
    df['Month'] = pd.to_datetime(df['Month'])
    df.set_index('Month', inplace=True)
else:
    st.error("❌ Error: 'Month' column not found in dataset.")
    st.stop()

# 📌 Extract year and month for filtering and insights
df['Year'] = df.index.year
df['Month_Num'] = df.index.month
df['Month_Name'] = df.index.strftime('%B')

# 📌 Sidebar for Filters
with st.sidebar:
    st.title("🔍 Filter Options")
    selected_year = st.selectbox("Select Year:", options=sorted(df['Year'].unique()), index=0)
    selected_month = st.selectbox("Select Month:", options=["All"] + list(df['Month_Name'].unique()), index=0)

# 📌 Filter Data Based on Selections
filtered_df = df[df["Year"] == selected_year]
if selected_month != "All":
    filtered_df = filtered_df[filtered_df["Month_Name"] == selected_month]

# 🎯 One-Row Layout: KPIs + Charts + Data Table
st.title("📊 Air Passenger Dashboard")

# 🔹 **Create three horizontal columns with more space**
kpi_col, chart_col1, chart_col2, data_col = st.columns([1, 2, 2, 2])

# 📌 **Column 1: KPI Metrics**
with kpi_col:
    st.subheader("📌 Key Metrics")
    st.metric("📈 Highest Passengers", filtered_df['#Passengers'].max())
    st.metric("📉 Lowest Passengers", filtered_df['#Passengers'].min())
    st.metric("📊 Average Passengers", round(filtered_df['#Passengers'].mean(), 2))

# 📌 **Column 2: Passenger Trend Chart (Time Series)**
with chart_col1:
    st.subheader("📈 Passenger Trends Over Time")
    fig1 = px.line(filtered_df, x=filtered_df.index, y="#Passengers", markers=True, title="Passenger Trend")
    st.plotly_chart(fig1, use_container_width=True)

# 📌 **Column 3: Yearly Passenger Counts (Bar Chart)**
with chart_col2:
    st.subheader("📊 Yearly Passenger Counts")
    yearly_counts = df.groupby("Year")["#Passengers"].sum().reset_index()
    fig2 = px.bar(yearly_counts, x="Year", y="#Passengers", title="Total Passengers Per Year", text_auto=True)
    st.plotly_chart(fig2, use_container_width=True)

# 📌 **Column 4: Data Table**
with data_col:
    st.subheader("📋 Data Table")
    st.dataframe(filtered_df, height=300)

# 📌 Peak and Lowest Travel Months (Below the Dashboard)
st.subheader("🏆 Best & Worst Travel Months")
best_month = df.groupby("Month_Name")["#Passengers"].mean().idxmax()
worst_month = df.groupby("Month_Name")["#Passengers"].mean().idxmin()
st.write(f"📌 **Busiest Month:** {best_month}")
st.write(f"📌 **Slowest Month:** {worst_month}")

# ✅ **Insights & Explanations**
st.subheader("📌 Insights from the Data")

st.markdown("""
- **Why Line Chart?**  
  - Shows passenger trends over time, making it easy to spot seasonal fluctuations.  
- **Why Bar Chart?**  
  - Clearly represents yearly growth in total passengers.  
- **Why KPIs?**  
  - Gives a quick overview of key stats without needing to interpret a chart.  
- **Why a Table?**  
  - Allows users to see specific values and details based on selected filters.  
""")




