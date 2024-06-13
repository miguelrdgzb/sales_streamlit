import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

class Visualizations:
    @staticmethod
    def show_category_sales(df):
        category_df = df.groupby(by=['Category'], as_index=False)['Sales'].sum()
        st.subheader('Ventas por categoría')
        fig = px.bar(category_df, x='Category', y='Sales', text=['${:,.2f}'.format(x) for x in category_df['Sales']], 
                     template='seaborn')
        st.plotly_chart(fig, use_container_width=True)

    @staticmethod
    def show_region_sales(df):
        st.subheader('Ventas por Región')
        fig = px.pie(df, values='Sales', names='Region', hole=0.5)
        fig.update_traces(text=df['Region'], textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

    @staticmethod
    def show_time_series_analysis(df):
        df['month_year'] = df['Order Date'].dt.to_period('M')
        st.subheader('Análisis Time Series')
        linechart = pd.DataFrame(df.groupby(df['month_year'].dt.strftime('%Y : %b'))['Sales'].sum()).reset_index()
        fig = px.line(linechart, x='month_year', y='Sales', labels={'Sales': 'Amount'}, height=500, width=1000, template='gridon')
        st.plotly_chart(fig, use_container_width=True)
        with st.expander('Ver datos de TimeSeries:'):
            st.write(linechart.T.style.background_gradient(cmap='Blues'))
            csv = linechart.to_csv(index=False).encode('utf-8')
            st.download_button('Descargar datos', data=csv, file_name='Timeseriesanalisis.csv', mime='text/csv')

    @staticmethod
    def show_treemap(df):
        st.subheader('Vista jerárquica de ventas en Tree map')
        fig = px.treemap(df, path=['Region', 'Category', 'Sub-Category'], values='Sales', hover_data=['Sales'],
                         color='Sub-Category')
        fig.update_layout(width=800, height=650)
        st.plotly_chart(fig, use_container_width=True)

    @staticmethod
    def show_sales_segmentation(df):
        st.subheader('Segmentación de ventas')
        fig = px.pie(df, values='Sales', names='Segment', template='gridon')
        fig.update_traces(text=df['Segment'], textposition='inside')
        st.plotly_chart(fig, use_container_width=True)

    @staticmethod
    def show_category_pie(df):
        st.subheader('Ventas por categoría')
        fig = px.pie(df, values='Sales', names='Category', template='gridon')
        fig.update_traces(text=df['Category'], textposition='inside')
        st.plotly_chart(fig, use_container_width=True)

    @staticmethod
    def show_monthly_summary(df):
        st.subheader(':point_right: Resumen mensual de ventas')
        with st.expander('Tabla resumen:'):
            df_sample = df[0:5][['Region','State','City','Category','Sales','Profit','Quantity']]
            fig = ff.create_table(df_sample, colorscale='Cividis')
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('Tabla resumen por subcategorías:')
            df['month'] = df['Order Date'].dt.month_name()
            sub_category_year = pd.pivot_table(data=df, values='Sales', index=['Sub-Category'], columns='month')
            st.write(sub_category_year)

    @staticmethod
    def show_scatterplot(df):
        st.subheader('Relación entre ventas y beneficio')
        fig = px.scatter(df, x='Sales', y='Profit', size='Quantity')
        st.plotly_chart(fig, use_container_width=True)
