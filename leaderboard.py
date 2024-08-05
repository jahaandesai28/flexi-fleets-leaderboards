import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def process_data(file):
    # Load the Excel file
    df_payouts = pd.read_excel(file, sheet_name='Compiled_Payouts_and_OPH')
    df_login_hours = pd.read_excel(file, sheet_name='Compiled_Login_Hours')
    
    # Merge the dataframes on ID and Name
    df = pd.merge(df_payouts, df_login_hours[['ID', 'TotalLoginHours', 'AVG_weekly_login_hours']], on='ID')
    
    # Normalize the metrics for composite score calculation
    metrics = ['TotalOrders', 'TotalPayout', 'TotalLoginHours', 'AVG_weekly_login_hours']
    df_normalized = df.copy()
    for col in metrics:
        df_normalized[col] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())
    
    # Calculate the composite index
    df['Composite_Score'] = df_normalized[metrics].mean(axis=1)
    
    return df

def create_bar_chart(df, sort_by):
    df_sorted = df.sort_values(by=sort_by, ascending=False)
    plt.figure(figsize=(10, 8))
    plt.barh(df_sorted['Name'], df_sorted[sort_by], color='skyblue')
    plt.xlabel(sort_by)
    plt.ylabel('Rider Name')
    plt.title(f'Riders Sorted by {sort_by}')
    plt.gca().invert_yaxis()
    st.pyplot(plt)

st.title("Rider Leaderboard")

uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")

if uploaded_file is not None:
    df = process_data(uploaded_file)
    
    sort_options = ['TotalOrders', 'TotalPayout', 'TotalLoginHours', 'AVG_weekly_login_hours', 'Composite_Score']
    sort_by = st.selectbox('Sort riders by:', sort_options)
    
    create_bar_chart(df, sort_by)
    
    # Create a leaderboard
    leaderboard = df[['ID', 'Name', sort_by]].sort_values(by=sort_by, ascending=False).reset_index(drop=True)
    leaderboard.index += 1
    st.write("Leaderboard")
    st.dataframe(leaderboard)
