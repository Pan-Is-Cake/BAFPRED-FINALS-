import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import time  # Import time for delay functionality

# Add title at the top of the page
st.title("Martha's Kidnapping Investigation")

# Sample data for Martha
martha_df = pd.DataFrame({
    'Day': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
    'Office Clock In': [900, 905, np.nan, 910, 920],
    'Office Clock Out': [1800, 1815, 1800, 1810, np.nan],
    'Parking Lot Clock In': [850, 855, 860, 850, 870],
    'Parking Lot Clock Out': [1850, 1900, 1855, 1905, 1920]
})

# Set up the session state to track the step
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'wrong_attempt' not in st.session_state:
    st.session_state.wrong_attempt = False

# Part 1: Data Cleaning Step
if st.session_state.step == 1 and not st.session_state.game_over:
    st.title("Step 1: Clean the Data")
    st.write("Here is the raw data for Martha:")
    st.write(martha_df)
    
    # Data Cleaning Process
    st.write("Data with missing values:")
    st.write(martha_df)
    
    columns_to_clean = st.multiselect("Select columns to clean", martha_df.columns)
    fill_method = st.selectbox("Choose how to handle missing data", ["Mean", "Median", "Remove"])

    if fill_method == "Mean":
        martha_df[columns_to_clean] = martha_df[columns_to_clean].fillna(martha_df[columns_to_clean].mean())
        st.write("Missing values have been filled with the mean of the selected columns.")
    elif fill_method == "Median":
        martha_df[columns_to_clean] = martha_df[columns_to_clean].fillna(martha_df[columns_to_clean].median())
        st.write("Missing values have been filled with the median of the selected columns.")
    elif fill_method == "Remove":
        martha_df = martha_df.dropna(subset=columns_to_clean)
        st.write("Rows with missing values in the selected columns have been removed.")

    # Display cleaned data
    st.write("Cleaned data:")
    st.write(martha_df)

    # Clue buttons for data cleaning
    if st.button("Clue 1: What should I fill missing values with?"):
        st.write("Clue: Try filling missing values with the mean or median of the column to keep the data consistent.")

    if st.button("Clue 2: What happens if I remove missing values?"):
        st.write("Clue: Removing rows with missing values might cause data loss. Ensure the dataset is still useful.")

    if st.button("Clue 3: Why is data cleaning important?"):
        st.write("Clue: Cleaning the data ensures that the analysis or model is based on reliable and accurate information.")

    if st.button("Next: Perform Regression Analysis"):
        st.session_state.step = 2  # Move to next step

# Part 2: Regression Analysis Step
elif st.session_state.step == 2:
    st.title("Step 2: Perform Regression Analysis")
    
    # Manually map the days to numeric values (Monday = 0, ..., Friday = 4)
    day_map = {
        'Monday': 0,
        'Tuesday': 1,
        'Wednesday': 2,
        'Thursday': 3,
        'Friday': 4
    }
    martha_df['Day'] = martha_df['Day'].map(day_map)

    # Handle missing values in the dependent variable (y) by removing or filling them
    martha_df = martha_df.dropna(subset=['Office Clock In'])

    # Now 'Day' is a numeric column
    X = martha_df['Day'].values.reshape(-1, 1)  # Independent variable (Day of the week)
    y = martha_df['Office Clock In'].values  # Dependent variable (Office Clock In time)

    # Initialize the Linear Regression model
    model = LinearRegression()

    try:
        # Perform linear regression
        model.fit(X, y)
        slope = model.coef_[0]
        intercept = model.intercept_

        # Display the regression equation
        st.write(f"Regression Equation: y = {slope:.2f}x + {intercept:.2f}")

        # Predict the clock-in times based on the regression model
        predictions = model.predict(X)

        # Display predictions
        st.write("Predicted Office Clock In Times:")
        st.write(predictions)

        # Plot the predictions (using streamlit's line chart)
        st.line_chart(predictions)

    except Exception as e:
        st.write(f"Error in regression analysis: {e}")
    
    if st.button("Next: Guess the Suspect"):
        st.session_state.step = 3  # Move to the final step

# Part 3: Guess the Suspect Step
elif st.session_state.step == 3:
    st.title("Step 3: Guess the Suspect")
    
    suspects = ['Suspect 1', 'Suspect 2', 'Suspect 3']
    selected_suspect = st.selectbox('Who do you think kidnapped Martha?', suspects)

    correct_suspect = 'Suspect 1'  # Example, change it as needed

    if st.button("Submit Guess"):
        if selected_suspect == correct_suspect:
            st.session_state.game_over = True  # Mark the game as over
            st.write(f"Correct! {correct_suspect} kidnapped Martha.")
        else:
            st.write(f"Incorrect. {selected_suspect} is not the kidnapper.")
            st.write("Returning to Step 1...")
            time.sleep(3)  # Add a 3-second delay
            st.session_state.step = 1  # Reset to Step 1 if the answer is wrong

# Part 4: Game Over Section
if st.session_state.game_over:
    st.title("Congratulations!")
    st.write("You successfully solved the case and identified the kidnapper!")
