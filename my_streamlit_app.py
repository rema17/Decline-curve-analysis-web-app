import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Arps Decline Curve Equations
def exponential_decline(t, qi, di):
    return qi * np.exp(-di * t)

def hyperbolic_decline(t, qi, di, b):
    return qi / (1 + b * di * t)**(1 / b)

def harmonic_decline(t, qi, di):
    return qi / (1 + di * t)

st.title("Decline Curve Analysis with Arps Model")

# Introduction
st.write("My name is Reema Omar and I am a petroleum engineer.")
st.write("This app performs decline curve analysis using the Arps model.")

# Sidebar: Upload data and select analysis type
st.sidebar.header("Upload Data")
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")
analysis_type = st.sidebar.selectbox(
    "Select the decline curve analysis type",
    options=["Exponential", "Hyperbolic", "Harmonic"],
)

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.write("Data preview:")
    st.write(data.head())

    # Check if data has required columns ('time' and 'production')
    if "time" in data.columns and "production" in data.columns:
        time = data["time"].values
        production = data["production"].values

        # Curve fitting
        if analysis_type == "Exponential":
            popt, _ = curve_fit(exponential_decline, time, production, maxfev=10000)
            qi, di = popt
            st.write(f"Initial production rate, q_i: {qi:.2f}")
            st.write(f"Decline rate, d_i: {di:.2e}")
            fitted_production = exponential_decline(time, qi, di)
        elif analysis_type == "Hyperbolic":
            popt, _ = curve_fit(hyperbolic_decline, time, production, maxfev=10000)
            qi, di, b = popt
            st.write(f"Initial production rate, q_i: {qi:.2f}")
            st.write(f"Decline rate, d_i: {di:.2e}")
            st.write(f"Hyperbolic exponent, b: {b:.2f}")
            fitted_production = hyperbolic_decline(time, qi, di, b)
        else:
            popt, _ = curve_fit(harmonic_decline, time, production, maxfev=10000)
            qi, di = popt
            st.write(f"Initial production rate, q_i: {qi:.2f}")
            st.write(f"Decline rate, d_i: {di:.2e}")
            fitted_production = harmonic_decline(time, qi, di)

        # Plotting the decline curve analysis
        plt.plot(time, production, "ro", label="Observed Production")
        plt.plot(time, fitted_production, "b-", label="Fitted Decline Curve")
        plt.xlabel("Time")
        plt.ylabel("Production")
        plt.legend()
        st.pyplot(plt.gcf())
    else:
        st.error("Data must have columns 'time' and 'production'.")
else:
    st.warning("Please upload a CSV file.")