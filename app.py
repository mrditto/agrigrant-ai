import streamlit as st
import json
import os
import requests
from google.generativeai import GenerativeModel
import google.generativeai as genai

# Initialize session state
if "step" not in st.session_state:
    st.session_state.step = 0
if "interview_data" not in st.session_state:
    st.session_state.interview_data = {}

# Load grants database
grants_path = os.path.join(os.path.dirname(__file__), 'grants_database.json')
with open(grants_path, 'r') as f:
    grants_db = json.load(f)

# Initialize Google Generative AI
api_key = st.secrets.get("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("⚠️ GOOGLE_API_KEY not found in secrets.toml")

PRIMARY_COLOR = "#C9881F"
SECONDARY_COLOR = "#8B2E1F"

st.set_page_config(page_title="AgriGrant AI", page_icon="🌾", layout="wide")

st.markdown(f"""
<style>
    .stButton>button {{
        background-color: {PRIMARY_COLOR};
        color: white;
    }}
    h1 {{ color: {PRIMARY_COLOR}; }}
</style>
""", unsafe_allow_html=True)

st.title("🌾 AgriGrant AI")
st.markdown("**Find grants that match your farm in minutes.**")

def match_grants():
    """Use Gemini to match grants based on interview answers."""
    data = st.session_state.interview_data
    
    prompt = f"""You are a grant-matching expert for farmers. Based on this farmer's information:

- Farm Name: {data.get('farm_name', 'N/A')}
- County: {data.get('county', 'N/A')}
- Primary Crop: {data.get('primary_crop', 'N/A')}
- Acres: {data.get('acres', 'N/A')}
- Organic Status: {data.get('organic_status', 'N/A')}
- Years Farming: {data.get('years_farming', 'N/A')}
- Beginning Farmer: {data.get('is_beginning_farmer', 'N/A')}
- Veteran: {data.get('is_veteran', 'N/A')}
- Main Goal: {data.get('main_goal', 'N/A')}
- Budget: {data.get('budget', 'N/A')}

Recommend the TOP 3 MATCHING GRANTS based on USDA programs. For each one, explain WHY it's a good fit in 1-2 sentences.

Format your response as:
**GRANT NAME**
Why: [explanation]
"""
    
    try:
        model = GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(
            prompt,
            generation_config={
                "max_output_tokens": 500,
                "temperature": 0.7
            }
        )
        return response.text
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# Interview Steps
if st.session_state.step == 0:
    st.info("📋 Answer a few quick questions and we'll show you the best grants for your farm.")
    if st.button("▶️ Start Interview", use_container_width=True, type="primary"):
        st.session_state.step = 1
        st.rerun()

elif st.session_state.step == 1:
    st.progress(0.25, text="Section 1 of 4: Location")
    st.subheader("📍 Section 1: Farm Location")
    
    farm_name = st.text_input("Farm/Business Name", value=st.session_state.interview_data.get('farm_name', ''))
    farm_address = st.text_input("Farm Address", value=st.session_state.interview_data.get('farm_address', ''))
    county = st.text_input("County", value=st.session_state.interview_data.get('county', ''))
    
    st.session_state.interview_data.update({
        'farm_name': farm_name,
        'farm_address': farm_address,
        'county': county
    })
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back"):
            st.session_state.step = 0
            st.rerun()
    with col2:
        if st.button("Next ➡️", use_container_width=True) and farm_name and farm_address and county:
            st.session_state.step = 2
            st.rerun()
        elif not (farm_name and farm_address and county):
            st.warning("⚠️ Please fill in all fields to continue")

elif st.session_state.step == 2:
    st.progress(0.50, text="Section 2 of 4: Farm Details")
    st.subheader("🌱 Section 2: Your Farm")
    
    primary_crop = st.selectbox(
        "Primary Crop",
        ["Corn", "Soybeans", "Hay", "Vegetables", "Fruit", "Livestock", "Mixed"]
    )
    acres = st.slider("Total Acres", 1, 10000, st.session_state.interview_data.get('acres', 100))
    ownership = st.radio("Own or Lease?", ["Own", "Lease", "Both"])
    organic = st.radio("Organic Status", ["Conventional", "Transitioning", "Certified"])
    years = st.number_input("Years Farming", 0, 80, st.session_state.interview_data.get('years_farming', 5))
    
    st.session_state.interview_data.update({
        'primary_crop': primary_crop,
        'acres': acres,
        'ownership': ownership,
        'organic_status': organic,
        'years_farming': years
    })
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back"):
            st.session_state.step = 1
            st.rerun()
    with col2:
        if st.button("Next ➡️", use_container_width=True):
            st.session_state.step = 3
            st.rerun()

elif st.session_state.step == 3:
    st.progress(0.75, text="Section 3 of 4: About You")
    st.subheader("👤 Section 3: About You")
    
    name = st.text_input("Full Legal Name", value=st.session_state.interview_data.get('name', ''))
    email = st.text_input("Email", value=st.session_state.interview_data.get('email', ''))
    beginning = st.radio("Beginning Farmer (< 10 years)?", ["No", "Yes"])
    veteran = st.radio("U.S. Military Veteran?", ["No", "Yes"])
    
    st.session_state.interview_data.update({
        'name': name,
        'email': email,
        'is_beginning_farmer': beginning == "Yes",
        'is_veteran': veteran == "Yes"
    })
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back"):
            st.session_state.step = 2
            st.rerun()
    with col2:
        if st.button("Next ➡️", use_container_width=True) and name and email:
            st.session_state.step = 4
            st.rerun()
        elif not (name and email):
            st.warning("⚠️ Please fill in name and email")

elif st.session_state.step == 4:
    st.progress(1.0, text="Section 4 of 4: Goals")
    st.subheader("🎯 Section 4: Your Goals")
    
    goal = st.selectbox(
        "What's your main goal?",
        ["Soil Health", "Water Quality", "Erosion Control", "Organic Transition", "Equipment", "Energy/Renewable", "Disaster Recovery", "Value-Added Product"]
    )
    budget = st.radio("Budget Range", ["Under $5K", "$5-25K", "$25-50K", "$50K+"])
    matching = st.radio("Do you have matching funds?", ["No", "Yes", "Not Sure"])
    timeline = st.selectbox("Timeline", ["ASAP", "3-6 months", "6-12 months", "Flexible"])
    
    st.session_state.interview_data.update({
        'main_goal': goal,
        'budget': budget,
        'matching_funds': matching,
        'timeline': timeline
    })
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back"):
            st.session_state.step = 3
            st.rerun()
    with col2:
        if st.button("🔍 Find Grants", use_container_width=True, type="primary"):
            st.session_state.step = 5
            st.rerun()

elif st.session_state.step == 5:
    st.progress(1.0, text="Your Results")
    st.subheader("🎯 Your Recommended Grants")
    st.markdown("Based on your farm profile, here are the top grants you qualify for:")
    
    with st.spinner("⏳ Gemini is analyzing your farm..."):
        recommendations = match_grants()
    
    st.markdown(recommendations)
    
    st.markdown("---")
    st.markdown("### 📞 Next Steps")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        1. Review the grants above
        2. Contact your local USDA Service Center
        3. Submit applications (deadlines vary)
        """)
    with col2:
        st.markdown(f"""
        **📍 Your County:** {st.session_state.interview_data.get('county', 'N/A')}
        
        **Find Your USDA Office:**
        👉 farmers.gov/service-locator
        """)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back to Goals"):
            st.session_state.step = 4
            st.rerun()
    with col2:
        if st.button("↺ Start Over", use_container_width=True):
            st.session_state.step = 0
            st.session_state.interview_data = {}
            st.rerun()
