# home.py
import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="Agentic AI Portfolio",
    page_icon="🤖",
    layout="wide"
)

# Sidebar for navigation
st.sidebar.title("Navigation")
app_choice = st.sidebar.radio(
    "Choose an App",
    ["Home", "Rent Price Prediction", "Research Summary", "Signature Verification", "Data Analysis", "Personalized Fitness & Meal Plan Recommender"]
)

# Home Page
if app_choice == "Home":
    st.title("Welcome to My Agentic AI Portfolio! 🚀")
    st.write("""
    This portfolio showcases my AI projects and applications. Use the navigation bar on the left to explore the apps:
    
    - **Rent Price Prediction**: Predict rental prices based on features.
    - **Research Summary**: Summarize research papers or articles.
    - **Signature Verification**: Verify handwritten signatures.
    """)

# Rent Price Prediction App
elif app_choice == "Rent Price Prediction":
    # Import and run the Rent Price Prediction app
    from rent_price_pridiction_app import main as rent_price_main
    rent_price_main()

# Research Summary App
elif app_choice == "Research Summary":
    # Import and run the Research Summary app
    from research_sum_app import main as research_sum_main
    research_sum_main()

# Signature Verification App
elif app_choice == "Signature Verification":
    # Import and run the Signature Verification app
    from signature_verification_app import main as signature_verification_main
    signature_verification_main()

# data analysis 
elif app_choice == "Data Analysis":
    # Import and run the Signature Verification app
    from data_analyst_app import main as data_analyst_main
    data_analyst_main()

# data analysis 
elif app_choice == "Personalized Fitness & Meal Plan Recommender":
    # Import and run the Signature Verification app
    from fitness_app import main as fitness_main
    fitness_main()
    