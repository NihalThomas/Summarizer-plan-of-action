import streamlit as st
import streamlit.components.v1 as components

# Load CSS
with open("buttonss.css") as f:
    css = f.read()

# Load HTML
with open("web_page.html") as f:
    html = f.read()

# Render CSS and HTML in Streamlit
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
components.html(html, height=100)