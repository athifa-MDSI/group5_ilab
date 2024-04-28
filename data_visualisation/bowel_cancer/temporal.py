import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go

from pathlib import Path
import re

def load_data():
    try:
        # Assuming 'data_visualisation' is a directory within your project root
        data_path = Path('data_visualisation/bowel_cancer/data/bc_general.csv')
        df = pd.read_csv(data_path)
        # Extract the first sequence of digits from the 'Year' column as 'Start Year'
        df['Start Year'] = df['Year'].apply(lambda x: int(re.match(r'^(\d+)', x).group(1)) if re.match(r'^(\d+)', x) else None)
    except Exception as e:
        st.error(f"Failed to load and process data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on failure
    return df

def load_monthly_data(state):
    df = pd.read_csv('data_visualisation/bowel_cancer/data/bc_monthly.csv')
    df['Date'] = pd.to_datetime(df['Year'].astype(str) + ' ' + df['Month'])
    
    # Filtering data based on the selected state and status
    invited_df = df[(df['Status'] == 'Invited') & (df['Sex'] != 'Persons')][['Date', state]].rename(columns={state: 'Count'})
    returned_df = df[(df['Status'] == 'Returned') & (df['Sex'] != 'Persons')][['Date', state]].rename(columns={state: 'Count'})

    invited_df['Type'] = 'Invited'
    returned_df['Type'] = 'Returned'
    
    # Concatenate the dataframes
    final_df = pd.concat([invited_df, returned_df])
    final_df['Count'] = pd.to_numeric(final_df['Count'], errors='coerce').fillna(0)
    return final_df




def create_monthly_screening_plot(data):
    fig = go.Figure()
    for label, color in zip(['Invited', 'Returned'], ['skyblue', 'orange']):
        df_filtered = data[data['Type'] == label]
        fig.add_trace(go.Scatter(x=df_filtered['Date'], y=df_filtered['Count'],
                                 fill='tozeroy',  # Fill area under the line
                                 name=label,
                                 line=dict(color=color)))

    # Enhancements
    fig.update_layout(title='Monthly Screening - Invited vs Returned',
                      xaxis_title='Date',
                      yaxis_title='Count',
                      legend_title='Screening Status')
    return fig


def create_temporal_plot(data, sex, state, selected_age_groups):
    # Filter data based on sex, state, and selected age groups
    filtered_data = data[
        (data['Sex'] == sex) &
        (data['State/territory'] == state) &
        (data['Age group'].isin(selected_age_groups))
    ]

    # Group by 'Start Year' and 'Age group' to calculate the mean participation for each group over time
    grouped_data = filtered_data.groupby(['Start Year', 'Age group'])['Participation (%)'].mean().reset_index()

    # Creating the plot with Plotly Express
    colors = px.colors.qualitative.T10
    fig = px.area(
        grouped_data,
        x='Start Year',
        y='Participation (%)',
        color='Age group',
        template='plotly_dark',
        color_discrete_sequence=colors,
        title=f"Participation Over Time in {state}",
        line_shape='spline'
    )

    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='Average Participation (%)',
        legend_title='Age Group'
    )

    return fig



def create_sex_partition_plot(data, selected_years, selected_state):
    # Filter data based on selected years and state
    filtered_data = data[(data['Start Year'].isin(selected_years)) & (data['State/territory'] == selected_state)]

    # Group by Age group and Sex, then calculate the mean participation percentage
    grouped_data = filtered_data.groupby(['Age group', 'Sex'])['Participation (%)'].mean().reset_index()

    # Create the plot
    fig = px.bar(grouped_data,
                 x='Age group',
                 y='Participation (%)',
                 color='Sex',
                 barmode='group',
                 title=f"Average Participation % by Age Group and Sex in {selected_state}")
    return fig


def create_state_participation_plot(data, selected_years):
    # Filter the data for the selected years first
    if selected_years:
        data = data[data['Start Year'].isin(selected_years)]
        
    # Group by state and calculate the mean participation rate
    state_participation = data.groupby('State/territory')['Participation (%)'].mean().reset_index()
    
    # Sort by participation rate
    state_participation = state_participation.sort_values('Participation (%)', ascending=False)

    # Create the plot
    fig = px.bar(state_participation,
                 x='State/territory',
                 y='Participation (%)',
                 title='Average Cancer Screening Participation Rates by State',
                 color='Participation (%)',
                 color_continuous_scale=px.colors.sequential.Viridis)  # Using Plotly Express color scale
    fig.update_layout(xaxis_title='State/Territory',
                      yaxis_title='Average Participation Rate (%)',
                      coloraxis_colorbar=dict(title="Participation %"))
    return fig




def temporal_page_bc():
    st.title("Temporal Trends in Participation")
    data = load_data()

    # Get the filters from setup controls
    sex_option, state_option, selected_years, age_groups = setup_controls(data)

    monthly_data = load_monthly_data(state_option)

    # Grid layout for plots
    row1_col1, row1_col2 = st.columns(2)
    row2_col1, row2_col2 = st.columns(2)

    with row1_col1:
        fig_temporal = create_temporal_plot(data, sex_option, state_option, age_groups)
        st.plotly_chart(fig_temporal)

    with row1_col2:
        fig_sex_partition = create_sex_partition_plot(data, selected_years, state_option)
        st.plotly_chart(fig_sex_partition)

    with row2_col1:
        fig_state_participation = create_state_participation_plot(data, selected_years)
        st.plotly_chart(fig_state_participation)

    with row2_col2:
        fig_monthly_screening = create_monthly_screening_plot(monthly_data)
        st.plotly_chart(fig_monthly_screening)

# Utility function to setup controls
def setup_controls(data):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        sex_option = st.selectbox("Select Sex:", options=data['Sex'].unique(), index=0)
    with col2:
        state_option = st.selectbox("Select State/Territory:", options=data['State/territory'].unique(), index=0)
    with col3:
        years = sorted(data['Start Year'].unique())
        selected_years = st.multiselect("Select Years:", options=years, default=years)
    with col4:
        age_groups = sorted(data['Age group'].unique())
        selected_age_groups = st.multiselect("Select Age Groups:", options=age_groups, default=age_groups)
    return sex_option, state_option, selected_years, selected_age_groups
