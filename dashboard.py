import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title='SuperStore', page_icon=':bar_chart:', layout='wide')
st.title(' :bar_chart: SuperStore EDA')

fl = st.file_uploader(':file_folder: Upload a file', type=(['csv','xlsx','txt','xls']))
if fl is not None:
    filename = fl.name
    st.write(filename)
    df = pd.read_csv(filename, encoding= 'ISO-8859-1')

else:
    df = pd.read_excel('resources/SampleSuperStore.xls')


col1, col2 = st.columns((2))
df['Order Date'] = pd.to_datetime(df['Order Date'])

# Conseguir la minima y maxima fecha

startDate = pd.to_datetime(df['Order Date']).min()
endDate = pd.to_datetime(df['Order Date']).max()

with col1:
    date1 = pd.to_datetime(st.date_input('Start Date', startDate))

with col2:
    date2 = pd.to_datetime(st.date_input('End Date', endDate))

df = df[(df['Order Date'] >= date1) & (df['Order Date'] <= date2)].copy()

## 15.05