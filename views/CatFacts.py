import json
import requests
import streamlit as st
import os

st.set_page_config(layout="wide")
st.title("🐱 Live Breed-Populated Cat Gallery")
CAT_API_KEY = st.secrets["api_key"]
base_url = "https://api.thecatapi.com/v1/"
headers = {"x-api-key": CAT_API_KEY} if CAT_API_KEY else {}

url = base_url + "breeds"
response = requests.get(url, headers=headers, timeout=5)
data = response.json()

# Extract a list of all breed names, plus an "All" option
breed_names = [x["name"] for x in data]
breed_names.insert(0, "All Breeds")

# Add the dropdown filter to the sidebar
selected_breed = st.sidebar.selectbox("Select a Cat Breed:", breed_names)

# Filter the data based on the sidebar selection
if selected_breed != "All Breeds":
  filtered_data = [x for x in data if x["name"] == selected_breed]
else:
  filtered_data = data

# Loop through each item in your filtered dataset
for x in filtered_data:
  # 1. Outer Container creates the Bootstrap-style card border around the whole item
  with st.container(border=True):
    # 2. Put columns INSIDE the loop so every item gets its own side-by-side row
    col1, col2 = st.columns([1, 1])

    with col1:
      # 3. Check safe dictionary fetching and use correct image sizing syntax
      if "image" in x and x["image"] and "url" in x["image"]:
        st.image(x["image"]["url"], width='stretch')
      else:
        st.image("placeholder.jpg", width='stretch')

    with col2:
      # 4. Use double quotes inside single-quoted f-strings to avoid SyntaxError
      st.subheader(f"Name: {x['name']}")

      # 5. Cleanly print out the allowed dictionary keys
      for key, value in x.items():
        if key in ["life_span", "temperament", "description", "history"]:
          clean_key = key.replace("_", " ").title()
          st.write(f"**{clean_key}:** {value}")

    # Optional: Small spacing buffer between your card blocks
    st.write("")
