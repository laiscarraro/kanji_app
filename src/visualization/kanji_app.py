import streamlit as st

from pages import home

st.set_page_config(layout="wide")

tabs = st.tabs(['Home'])

with tabs[0]:
    home.render_page()