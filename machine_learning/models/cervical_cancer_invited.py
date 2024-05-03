import streamlit as st
import pandas as pd
import altair as alt

def invited():
    # Load the CSV file directly
    df = pd.read_csv('machine_learning/data/cervical_invites_2019_2022.csv')
    
    # Get unique years from the DataFrame
    years = sorted(df['Year'].unique())
    
    # Create a dropdown to select the year
    selected_year = st.selectbox("Select Year", years)
    
    # Filter data for the selected year
    df_selected_year = df[df['Year'] == selected_year]
    
    # Pivot the DataFrame to have states as rows and invited as columns
    pivot_df = df_selected_year.pivot_table(index='States_and_territories', values='Invited', aggfunc='sum').reset_index()
    
    # Plot the bar chart using Altair
    bar_chart = alt.Chart(pivot_df).mark_bar().encode(
        x='States_and_territories',
        y='Invited'
    ).properties(
        width=600,
        height=400,
        title=f'Invited for Screening by State in {selected_year}'
    )
    
    # Set y-axis label
    graph = st.altair_chart(bar_chart, use_container_width=True)

