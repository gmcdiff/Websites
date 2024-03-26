import pandas as pd
import numpy as np
from sqlalchemy import create_engine

# Load the Excel file into a DataFrame
df = pd.read_excel('megaGymDataset.xlsx')
print(df.head)

# Define the dictionary mapping old values to the new value
replace_legs = {'Adductors': 'Legs', 'Abductors': 'Legs', 'Hamstrings': 'Legs', 'Glutes': 'Legs', 'Quadriceps': 'Legs'}
replace_back = {'Lower Back': 'Back', 'Middle Back': 'Back'}

# Use the .replace() method to replace old values with the new value
df['BodyPart'] = df['BodyPart'].replace(replace_legs)
df['BodyPart'] = df['BodyPart'].replace(replace_back)
df['Equipment'] = df['Equipment'].replace('Body Only','Bodyweight')

# Define conditions for replacing 'None' based on different types
stretching_condition = (df['Type'] == 'Stretching')
plyometrics_condition = (df['Type'] == 'Plyometrics')

# Replace 'None' with 'Stretching Mat' where 'Type' is 'Stretching'
df['Equipment'] = np.where(stretching_condition & (df['Equipment'] == 'None'), 'Stretching Mat', df['Equipment'])

# Replace 'None' with 'Plyo' where 'Type' is 'Plyometrics'
df['Equipment'] = np.where(plyometrics_condition & (df['Equipment'] == 'None'), 'Plyos', df['Equipment'])

# Drop rows where 'Equipment' is still 'None'
df.drop(df[df['Equipment'] == 'None'].index, inplace=True)

# Drop rows where column_name has value_to_remove
df = df.drop(df[df['BodyPart'] == 'Neck'].index)
df = df.drop(df[df['Equipment'] == 'Other'].index)
df = df.drop(df[df['Equipment'] == 'Medicine Ball'].index)
df = df.drop(df[df['Equipment'] == 'E-Z Curl Bar'].index)

# Save the changes to the Excel file
df.to_excel('megaGymDataset.xlsx', index=False)

unique_values = df['Equipment'].unique()
print(unique_values)

# Get the count of each unique value in the 'Equipment' column
level_counts = df['Level'].value_counts()

# Print the counts
print(level_counts)

# Connect to your database (replace 'sqlite:///your_database.db' with your database URI)
engine = create_engine('sqlite:///workout.db')

# Assuming df is your DataFrame
df.to_sql('Exercises', engine, if_exists='replace', index=False)