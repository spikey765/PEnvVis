# Streamlit Frontend (app.py)

import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(page_title='Pakistan Environmental Issues', layout='wide')

st.title('Pakistan Environmental Issues Dashboard')

# Fetch data from Flask backend
response = requests.get('http://127.0.0.1:5000/api/air_pollution')
data = response.json()
df = pd.DataFrame(data)

st.subheader('Air Pollution Data per City')

# Dropdown to select city
city = st.selectbox('Select a City:', df['city'].unique())
filtered_df = df[df['city'] == city]

# Line chart for air pollution trends
fig = px.line(filtered_df, x='year', y='pm2.5', title=f'PM2.5 Levels in {city}')
st.plotly_chart(fig)
