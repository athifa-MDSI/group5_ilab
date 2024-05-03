import streamlit as st
import pandas as pd 

# Check if the attribute is already initialized, if not, initialize it


def breastCan_input_values():
    
    df = pd.read_csv('machine_learning/data/Breast_Cancer_Participants.csv')

    states = df["State_and_territory"].tolist()
    SA3_names = df["SA3_name"].tolist()
    Age_groups = df["Age_group"].tolist()
    df_combined = pd.DataFrame({
        "States_and_territorie": states,
        "SA3_name": SA3_names,
        "Age_group": Age_groups
    }).drop_duplicates()
    if 'display_result2' not in st.session_state:
        st.session_state.display_result2 = False
    if 'reset2' not in st.session_state:
        st.session_state.reset2 = False
    st.header("")
    
    def btn_b_callback2():
        st.session_state.display_result2=False
        st.session_state.reset2=False
    
    open_button_a2 = st.button('Breast Cancer input values',key='open_button_a2')
    if open_button_a2 :
       st.session_state.display_result2 = True

    if st.session_state.display_result2:
       st.write(df_combined)
       close_button_b2 = st.button('Close Button_', on_click=btn_b_callback2, key='close_button_b2')

    