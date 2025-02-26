import streamlit as st
import pandas as pd
import numpy as np

def calculate_bmi(weight, height):
    height_m = height / 100  # Convert cm to meters
    return round(weight / (height_m ** 2), 2)

def get_fitness_plan(goal, activity_level):
    plans = {
        "Weight Loss": {
            "Low": "Walking, Yoga, Light Cardio",
            "Medium": "Running, HIIT, Strength Training",
            "High": "CrossFit, Intense Cardio, Advanced Weightlifting"
        },
        "Muscle Gain": {
            "Low": "Bodyweight Exercises, Light Resistance Training",
            "Medium": "Strength Training, Hypertrophy Workouts",
            "High": "Heavy Weightlifting, High-Intensity Strength Workouts"
        },
        "General Fitness": {
            "Low": "Daily Walks, Light Aerobics",
            "Medium": "Mixed Cardio and Strength Workouts",
            "High": "Advanced Functional Training"
        }
    }
    return plans.get(goal, {}).get(activity_level, "Custom Plan Needed")

def get_meal_plan(goal, preference):
    meal_plans = {
        "Weight Loss": {
            "Vegetarian": "Salads, Lentils, Low-Carb Meals",
            "Non-Vegetarian": "Grilled Chicken, Fish, Lean Meats",
            "Vegan": "Quinoa, Tofu, Nuts, Low-Carb Options"
        },
        "Muscle Gain": {
            "Vegetarian": "High-Protein Lentils, Paneer, Nuts",
            "Non-Vegetarian": "Eggs, Chicken, Beef, High-Calorie Diet",
            "Vegan": "Plant-Based Protein, Soy, Chickpeas"
        },
        "General Fitness": {
            "Vegetarian": "Balanced Diet with Whole Grains & Proteins",
            "Non-Vegetarian": "Balanced Diet with Lean Proteins & Carbs",
            "Vegan": "Plant-Based Balanced Diet"
        }
    }
    return meal_plans.get(goal, {}).get(preference, "Custom Diet Needed")

st.title("🏋️ Personalized Fitness & Meal Plan Recommender 🍎")

# User Input Form
st.sidebar.header("User Information")
age = st.sidebar.number_input("Age", min_value=10, max_value=100, value=25)
weight = st.sidebar.number_input("Weight (kg)", min_value=30, max_value=200, value=70)
height = st.sidebar.number_input("Height (cm)", min_value=100, max_value=250, value=170)
activity_level = st.sidebar.selectbox("Activity Level", ["Low", "Medium", "High"])
fitness_goal = st.sidebar.selectbox("Fitness Goal", ["Weight Loss", "Muscle Gain", "General Fitness"])
diet_preference = st.sidebar.selectbox("Dietary Preference", ["Vegetarian", "Non-Vegetarian", "Vegan"])

if st.sidebar.button("Generate Plan"):
    bmi = calculate_bmi(weight, height)
    fitness_plan = get_fitness_plan(fitness_goal, activity_level)
    meal_plan = get_meal_plan(fitness_goal, diet_preference)
    
    st.subheader("📊 Health Report")
    st.write(f"**BMI:** {bmi} (Normal: 18.5 - 24.9)")
    
    st.subheader("🏋️ Recommended Workout Routine")
    st.write(f"{fitness_plan}")
    
    st.subheader("🍽️ Personalized Meal Plan")
    st.write(f"{meal_plan}")
    
    st.success("Plan Generated Successfully!")
