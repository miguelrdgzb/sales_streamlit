import pandas as pd
import streamlit as st

class DataLoader:
    @staticmethod
    def load_data(file):
        if file is not None:
            filename = file.name
            st.write(filename)
            df = pd.read_csv(file, encoding='ISO-8859-1')
        else:
            df = pd.read_excel('resources/SampleSuperStore.xls')
        return df