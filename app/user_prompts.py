import streamlit as st

def prompt_for_missing_info(startup_data):
    st.subheader("Additional Information Needed")
    
    # Check for missing information and prompt the user
    if "revenue" not in startup_data:
        revenue = st.number_input("What is the company's annual revenue?", min_value=0)
        startup_data["revenue"] = revenue
    
    if "employees" not in startup_data:
        employees = st.number_input("How many employees does the company have?", min_value=1)
        startup_data["employees"] = employees
    
    if "funding_raised" not in startup_data:
        funding = st.number_input("How much funding has the company raised so far?", min_value=0)
        startup_data["funding_raised"] = funding
    
    # Add more prompts for other necessary information
    
    return startup_data