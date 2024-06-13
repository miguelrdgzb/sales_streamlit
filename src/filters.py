import pandas as pd
import streamlit as st

class Filters:
    def __init__(self, df):
        self.df = df
        self.filtered_df = df

    def apply_date_filter(self):
        self.df['Order Date'] = pd.to_datetime(self.df['Order Date'])
        startDate = self.df['Order Date'].min()
        endDate = self.df['Order Date'].max()
        
        col1, col2 = st.columns((2))
        with col1:
            date1 = pd.to_datetime(st.date_input('Start Date', startDate))
        with col2:
            date2 = pd.to_datetime(st.date_input('End Date', endDate))

        self.filtered_df = self.df[(self.df['Order Date'] >= date1) & (self.df['Order Date'] <= date2)].copy()

    def apply_sidebar_filters(self):
        st.sidebar.header("Elegir filtro: ")

        # Región
        region = st.sidebar.multiselect("Elegir región", self.filtered_df["Region"].unique())
        if region:
            self.filtered_df = self.filtered_df[self.filtered_df["Region"].isin(region)]

        # Estado
        state = st.sidebar.multiselect("Elegir Estado", self.filtered_df["State"].unique())
        if state:
            self.filtered_df = self.filtered_df[self.filtered_df["State"].isin(state)]

        # Ciudad
        city = st.sidebar.multiselect("Elegir Ciudad", self.filtered_df["City"].unique())
        if city:
            self.filtered_df = self.filtered_df[self.filtered_df["City"].isin(city)]

        return self.filtered_df