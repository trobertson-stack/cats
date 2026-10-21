import streamlit as st
import requests
import os

# 1. Base Framework Layout Setup
st.set_page_config(layout="wide", page_title="Cat API Photo Gallery")
st.title("🐱 Live Breed-Populated Cat Gallery")

# 2. Universal Custom Styling (Enforces uniform photo height dimensions)
st.markdown(
    """
    <style>
    [data-testid="stImageFilter"] img, 
    [data-testid="stHorizontalBlock"] img,
    .st_container_border img {
        height: 260px !important;
        object-fit: cover !important;
        width: 100% !important;
        border-radius: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

CAT_API_KEY = st.secrets["api_key"]

# 3. Cache the Full List of Breeds from the API
@st.cache_data(show_spinner="Loading breed dictionary from API...")
@st.cache_data(show_spinner="Loading breed dictionary...")
def get_all_breeds():
    url = "https://api.thecatapi.com/v1/breeds"
    headers = {"x-api-key": CAT_API_KEY} if CAT_API_KEY else {}

    response = requests.get(url, headers=headers, timeout=5) # Added a timeout limit
    if response.status_code == 200 and "application/json" in response.headers.get("Content-Type", ""):
        return response.json()


# 4. Dynamic API Data Fetcher for Images
def fetch_cat_images(limit=12, breed_id=""):
    # LOCK IN PLACE: Using your exact required string format
    url = f"https://api.thecatapi.com/v1/images/search?limit={limit}&has_breeds=true"
    
    # If a specific breed is chosen from the dropdown, apply the valid filter extension cleanly
    if breed_id:
        url = f"https://api.thecatapi.com/v1/images/search?limit={limit}&has_breeds=true&breed_ids={breed_id}"
        
    headers = {"x-api-key": CAT_API_KEY} if CAT_API_KEY else {}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                return data
            return []
        else:
            st.error(f"Server Connection Issue: Status code {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Network Failure Trace: {e}")
        return []

# 5. Lightbox Modal Details Dialog Window
@st.dialog("Cat Profile Information", width="large")
def open_cat_lightbox(cat_data):
    st.image(cat_data["url"], width="stretch")
    
    raw_breeds = cat_data.get("breeds", [])
    if isinstance(raw_breeds, list) and len(raw_breeds) > 0:
        breed_info = raw_breeds[0]  # Extracts the main breed dictionary object safely
        st.subheader(f"Breed: {breed_info.get('name', 'Unknown')}")
        st.write(f"**Temperament:** *{breed_info.get('temperament', 'N/A')}*")
        st.write(f"**Origin Country:** {breed_info.get('origin', 'Global')}")
        st.info(f"**About:** {breed_info.get('description', 'No details recorded.')}")
    else:
        st.subheader("Lovely Domestic Cat")
        st.caption("This cat doesn't have an associated pedigree profile track.")
        
    if st.button("Close Window"):
        st.rerun()

# 6. Initialize tracking keys inside Session State memory
if "last_breed" not in st.session_state:
    st.session_state["last_breed"] = "INITIAL_LOAD"

# Load the full breed list to build our dropdown options
breeds_list = get_all_breeds()

# Create a mapping dictionary of { "Breed Name": "breed_id" }
breed_map = {"All Breeds (Random)": ""}
for b in breeds_list:
    name = b.get("name")
    b_id = b.get("id")
    if name and b_id:
        breed_map[name] = b_id

# 7. Dropdown Select Element populated directly from breed keys
selected_breed_name = st.selectbox("🔍 Filter by Official Breed", options=list(breed_map.keys()))
target_breed_id = breed_map[selected_breed_name]

# 8. Dashboard Sidebar Form Controls
st.sidebar.header("⚙️ Core Controls")
image_count = st.sidebar.slider("Cats per Fetch Action", min_value=3, max_value=6, value=3, step=3)

# Core layout updater using correct native memory dictionary extraction methods
if st.sidebar.button("🔄 Download Fresh Cats", width="stretch") or st.session_state.get("last_breed") != target_breed_id:
    with st.spinner("Streaming filtered images from api.thecatapi.com..."):
        st.session_state.cat_gallery_data = fetch_cat_images(limit=image_count, breed_id=target_breed_id)
        # Store current breed ID tracking token to handle automated pagination changes
        st.session_state["last_breed"] = target_breed_id

# 9. Grid Renderer Layout Component
loaded_cats = st.session_state.get("cat_gallery_data", [])

if loaded_cats:
    num_columns = 3
    columns_layout = st.columns(num_columns)
    
    for idx, cat in enumerate(loaded_cats):
        with columns_layout[idx % num_columns]:
            with st.container(border=True):
                st.image(cat["url"], width="stretch")
                
                # Check list properties safely to display breed card title strings
                raw_breeds = cat.get("breeds", [])
                if isinstance(raw_breeds, list) and len(raw_breeds) > 0:
                    display_title = raw_breeds[0].get("name", "Unknown Breed")
                else:
                    display_title = "Domestic Cat"
                
                st.markdown(f"#### {display_title}")
                
                if st.button("🔎 View Breed Profile", key=f"btn_{cat.get('id', idx)}", width="stretch"):
                    open_cat_lightbox(cat)
else:
    st.warning("No cat pictures returned for this specific breed selection. Try selecting another or hit reload.")
