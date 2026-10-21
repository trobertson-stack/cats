import streamlit as st

home_page = st.Page("views/home.py", title="Home", icon="😸")
cats = st.Page("views/cats.py", title="Cats", icon="🐈")
CatFacts = st.Page("views/CatFacts.py", title="Cat Facts", icon="😻")
about_page = st.Page("views/about.py", title="About", icon="😻")
pg = st.navigation({
    "Overview": [home_page],
    "Cat Pictures and Facts": [cats, CatFacts],
    "About": [about_page],
    })
    
pg.run()