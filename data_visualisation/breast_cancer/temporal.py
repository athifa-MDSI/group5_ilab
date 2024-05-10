import pandas as pd
import plotly.express as px
import streamlit as st
import re

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
    df['Date'] = pd.to_datetime(df['Period (quarter)'].astype(str))
    df = df[['Date', state]].rename(columns={state: 'Participation (%)'})
    return df

def create_temporal_plot(data, state, selected_age_groups):
    filtered_data = data[
        (data['State/territory'] == state) &
        (data['Age group'].isin(selected_age_groups))
    ]
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

def create_age_partition_plot(data, selected_years, selected_state):
    filtered_data = data[(data['Start Year'].isin(selected_years)) & (data['State/territory'] == selected_state)]
    grouped_data = filtered_data.groupby(['Age group'])['Participation (%)'].mean().reset_index()
    fig = px.bar(grouped_data,
                 x='Age group',
                 y='Participation (%)',
                 title=f"Average Participation % by Age Group in {selected_state}")
    return fig



def temporal_page_brc():
    st.title("Temporal Trends in Participation")
    data = load_data()
    state_option, selected_years, age_groups = setup_controls(data)

    # Grid layout for plots
    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:
        fig_temporal = create_temporal_plot(data, state_option, age_groups)
        st.plotly_chart(fig_temporal)

    with row1_col2:
        fig_age_partition = create_age_partition_plot(data, selected_years, state_option)
        st.plotly_chart(fig_age_partition)

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
