import streamlit as st
from streamlit_option_menu import option_menu

# Importing page functions from different modules
from data_visualisation.bowel_cancer.temporal import temporal_page_bc as bowel_temporal_app
from data_visualisation.breast_cancer.temporal import temporal_page_brc as breast_temporal_app
from data_visualisation.cervical_cancer.temporal import temporal_page_cc as cervical_temporal_app

from data_visualisation.bowel_cancer.geographic import geographical_tab_bc  
from data_visualisation.breast_cancer.geographic import geographical_tab_brc  
from data_visualisation.cervical_cancer.geographic import geographical_tab_cc  

from data_visualisation.bowel_cancer.demographic import demographic_page_bc  
from data_visualisation.breast_cancer.demographic import demographic_page_brc  
from data_visualisation.cervical_cancer.demographic import demographic_page_cc

from machine_learning.models.cervical_cancer import cervical_cancer
from machine_learning.models.breast_cancer import breast_cancer
from machine_learning.models.bowel_cancer import bowel_cancer 

def show_home():
    st.write("""
    # Welcome to the Cancer Screening Analysis Tool
    ## Understanding Socio-economic Factors Affecting Cancer Screening Participation in Australia

    This interactive tool is designed to provide health professionals, researchers, and policy-makers with detailed insights into cancer screening participation across Australia. By analyzing various socio-economic and demographic factors, this application aims to identify key trends, barriers, and opportunities to enhance screening outreach and effectiveness.

    ### Australia's National Cancer Screening Programs
    This application focuses on the three main national cancer screening programs in Australia, which are critical components of the country's public health strategy:

    - **Bowel Cancer Screening Program**: Aimed at detecting early signs of bowel cancer, this program provides free screening kits to Australians within the eligible age range. Early detection can significantly improve treatment outcomes.
    - **BreastScreen Australia**: This program offers free mammography screening every two years to all women aged 50 to 74, aiming to detect early stages of breast cancer. Regular screening is crucial as it can detect cancers before they can be felt or cause symptoms.
    - **Cervical Screening Program**: Replacing the traditional Pap test, the new Cervical Screening Test is more effective at preventing cervical cancers and is offered free to women aged 25 to 74 every five years.

    ### Key Features of the Application:
    - **Demographic Analysis**: Examine how participation rates vary by sex, age, and other demographic factors. This analysis helps understand which groups are underserved and how tailored interventions could improve uptake.
    - **Geographic Trends**: Utilize GIS data to identify areas with lower participation rates. This feature assists in pinpointing geographic disparities in screening uptake and can guide regional health campaigns.
    - **Temporal Trends**: Analyze how participation rates have changed over time, reflecting on the impact of public health initiatives and policy changes. This helps in understanding the effectiveness of past actions and planning future strategies.
    - **Effectiveness of Outreach**: Assess the impact of different outreach efforts by comparing the number of invitations issued to the number of screenings completed. This feature aims to evaluate and optimize communication strategies.

    ### How to Use This Tool:
    Navigate through the app using the menu above to explore different analyses and predictions. Each section provides interactive visualizations and data-driven insights that can help in making informed decisions about cancer screening programs.

    ### Additional Resources:
    - **Chatbot Assistance**: Get quick answers to common questions about cancer screenings through our interactive chatbot.
    - **Latest Research and Data**: Access up-to-date research findings and raw datasets used in our analyses to perform your own detailed studies.

    We hope this tool empowers you with the information needed to improve cancer screening outcomes and reduce the burden of cancer across communities. Your feedback is invaluable in helping us enhance this tool further.
    """)


import streamlit as st
from streamlit_option_menu import option_menu

def main():
    st.set_page_config(page_title="Cancer Screening App", layout="wide")

    # Top-level horizontal menu
    top_level_selection = option_menu(None, ["Home", "Data Visualisation", "Machine Learning Prediction"],
                                      icons=['house', 'bar-chart-line', 'cpu'],
                                      menu_icon="cast", default_index=0, orientation="horizontal")

    if top_level_selection == "Home":
        show_home()

    elif top_level_selection == "Data Visualisation":
        # Second-level horizontal menu for cancer types
        cancer_type = option_menu(None, ["Bowel Cancer", "Breast Cancer", "Cervical Cancer"],
                                  icons=['clipboard-data', 'clipboard-data', 'clipboard-data'],
                                  menu_icon="cast", default_index=0, orientation="horizontal")
        
        # Third-level horizontal menu for analysis types
        if cancer_type == "Bowel Cancer":
            analysis_type = option_menu(None, ["Temporal", "Demographic", "Geographic"],
                                        icons=['clock-history', 'people', 'geo-alt'], 
                                        menu_icon="cast", default_index=0, orientation="horizontal")
            if analysis_type == "Temporal":
                bowel_temporal_app()
            elif analysis_type == "Demographic":
                demographic_page_bc()
            elif analysis_type == "Geographic":
                geographical_tab_bc()

        elif cancer_type == "Breast Cancer":
            analysis_type = option_menu(None, ["Temporal", "Demographic", "Geographic"],
                                        icons=['clock-history', 'people', 'geo-alt'], 
                                        menu_icon="cast", default_index=0, orientation="horizontal")
            if analysis_type == "Temporal":
                breast_temporal_app()
            elif analysis_type == "Demographic":
                demographic_page_brc()
            elif analysis_type == "Geographic":
                geographical_tab_brc()

        elif cancer_type == "Cervical Cancer":
            analysis_type = option_menu(None, ["Temporal", "Demographic", "Geographic"],
                                        icons=['clock-history', 'people', 'geo-alt'], 
                                        menu_icon="cast", default_index=0, orientation="horizontal")
            if analysis_type == "Temporal":
                cervical_temporal_app()
            elif analysis_type == "Demographic":
                demographic_page_cc()
            elif analysis_type == "Geographic":
                geographical_tab_cc()

    elif top_level_selection == "Machine Learning Prediction":
            # Placeholder for machine learning prediction page
            #st.write("Machine Learning Prediction will be here")
            # Second-level horizontal menu for cancer types
         predictive_model_type = option_menu(None, ["Cervical Cancer", "Breast Cancer", "Bowel Cancer" ],
                                  icons=['clipboard2-pulse', 'clipboard2-plus', 'clipboard2-pulse-fill'],
                                  menu_icon="cast", default_index=0, orientation="horizontal")
         if predictive_model_type == "Cervical Cancer":
           cervical_cancer()
         elif predictive_model_type == "Breast Cancer":
            breast_cancer()
         elif predictive_model_type == "Bowel Cancer":
            bowel_cancer()
if __name__ == "__main__":
    main()
