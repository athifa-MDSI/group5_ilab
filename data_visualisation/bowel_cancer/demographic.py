import pandas as pd
import streamlit as st
import plotly.express as px

def load_data():
    df = pd.read_csv('data_visualisation/bowel_cancer/data/final_bc_data.csv')
    # Calculating the percentage of English spoken at home
    df['Percentage English Spoken'] = df['Language_spoken_at_home_English_only_Persons'] / (df['Language_spoken_at_home_English_only_Persons'] + df['Language_spoken_at_home_Other_Language_Persons']) * 100
    return df

def create_income_vs_participation_plot(data):
    # Assuming 'Participation (%)' and 'Median_total_household_income_weekly' are present and correctly formatted in data
    fig = px.scatter(data,
                     x='Median_total_household_income_weekly',
                     y='Participation (%)',
                     title='Household Income vs. Participation Rate',
                     hover_data=['State/territory', 'Year'])  # Including hover data for better insight on each point
    
    # Customize marker appearance
    fig.update_traces(marker=dict(size=10, opacity=0.7, line=dict(width=1, color='DarkSlateGrey')))
    
    # Enhancements for layout
    fig.update_layout(xaxis_title='Median Total Household Income Weekly ($)',
                      yaxis_title='Participation Rate (%)',
                      xaxis_tickangle=-45,
                      plot_bgcolor='white',
                      yaxis=dict(tickformat=".2%"))  # Format the y-axis ticks as percentages

    st.plotly_chart(fig)

def create_language_vs_participation_plot(data):
    # Calculate total sums for English and Other Languages spoken at home
    total_english = data['Language_spoken_at_home_English_only_Persons'].sum()
    total_other = data['Language_spoken_at_home_Other_Language_Persons'].sum()

    # Preparing data for the donut chart
    language_data = {
        'Language': ['English Only', 'Other Languages'],
        'Count': [total_english, total_other]
    }
    df_language = pd.DataFrame(language_data)

    # Creating a donut chart
    fig = px.pie(df_language, values='Count', names='Language', title='Language Spoken at Home', hole=0.5)
    fig.update_traces(textposition='inside', textinfo='percent+label')

    st.plotly_chart(fig)


def create_birthplace_donut_chart(data):
    # Summing the columns for the chart
    birthplace_data = {
        'Category': ['Australia', 'Elsewhere'],
        'Count': [data['Birthplace_Australia_Persons'].sum(), data['Birthplace_Elsewhere_Persons'].sum()]
    }
    df_pie = pd.DataFrame(birthplace_data)

    # Creating a donut chart
    fig = px.pie(df_pie, values='Count', names='Category', title='Birthplace Distribution', hole=0.5)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig)



def create_donut_chart(data, value, name, title):
    # Data preparation for the donut chart
    chart_data = {
        'Category': [name, 'Other'],
        'Count': [data[value].sum(), data['Total_Persons'].sum() - data[value].sum()]
    }
    df_chart = pd.DataFrame(chart_data)
    
    # Creating the donut chart
    fig = px.pie(df_chart, values='Count', names='Category', title=title, hole=0.5)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig

def create_indigenous_population_chart(data):
    # Calculate the sum of Indigenous persons and calculate the non-Indigenous count
    total_indigenous = data['Aboriginal_and_or_Torres_Strait_Islander_Persons'].sum()
    total_non_indigenous = data['Total_Persons'].sum() - total_indigenous

    # Preparing data for the donut chart
    indigenous_data = {
        'Category': ['Indigenous Persons', 'Non-Indigenous Persons'],
        'Count': [total_indigenous, total_non_indigenous]
    }
    df_indigenous = pd.DataFrame(indigenous_data)

    # Creating a donut chart
    fig = px.pie(df_indigenous, values='Count', names='Category', title='Proportion of Indigenous Persons in Population', hole=0.5)
    fig.update_traces(textposition='inside', textinfo='percent+label')

    st.plotly_chart(fig)


def create_education_proportion_table(data):
    # Calculate the total of persons with higher education
    higher_education_columns = [
        "Persons_Advanced_and_Associate_Degree",
        "Persons_Advanced_Diploma",
        "Persons_Certificate_Level_Certificate_III_and_IV",
        "Persons_Certificate_Level_Certificate_I_and_II",
        "Persons_Postgraduate_Degree",
        "Persons_Graduate_Diploma_and_Graduate_Certificate",
        "Persons_Bachelor_Degree"
    ]
    
    data['Total_Higher_Education'] = data[higher_education_columns].sum(axis=1)
    data['% Higher Education'] = data['Total_Higher_Education'] / data['Total_Persons'] * 100
    data['% Not Higher Education'] = 100 - data['% Higher Education']
    
    # Group by year and calculate the mean for each year
    education_by_year = data.groupby('Year')[['% Higher Education', '% Not Higher Education']].mean().reset_index()

    return education_by_year



def create_gender_table(data):
    # Group by year and sum the total number of males and females
    gender_by_year = data.groupby('Year')[['Total_Persons_Males', 'Total_Persons_Females']].sum().reset_index()
    return gender_by_year


import streamlit as st


def demographic_page_bc():
    st.title("Bowel Cancer Screening Demographics")
    
    df = load_data()


    # User interface row for selecting parameters
    col_state, col_year, col_participation = st.columns(3)
    with col_state:
        state_option = st.selectbox("Select State:", df['State/territory']. unique())
    with col_year:
        year_option = st.selectbox("Select Year:", df['Year'].unique())
    with col_participation:
        participation_range = st.slider("Select Participation Rate Range:", 0, 100, (0, 100))

    # Filter data based on selections
    filtered_data = df[(df['State/territory'] == state_option) & (df['Year'] == year_option) & (df['Participation (%)'] >= participation_range[0]) & (df['Participation (%)'] <= participation_range[1])]
    
    # First row: Creating columns for the donut charts
    col1, col2, col3 = st.columns(3)
    with col1:
        create_language_vs_participation_plot(filtered_data)
    with col2:
        create_birthplace_donut_chart(filtered_data)
    with col3:
        create_indigenous_population_chart(filtered_data)

    # Second row: Scatter plot spanning two rows in height, with two smaller columns for tables
    col4, col5 = st.columns([3, 1])  # Adjusting the layout: scatter plot gets more space
    with col4:
        create_income_vs_participation_plot(filtered_data)

    # Additional column for tables
    with col5:
        st.write("#### Higher Education Proportion")
        education_proportion_data = create_education_proportion_table(filtered_data)
        st.table(education_proportion_data.style.format({
            '% Higher Education': '{:.2f}%',
            '% Not Higher Education': '{:.2f}%'
        }))

        st.write("#### Gender")
        gender_data = create_gender_table(filtered_data)
        st.table(gender_data)