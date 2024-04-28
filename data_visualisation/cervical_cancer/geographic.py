import pandas as pd
import streamlit as st
import pydeck as pdk

# Load and Prepare Data Function
def load_and_prepare_data():
    df = pd.read_csv('data_visualisation/cervical_cancer/data/geo_sa3_data.csv')
    df['Participants'] = pd.to_numeric(df['Participants'].str.replace(',', ''), errors='coerce')
    df['Population'] = pd.to_numeric(df['Population'].str.replace(',', ''), errors='coerce')
    df['Participation_perc'] = pd.to_numeric(df['Participation (%)'], errors='coerce')
    df = df.dropna(subset=['Lat_precise', 'Long_precise'])
    return df

# Create Geographical Map Function
def create_geographical_map(filtered_data, column_name, color, cell_size=200):
    if column_name == 'Participation_perc':
        layer = pdk.Layer(
            "HeatmapLayer",
            data=filtered_data,
            get_position='[Long_precise, Lat_precise]',
            get_weight=column_name,  # Weight by participation percentage
            radius=cell_size,  # Radius of each data point for the heatmap
            intensity=1,  # Intensity of each point
            color_range=[  # Color from blue (low) to red (high)
                [0, 0, 255, 25],  # Blue, low
                [0, 255, 255, 85],  # Cyan
                [0, 255, 0, 127],  # Green
                [255, 255, 0, 170],  # Yellow
                [255, 165, 0, 212],  # Orange
                [255, 0, 0, 255]  # Red, high
            ],
            threshold=0.05,  # Minimum threshold for rendering
            opacity=0.6
        )
    else:
        scaling_factor = 0.5 if column_name != 'Participation_perc' else 100
        layer = pdk.Layer(
            'ScatterplotLayer',
            filtered_data,
            get_position='[Long_precise, Lat_precise]',
            get_color=color,
            get_radius=f"{column_name} * {scaling_factor}",
            pickable=True,
            opacity=0.8
        )

    view_state = pdk.ViewState(
        longitude=filtered_data['Long_precise'].mean(),
        latitude=filtered_data['Lat_precise'].mean(),
        zoom=6,
        pitch=0
    )

    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        map_style='mapbox://styles/mapbox/light-v9'
    )
    return deck



def geographical_tab_cc():
    st.title('Geographical Trends in Participation')
    df = load_and_prepare_data()

    state_option, sa3_code, sa3_name, year = setup_controls(df)

    if state_option:
        df = df[df['State/territory'].isin(state_option)]
    if sa3_code:
        df = df[df['SA3 code'].isin(sa3_code)]
    if sa3_name:
        df = df[df['SA3 name'].isin(sa3_name)]
    if year:
        df = df[df['Year'].isin(year)]

    if df.empty:
        st.write("No data available for the selected filters.")
    else:
        # Display maps
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Invitation Map")
            invited_deck = create_geographical_map(df, 'Population', '[0, 116, 217, 160]')
            st.pydeck_chart(invited_deck)
        with col2:
            st.subheader("Participation Map")
            participated_deck = create_geographical_map(df, 'Participants', '[200, 30, 0, 160]')
            st.pydeck_chart(participated_deck)
        # Heatmap for participation percentage
        st.subheader("Participation Percentage Map")
        participation_percent_deck = create_geographical_map(df, 'Participation_perc', None)
        st.pydeck_chart(participation_percent_deck)


def setup_controls(data):
    col1, col2, col3, col4 = st.columns(4)

    with col2:
        # Select SA3 Code first
        sa3_code = st.multiselect("Select SA3 Code:", options=data['SA3 code'].unique())

    # Filter the dataframe based on the selected SA3 code for state and SA3 name
    if sa3_code:
        filtered_data = data[data['SA3 code'].isin(sa3_code)]
        state_options = filtered_data['State/territory'].unique()
        sa3_name_options = filtered_data['SA3 name'].unique()
    else:
        state_options = data['State/territory'].unique()
        sa3_name_options = data['SA3 name'].unique()

    with col1:
        # Select State/Territory based on selected SA3 Code
        state_option = st.multiselect("Select State/Territory:", options=state_options)

    with col3:
        # Select SA3 Name based on selected SA3 Code
        sa3_name = st.multiselect("Select SA3 Name:", options=sa3_name_options)

    with col4:
        # Select Year
        year = st.multiselect("Select Year:", options=data['Year'].unique())

    return state_option, sa3_code, sa3_name, year
