import re

try:
    import streamlit as st
except ModuleNotFoundError:  # Allows local validation without Streamlit installed.
    st = None

from grants import load_grants_data


DEFAULT_EMAIL = ""
EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"


def validate_email(email):
    return re.match(EMAIL_REGEX, email) is not None


if st is not None:

    @st.cache_data
    def get_grants_data():
        return load_grants_data()

else:

    def get_grants_data():
        return load_grants_data()


def main():
    if st is None:
        raise SystemExit("Streamlit is not installed. Run `pip install -r requirements.txt` first.")

    st.title("Grant Finder")
    st.caption("Browse the bundled farmer grant database.")

    email = st.text_input("Email (optional)", value=DEFAULT_EMAIL)
    if email and not validate_email(email):
        st.error("Invalid email address.")
        return

    try:
        grants = get_grants_data()
    except RuntimeError as exc:
        st.error(str(exc))
        return

    if not grants:
        st.warning("No grants found.")
        return

    st.subheader(f"Available Grants ({len(grants)})")
    for grant in grants:
        with st.container(border=True):
            st.markdown(f"### [{grant['name']}]({grant['url']})")
            st.write(grant["description"])
            st.write(f"Agency: {grant['agency']}")
            st.write(f"Max funding: {grant['max_funding']}")


if __name__ == "__main__":
    main()
