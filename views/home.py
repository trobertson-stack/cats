import streamlit as st
import requests, json

st.set_page_config(layout="wide", page_title="Cats")
st.title("🐱 Welcome Cat Lovers🐱")
data = requests.get('https://api.thecatapi.com/v1/images/search?limit=2')
col1, col2 = st.columns(2)
with col1:
    cd = data.json()[0]
    st.image(cd['url'], width=300)
with col2:
    cd = data.json()[1]
    st.image(cd['url'], width=300)

st.snow()