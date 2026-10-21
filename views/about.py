import streamlit as st
st.markdown("**The Cat API** is an excellent resource for learning how to get data from **APIs**.")
st.markdown("**Streamlit** is an open-source **Python** framework that makes Building and deploying powerful data driven apps in minutes.")

st.subheader('Using the cat API')
st.markdown("A key is required to make requests to this API and they offer ") 
st.markdown("Get a free API key at https://thecatapi.com/signup")
st.markdown("Documentation can be found at https://docs.thecatapi.com/docs/intro")

st.subheader('New to Streamlit?')
st.markdown("Getting started with Streamlit https://docs.streamlit.io/get-started")
st.markdown("Documentation can be found at https://docs.thecatapi.com/docs/intro")

st.link_button("A helpful quick reference guide can be found here:", "https://docs.streamlit.io/develop/quick-reference/cheat-sheet  ")
multi = '''Here's an example api call to thecatapi using streamlit.
'''
st.markdown(multi)
code_payload = '''
import json
import requests
import streamlit as st

CAT_API_KEY = "your api key"
base_url = "https://api.thecatapi.com/v1/"
headers = {"x-api-key": CAT_API_KEY} if CAT_API_KEY else {}

url = base_url + "breeds"
response = requests.get(url, headers=headers, timeout=5)
data = response.json()

breed_names = [x["name"] for x in data]
for breed in breed_names:
    st.write(breed)
'''

st.code(code_payload, language="python", line_numbers=True)
st.feedback("thumbs")
st.markdown('''
    :red[Streamlit] :orange[can] :green[write] :blue[text] :violet[in]
    :gray[pretty] :rainbow[colors] and :blue-background[highlight] text.''')