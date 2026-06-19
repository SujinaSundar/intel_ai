import streamlit as st

st.title("🏢 Company Research")

company = st.selectbox(
    "Select Company",
    [
        "Infosys",
        "TCS",
        "Reliance",
        "ICICI Bank"
    ]
)

st.write(f"### {company}")

st.write("Sector: Information Technology")

st.write("""
Dummy company description.
This data will later come from PostgreSQL.
""")