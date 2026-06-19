import streamlit as st

st.title("📊 Dashboard")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Companies", "10")

with col2:
    st.metric("News Articles", "250")

with col3:
    st.metric("Risk Alerts", "12")

st.subheader("Market Trend")

st.line_chart(
    [24500, 24600, 24750, 24680, 24800]
)