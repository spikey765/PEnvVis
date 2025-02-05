# Streamlit Frontend (app.py)

import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(page_title='Pakistan Environmental Issues', layout='wide')

st.title('Pakistan Environmental Issues Dashboard')

st.markdown("""
    <style>
        .main {background-color: #f0f2f6;}
        h1 {color: #1f4e79; text-align: center;}
    </style>
    """, unsafe_allow_html=True)

st.title('🌍 Pakistan Environmental Issues Dashboard')

# Fetch data from Flask backend
# Function to fetch data from the Flask backend
def fetch_data(endpoint):
    try:
        response = requests.get(f'http://127.0.0.1:5000/api/{endpoint}')
        response.raise_for_status()
        return pd.DataFrame(response.json())
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching {endpoint} data: {e}")
        return pd.DataFrame()

# Fetch datasets
df_pollution = fetch_data('air_pollution')
df_farming = fetch_data('farming')

# Sidebar for dataset selection
st.sidebar.title("Select Dataset")
option = st.sidebar.radio("Choose an environmental issue:", ("Air Pollution", "Farming"))

if option == "Air Pollution" and not df_pollution.empty:
    st.subheader('Air Pollution Data per City')
    
    # Add a slider for selecting the year range
    min_year = int(df_pollution['year'].min())
    max_year = int(df_pollution['year'].max())
    year_range = st.slider("Select Year Range", min_year, max_year, (min_year, max_year), step=1)
    
    # Dropdown to select a city
    city = st.selectbox('Select a City:', df_pollution['city'].unique())
    
    # Filter data based on selected city and year range
    filtered_df = df_pollution[
        (df_pollution['city'] == city) &
        (df_pollution['year'] >= year_range[0]) &
        (df_pollution['year'] <= year_range[1])
    ]
    
    if not filtered_df.empty:
        fig = px.line(filtered_df, x='year', y='pm2.5', title=f'PM2.5 Levels in {city}', markers=True)
        st.plotly_chart(fig)
    else:
        st.write("No data available for the selected city and time range.")

elif option == "Farming" and not df_farming.empty:
    st.subheader('Farming Data Trends')
    
    # Slider for selecting the year range for farming data
    min_year = int(df_farming['year'].min())
    max_year = int(df_farming['year'].max())
    year_range = st.slider("Select Year Range", min_year, max_year, (min_year, max_year), step=1)
    
    # Dropdown to select a crop
    crop = st.selectbox('Select a Crop:', df_farming['crop'].unique())
    
    # Filter data based on selected crop and year range
    filtered_df = df_farming[
        (df_farming['crop'] == crop) &
        (df_farming['year'] >= year_range[0]) &
        (df_farming['year'] <= year_range[1])
    ]
    
    if not filtered_df.empty:
        fig = px.line(filtered_df, x='year', y='production', title=f'Production of {crop}', markers=True)
        st.plotly_chart(fig)
    else:
        st.write("No data available for the selected crop and time range.")
