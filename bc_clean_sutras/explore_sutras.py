import pandas as pd

# Load the CSV with the scraped sutras
sutrast_dataframe = pd.read_csv('sutras.csv')

# Explore the first few rows
#print(sutrast_dataframe.head())

# Check for any missing or invalid data
#print(sutrast_dataframe.isnull().sum())  # Count missing values in each column

#Sort df for only relevent content
sutras_content = sutrast_dataframe['content']
print(sutras_content.head())