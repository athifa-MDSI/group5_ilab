import streamlit as st
import pandas as pd
import pickle
import joblib
from sklearn.preprocessing import StandardScaler
from joblib import load
import pydeck as pdk
import numpy as np
import matplotlib.pyplot as plt
import altair as alt
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
from machine_learning.models.cervical_cancer_inputvalues import cervical_input_values
from machine_learning.models.cervical_cancer_invited import invited

def cervical_cancer():

# Load your model
 model = load('machine_learning/models_joblib/cervical_RandomForestR_pipeline.joblib')

# Load your data

 df = pd.read_csv('machine_learning/data/Cervical_Cancer_last.csv')


 # Setting up the session state for click_button
 if 'clicked' not in st.session_state:
        st.session_state.clicked = False

 def click_button():
        st.session_state.clicked = True

 st.button('People_Invited', on_click=click_button)
    
 if st.session_state.clicked:
       invited() #Calling the invited function to display the number of people invited in the past


 cervical_input_values()

# Create dropdowns for selecting state, year, and age
 unique_State = sorted(df['States_and_territories'].unique())
 selected_state = st.selectbox("Select State/Territory", unique_State, key="state_selectbox1")
 unique_age = sorted(df['Age'].unique())
 selected_age = st.selectbox("Select Age",unique_age, key="age_selectbox1")
 current_max_year = max(df['Year'])
 future_years = range(current_max_year + 1, current_max_year + 11)
 year_options = sorted(list(set(future_years)))
 selected_year = st.selectbox("Year", options=year_options, key="year_selectbox1")

 # The below methods pull the latitude, and langitude information against the selected state from CSV.
 def get_coordinates_for_sa3(state_name, csv_file_path):
    # Read the CSV file containing States_and_territories names, longitude, and latitude
    state_data1 = pd.read_csv(csv_file_path)
    state_data = state_data1.drop_duplicates(subset=['States_and_territories', 'Latitude', 'Longitude'])
    
    # Filter the DataFrame to get the row for the specified SA3 name
    state_row = state_data[state_data['States_and_territories'] == state_name]
    
    # If SA3 name not found, return None for latitude and longitude
    if state_row.empty:
        return None, None
    
    # Extract latitude and longitude from the DataFrame
    latitude = state_row['Latitude'].values[0]
    longitude = state_row['Longitude'].values[0]
    
    return latitude, longitude



 if st.button('Predict', key="predict_button1"):
    try:
        # Prepare input data as a dictionary
        input_data = {
            'States_and_territories': [selected_state],
            'Year': [selected_year],
            'Age': [selected_age]
        }

        # Convert input data to a DataFrame
        input_features = pd.DataFrame(input_data)

        # Predict using the model
        prediction = model.predict(input_features)
        
        # Visualize predicted values on a map
        predicted_df = input_features.copy()
        predicted_df['Prediction'] = prediction.astype(int)

        # Display the prediction
        st.write("Predicted Cervical Cancer Nos. participants:", predicted_df)
        
        state_name = selected_state  # Specify the SA3 name you want to get coordinates for
        csv_file_path = 'machine_learning/data/2_cervical_abnormality_primary_screening_tests_2018_2022.csv'  # Specify the path to your CSV file
        selected_lat, selected_long = get_coordinates_for_sa3(state_name, csv_file_path)

        # This method helps in displaying the prediction on the map.
        def predict_map(selected_state, selected_lat, selected_long, prediction):

                m = folium.Map(location=[selected_lat, selected_long], zoom_start=10)

                # Add marker with suburb name and predicted value
                popup_content = f'State: {selected_state}<br>Predicted Nos. participants : {prediction.astype(int)}'
                folium.Marker(location=[selected_lat, selected_long], popup=popup_content).add_to(m)

                return m
        
        m = predict_map(selected_state, selected_lat, selected_long, prediction)
        folium_static(m) # display the map
        
        
        ### Plotting a prediction graph

        def predict_graph(selected_state, prediction):

           # Define the state abbreviations
     
            state_abbreviations = ['NSW', 'QLD', 'Vic', 'WA', 'NT', 'ACT', 'SA', 'Tas']

            # Create the bar chart
            fig, ax = plt.subplots()
            bar_width = 0.1  # Adjust the bar width as needed

            # Plot bars for all states
            ax.bar(range(len(state_abbreviations)), prediction, width=bar_width, color='lightgrey')

            # Move the bar to the selected state
            selected_index = state_abbreviations.index(selected_state)
            selected_prediction_value = prediction  # Use the first (and only) prediction value
            ax.bar(selected_index, selected_prediction_value, color='red')

            # Annotate the prediction value on the bar
            ax.text(selected_index, selected_prediction_value, f'{prediction.astype(int)}', ha='center', va='bottom', color='blue', fontsize=8)

            ax.set_xticks(range(len(state_abbreviations)))
            ax.set_xticklabels(state_abbreviations, rotation=45, ha='right')
            ax.set_ylabel('Cancer Screening Predicted Nos. participants')

            st.pyplot(fig)    

        #Call the function with appropriate arguments after obtaining the prediction
        predict_graph(selected_state, prediction )
        



              
    except Exception as e:
        st.error(f"An error occurred during prediction: {e}")
        







 
 
 
