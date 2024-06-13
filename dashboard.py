import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
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

st.sidebar.header("Elegir filtro: ")

#Región

region = st.sidebar.multiselect("Elegir región", df["Region"].unique())
if not region:
    df2 = df.copy()
else:
    df2 = df[df["Region"].isin(region)]


#Estado

state = st.sidebar.multiselect("Elegir Estado", df2["State"].unique())
if not state:
    df3 = df2.copy()
else:
    df3 = df2[df2["State"].isin(state)]

#Ciudad

city = st.sidebar.multiselect("Elegir Ciudad", df3["City"].unique())


#Filtrado condicional
if not region and not state and not city:
    filtered_df = df
elif not state and not city:
    filtered_df = df[df['Region'].isin(region)]
elif not region and not city:
    filtered_df = df[df['State'].isin(state)]
elif state and city:
    filtered_df = df3[df['State'].isin(state) & df3['City'].isin(city)]
elif region and city:
    filtered_df = df3[df['Region'].isin(region) & df3['City'].isin(city)]
elif region and state:
    filtered_df = df3[df['Region'].isin(region) & df3['State'].isin(state)]
elif city:
    filtered_df = df3[df3['City'].isin(city)]
else:
    filtered_df = df3[df3['Region'].isin(region) & df3['State'].isin(state) & df3['City'].isin(city)]

category_df = filtered_df.groupby(by = ['Category'], as_index=False)['Sales'].sum()

with col1:
    st.subheader('Ventas por categoría')
    fig = px.bar(category_df, x = 'Category', y = 'Sales', text=['${:,.2f}'.format(x) for x in category_df['Sales']], 
                 template='seaborn')
    st.plotly_chart(fig, use_container_width=True, height = 200)

with col2:
    st.subheader('Ventas por Región')
    fig = px.pie(filtered_df, values = 'Sales', names= 'Region', hole=0.5)
    fig.update_traces(text = filtered_df['Region'], textposition= 'outside')
    st.plotly_chart(fig, use_container_width=True)

cl1, cl2 = st.columns(2)
with cl1:
    with st.expander('Ver datos Categorías'):
        st.write(category_df)
        csv = category_df.to_csv(index=False).encode('utf-8')
        st.download_button('Descargar datos', data = csv, file_name='Categorias.csv', mime='text/csv',
                           help = 'Click para descargar datos en csv')
with cl2:
    with st.expander('Ver datos Región'):
        region = filtered_df.groupby(by = 'Region', as_index=False)['Sales'].sum()
        st.write(region)
        csv = category_df.to_csv(index=False).encode('utf-8')
        st.download_button('Descargar datos', data = csv, file_name='Region.csv', mime='text/csv',
                           help = 'Click para descargar datos en csv')



filtered_df['month_year'] = filtered_df['Order Date'].dt.to_period('M')
st.subheader('Análisis Time Series')

linechart = pd.DataFrame(filtered_df.groupby(filtered_df['month_year'].dt.strftime('%Y : %b'))['Sales'].sum()).reset_index()
fig2 = px.line(linechart, x = 'month_year', y='Sales', labels = {'Sales' : 'Amount'},height = 500, width = 1000, template='gridon')
st.plotly_chart(fig2, use_container_width=True)

with st.expander('Ver datos de TimeSeries:'):
    st.write(linechart.T.style.background_gradient(cmap='Blues'))
    csv = linechart.to_csv(index=False).encode('utf-8')
    st.download_button('Descargar datos', data = csv, file_name='Timeseriesanalisis.csv', mime='text/csv')


# Tree MAP

st.subheader('Vista jerárquica de ventas en Tree map')
fig3 = px.treemap(filtered_df, path=['Region', 'Category', 'Sub-Category'], values = 'Sales', hover_data = ['Sales'],
                  color= 'Sub-Category')
fig3.update_layout(width=800, height = 650)
st.plotly_chart(fig3, use_container_width=True)


chart1, chart2 = st.columns((2))

with chart1: 
    st.subheader('Segmentación de ventas')
    fig = px.pie(filtered_df, values = 'Sales', names = 'Segment', template='gridon')
    fig.update_traces(text = filtered_df['Segment'], textposition = 'inside')
    st.plotly_chart(fig, use_container_width=True)

with chart2: 
    st.subheader('Ventas por categoría')
    fig = px.pie(filtered_df, values = 'Sales', names = 'Category', template='gridon')
    fig.update_traces(text = filtered_df['Category'], textposition = 'inside')
    st.plotly_chart(fig, use_container_width=True)

st.subheader(':point_right: Resumen mensual de ventas')
with st.expander('Tabla resumen: '):
    df_sample = df[0:5][['Region','State','City','Category','Sales','Profit','Quantity']]
    fig = ff.create_table(df_sample, colorscale='Cividis')
    st.plotly_chart(fig, use_container_width = True)

    st.markdown('Tabla resumen por subcategorías:')
    filtered_df['month'] = filtered_df['Order Date'].dt.month_name()
    sub_category_year = pd.pivot_table(data = filtered_df, values = 'Sales', index=['Sub-Category'], columns = 'month')
    st.write(sub_category_year)

# Scatterplot

data1 = px.scatter(filtered_df, x= 'Sales', y='Profit', size='Quantity')
data1['layout'].update(title = 'Relación entre ventas y beneficio', titlefont = dict(size=20), 
                       xaxis = dict(title='Sales', titlefont=dict(size=19)),
                       yaxis = dict(title= 'Profit', titlefont = dict(size=19)))

st.plotly_chart(data1, use_container_width=True)

with st.expander('Datos'):
    st.write(filtered_df.iloc[:500,1:20:2])

#Descargar el dataset original
csv = df.to_csv(index=False).encode('utf-8')
st.download_button('Descargar datos orginales', data = csv, file_name='data.csv', mime='text/csv')


