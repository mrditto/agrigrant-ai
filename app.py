import json
import re
import streamlit as st

def validate_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

def fetch_grants_data():
    try:
        with open('grants_database.json', 'r') as f:
            data = json.load(f)
        return data.get('grants', [])
    except FileNotFoundError:
        st.error('grants_database.json not found.')
        return None
    except json.JSONDecodeError as e:
        st.error(f'Invalid JSON in grants database: {e}')
        return None

def main():
    st.title('Grant Finder')

    email = st.text_input('Email')
    if email and not validate_email(email):
        st.error('Invalid email address.')
        return

    grants = fetch_grants_data()
    if not grants:
        st.error('No grants found.')
        return

    for grant in grants:
        st.write(grant)

if __name__ == '__main__':
    main()
