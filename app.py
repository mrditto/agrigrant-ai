import streamlit as st
import requests

class Model:
    def __init__(self):
        # Initialize your model here
        pass

def validate_email(email):
    import re
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

def main():
    st.title('Grant Finder')
    api_key = st.text_input('API Key')
    if not api_key:
        st.error('API Key is required.')
        return

    email = st.text_input('Email')
    if email and not validate_email(email):
        st.error('Invalid email address.')
        return

    # Use the model
    model = Model()

    # Assuming you have grants data
    grants = fetch_grants_data()
    if not grants:
        st.error('No grants found.')
        return

    # Proceed to display grants
    for grant in grants:
        st.write(grant)

def fetch_grants_data():
    # Fetch your grants data from an API
    response = requests.get('https://api.example.com/grants')
    if response.status_code != 200:
        st.error('Error fetching grants data.')
        return None
    return response.json()

if __name__ == '__main__':
    main()