import streamlit as st
import pandas as pd 


def bowelCan_input_values():
    
    df = pd.read_csv('machine_learning/data/Bowel_cancer.csv')
    
    states = df["State_and_territory"].tolist()
    SA3_names = df["SA3_name"].tolist()
  
    df_combined = pd.DataFrame({
        "States_and_territorie": states,
        "SA3_name": SA3_names
    }).drop_duplicates()
    if 'display_result3' not in st.session_state:
        st.session_state.display_result3 = False
    if 'reset3' not in st.session_state:
        st.session_state.reset3 = False
    st.header("")
    
    def btn_b_callback3():
        st.session_state.display_result3=False
        st.session_state.reset3=False
    
    open_button_a3 = st.button('Bowel Cancer input values',key='open_button_a3')
    if open_button_a3 :
       st.session_state.display_result3 = True

    if st.session_state.display_result3:
       st.write(df_combined)
       close_button_b3 = st.button('Close_Button', on_click=btn_b_callback3, key='close_button_b3')

    