import streamlit as st
from data_loader import DataLoader
from filters import Filters
from visualizations import Visualizations

st.set_page_config(page_title='SuperStore', page_icon=':bar_chart:', layout='wide')
st.title(':bar_chart: SuperStore EDA')

def main():
    fl = st.file_uploader(':file_folder: Upload a file', type=(['csv', 'xlsx', 'txt', 'xls']))
    df = DataLoader.load_data(fl)

    filters = Filters(df)
    filters.apply_date_filter()
    filtered_df = filters.apply_sidebar_filters()

    col1, col2 = st.columns((2))
    with col1:
        Visualizations.show_category_sales(filtered_df)
    with col2:
        Visualizations.show_region_sales(filtered_df)

    Visualizations.show_time_series_analysis(filtered_df)
    Visualizations.show_treemap(filtered_df)

    chart1, chart2 = st.columns((2))
    with chart1:
        Visualizations.show_sales_segmentation(filtered_df)
    with chart2:
        Visualizations.show_category_pie(filtered_df)

    Visualizations.show_monthly_summary(filtered_df)
    Visualizations.show_scatterplot(filtered_df)

    # Descargar el dataset original
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button('Descargar datos originales', data=csv, file_name='data.csv', mime='text/csv')

if __name__ == '__main__':
    main()
