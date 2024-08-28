import streamlit as st
from add_new_ben import load_emails, send_mail_page, save_emails
from home_page import home_page

# Function to navigate between pages using buttons
def main():
    st.sidebar.title("Options")

    if 'page' not in st.session_state:
        st.session_state.page = "Home"

    if st.sidebar.button("Home"):
        st.session_state.page = "Home"
    if st.sidebar.button("Send Mail"):
        st.session_state.page = "Send Mail"

    if st.session_state.page == "Home":
        home_page()
    elif st.session_state.page == "Send Mail":
        send_mail_page()

if __name__ == "__main__":
    main()
