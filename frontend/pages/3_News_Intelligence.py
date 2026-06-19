import streamlit as st

st.title("📰 News Intelligence")

st.write("### Latest News")

news = [
    "Infosys wins AI contract",
    "Reliance expands retail operations",
    "ICICI Bank reports strong earnings",
    "TCS launches new platform"
]

for item in news:
    st.write("•", item)