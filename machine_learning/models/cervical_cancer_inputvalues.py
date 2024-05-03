import streamlit as st
import pandas as pd 

def cervical_input_values():
    #load the csv to display input values so the users can get help with data entry.
    df = pd.read_csv('machine_learning/data/Cervical_Cancer_last.csv')
    
    states = df["States_and_territories"].tolist()
    age = df["Age"].tolist()
    df_combined = pd.DataFrame({
        "States_and_territories": states,
        "Age": age
    }).drop_duplicates()
    
    
    # set the session state
    if 'display_result1' not in st.session_state:
        st.session_state.display_result1 = False
    if 'reset1' not in st.session_state:
        st.session_state.reset1 = False
    st.header("")
    
    #callback function
    def btn_b_callback1():
        st.session_state.display_result1=False
        st.session_state.reset1=False
    
    # creating a button
    open_button_a1 = st.button('Cervical Input Values', key='open_button_a1')
    if open_button_a1:
       st.session_state.display_result1 = True

    if st.session_state.display_result1:
       st.write(df_combined)
       close_button_b1 = st.button('Close Button', on_click=btn_b_callback1, key='close_button_b1')#close button uses a callback function to close the butoon
       

