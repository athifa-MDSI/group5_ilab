import streamlit as st
import pandas as pd
import pickle
from joblib import load
from sklearn.preprocessing import StandardScaler
import pydeck as pdk
import numpy as np
import matplotlib.pyplot as plt
import altair as alt
import folium
from xgboost import XGBRegressor
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
from machine_learning.models.breast_cancer_inputvalues import breastCan_input_values

def breast_cancer():
# Load your model

 model = load('machine_learning/models_joblib/Breast_Cancer_Participants_XGBRegressor.joblib')

# Load your data

 df = pd.read_csv('machine_learning/data/Breast_Cancer_participants.csv')
 df

 breastCan_input_values()
#State_and_territory	SA3_name	Year	Age_group	Participants

# Create dropdowns for selecting state, year, and age
 unique_State = sorted(df['State_and_territory'].unique())
 selected_state2 = st.selectbox("Select State/Territory", unique_State, key="state_selectbox2")
 unique_SA3_name = sorted(df['SA3_name'].unique())
 selected_SA3_name = st.selectbox("Select SA3 Name", unique_SA3_name, key="sa3_name_selectbox2")
 current_max_year = max(df['Year'])
 future_years = range(current_max_year + 1, current_max_year + 11)
 year_options = sorted(list(set(future_years)))
 selected_year = st.selectbox("Year", options=year_options, key="year_selectbox2")
 unique_age = sorted([str(age) for age in df['Age_group'].unique()])
 selected_age = st.selectbox("Select Age_group", unique_age, key="age_group_selectbox2")
 
 # get the latitude and longitude against the sa3 name
 def get_coordinates_for_sa3(sa3_name, csv_file_path):
    # Read the CSV file containing SA3 names, longitude, and latitude
    sa3_data1 = pd.read_csv(csv_file_path)
    sa3_data = sa3_data1.drop_duplicates(subset=['SA3_name', 'Latitude', 'Longitude'])
    
    # Filter the DataFrame to get the row for the specified SA3 name
    sa3_row = sa3_data[sa3_data['SA3_name'] == sa3_name]
    
    # If SA3 name not found, return None for latitude and longitude
    if sa3_row.empty:
        return None, None
    
    # Extract latitude and longitude from the DataFrame
    latitude = sa3_row['Latitude'].values[0]
    longitude = sa3_row['Longitude'].values[0]
    
    return latitude, longitude




# Create a button to trigger prediction
 if st.button('Predict', key="predict_button2"):
    try:
        # Create input features DataFrame
        input_features = pd.DataFrame({
            'State_and_territory': [selected_state2],
            'SA3_name': [selected_SA3_name],
            'Year': [selected_year],
            'Age_group' :[selected_age]
            
        })


        # Predict for the selected state, year, age, latitude, and longitude
        prediction = model.predict(input_features)

        # Visualize predicted values on a map
        predicted_df = input_features.copy()
        predicted_df['Prediction'] = prediction.astype(int)

        # Display the prediction
        st.write("Predicted Breast Cancer Nos. participants:", predicted_df)
         
        #map = folium.Map(location=[selected_lat, selected_long], zoom_start=5)
         # Create the Folium map with a custom tile layer and attribution
        sa3_name = selected_SA3_name  # Specify the SA3 name you want to get coordinates for
        csv_file_path = 'machine_learning/data/cleaned_final_breastcancer__data1.csv'  # Specify the path to your CSV file
        selected_lat, selected_long = get_coordinates_for_sa3(sa3_name, csv_file_path)
        #st.write(f'Latitude: {sa3_name}, Longitude: {sa3_name}')
 
        map = folium.Map(
             location=[selected_lat, selected_long],
             zoom_start=6,
             tiles='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',  # Example custom tile layer
             attr='Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        )
        # Add a marker for the selected state with the predicted value as tooltip
        folium.Marker(
            location=[selected_lat, selected_long],
            popup=f"SA3 Name: {selected_SA3_name}<br>State: {selected_state2}<br>Predicted Nos. participants: {prediction.astype(int)}",
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(map)

        # Display the map
        folium_static(map) 
        
        def predict_graph(selected_state2, prediction):
            # Create input features DataFrame


            # Define the state abbreviations
     
            state_abbreviations = ['NSW', 'Qld', 'Vic', 'WA', 'NT', 'ACT', 'SA', 'Tas']

            # Create the bar chart
            fig, ax = plt.subplots()
            bar_width = 0.1  # Adjust the bar width as needed

            # Plot bars for all states
            ax.bar(range(len(state_abbreviations)), prediction, width=bar_width, color='lightgrey')

            # Move the bar to the selected state
            selected_index = state_abbreviations.index(selected_state2)
            selected_prediction_value = prediction  # Use the first (and only) prediction value
            ax.bar(selected_index, selected_prediction_value, color='green')

            # Annotate the prediction value on the bar
            ax.text(selected_index, selected_prediction_value, f'{prediction.astype(int)}', ha='center', va='bottom', color='blue', fontsize=8)

            ax.set_xticks(range(len(state_abbreviations)))
            ax.set_xticklabels(state_abbreviations, rotation=45, ha='right')
            ax.set_ylabel('Cancer Screening Predicted Nos. participants')

            st.pyplot(fig)    

            # Call the function with the selected parameters
        predict_graph(selected_state2, prediction)



    except Exception as e:
        st.error(f"An error occurred during prediction: {e}")