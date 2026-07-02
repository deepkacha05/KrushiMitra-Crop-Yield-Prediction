# 🌾 KrushiMitra - Crop Yield Prediction System

## Project Overview

KrushiMitra is a Machine Learning based web application that predicts crop yield using agricultural data. The project helps farmers and researchers estimate crop production based on various factors such as state, crop type, season, area and production details.

This project was developed as an end-to-end Machine Learning project to understand the complete ML workflow including data preprocessing, exploratory data analysis, model building and deployment.

---

## Features

- Data Cleaning and Preprocessing
- Exploratory Data Analysis (EDA)
- Data Visualization
- Multiple Machine Learning Models
- Model Performance Comparison
- Crop Yield Prediction
- Interactive Streamlit Web Application

---

## Tech Stack

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-Learn
- Streamlit

---

## Machine Learning Models Used

- Linear Regression
- Decision Tree Regressor
- Random Forest Regressor

Final selected model: **Random Forest Regressor**

---

## Dataset Information

The dataset contains agricultural information from different states and districts of India.

Main features used:

- State
- District
- Crop
- Crop Year
- Season
- Area
- Production

Target Variable:

- Yield

---

## Project Structure

```text
KrushiMitra Crop Yield Prediction/
│
├── data/
│   └── crop_yield.csv
│
├── notebooks/
│   └── Crop_Yield_Prediction_Model.ipynb
│
├── models/
│   └── random_forest_model.pkl
│
├── app/
│   └── streamlit_app.py
│
├── assets/
│
├── requirements.txt
├── README.md
└── .gitignore