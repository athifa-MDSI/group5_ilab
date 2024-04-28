import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go

import pandas as pd
import re
import streamlit as st

def load_data():
    try:
        df = pd.read_csv('data_visualisation/breast_cancer/data/brc_general.csv')
        # Use regular expression to find the first sequence of digits at the beginning of the string
        df['Start Year'] = df['Year'].apply(lambda x: int(re.match(r'^(\d+)', x).group(1)) if re.match(r'^(\d+)', x) else None)
    except Exception as e:
        st.error(f"Failed to load and process data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on failure
    return df

def load_monthly_data(state):
    df = pd.read_csv('data_visualisation/breast_cancer/data/brc_monthly_mammograms_performed.csv')
    df['Date'] = pd.to_datetime(df['Period (quarter)'].astype(str))  # Assuming 'Month' was a typo since we have 'Period (quarter)'
    
    # Directly use 'Count' from the data if applicable
    df = df[['Date', state]].rename(columns={state: 'Participation (%)'})

    return df


def create_monthly_screening_plot(data):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Participation (%)'],
                             fill='tozeroy',  # Fill area under the line
                             name='Participation',
                             line=dict(color='deepskyblue')))

    # Enhancements
    fig.update_layout(title='Monthly Screening Participation',
                      xaxis_title='Date',
                      yaxis_title='Participation (%)',
                      legend_title='Screening Status')
    return fig



def create_temporal_plot(data, state, selected_age_groups):
    # Filter data based on state and selected age groups only
    filtered_data = data[
        (data['State/territory'] == state) &
        (data['Age group'].isin(selected_age_groups))
    ]

    # Group by 'Start Year' and 'Age group' to calculate the mean participation for each group over time
    grouped_data = filtered_data.groupby(['Start Year', 'Age group'])['Participation (%)'].mean().reset_index()

    colors = px.colors.qualitative.T10
    fig = px.area(
        grouped_data,
        x='Start Year',
        y='Participation (%)',
        color='Age group',
        title=f"Participation Over Time in {state}",
        line_shape='spline'
    )

    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='Average Participation (%)',
        legend_title='Age Group'
    )

    return fig

# Remove the sex_partition_plot if it's no longer relevant

def create_age_partition_plot(data, selected_years, selected_state):
    # Filter data based on selected years and state
    filtered_data = data[(data['Start Year'].isin(selected_years)) & (data['State/territory'] == selected_state)]

    # Group by Age group, then calculate the mean participation percentage
    grouped_data = filtered_data.groupby(['Age group'])['Participation (%)'].mean().reset_index()

    # Create the plot
    fig = px.bar(grouped_data,
                 x='Age group',
                 y='Participation (%)',
                 title=f"Average Participation % by Age Group in {selected_state}")
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




def temporal_page_brc():
    st.title("Temporal Trends in Participation")
    data = load_data()

    state_option, selected_years, age_groups = setup_controls(data)
    monthly_data = load_monthly_data(state_option)

    fig_monthly = create_monthly_screening_plot(monthly_data)
    st.plotly_chart(fig_monthly)

    # Assuming 'create_temporal_plot' is adjusted to the new dataset configuration
    fig_temporal = create_temporal_plot(data, state_option, age_groups)
    st.plotly_chart(fig_temporal)


# Utility function to setup controls
def setup_controls(data):
    col1, col2, col3 = st.columns(3)
    with col1:
        state_option = st.selectbox("Select State/Territory:", options=data['State/territory'].unique(), index=0)
    with col2:
        years = sorted(data['Start Year'].unique())
        selected_years = st.multiselect("Select Years:", options=years, default=years)
    with col3:
        age_groups = sorted(data['Age group'].unique())
        selected_age_groups = st.multiselect("Select Age Groups:", options=age_groups, default=age_groups)
    return state_option, selected_years, selected_age_groups
