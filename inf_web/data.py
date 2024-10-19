import pandas as pd
import sqlite3

file_path = 'All_data_FIW_2013-2024.xlsx'
data = pd.read_excel(file_path, sheet_name='FIW13-24')

data.columns = data.iloc[0]
data = data[1:]

country_df = data[['Country/Territory', 'Region', 'Status']].copy()
country_df.drop_duplicates(subset=['Country/Territory'], inplace=True)
country_df['Country_ID'] = range(1, len(country_df) + 1)

ratings_df = data[['Country/Territory', 'Edition', 'PR rating', 'CL rating', 'Total']].copy()
ratings_df = ratings_df.merge(country_df[['Country/Territory', 'Country_ID']], on='Country/Territory')
ratings_df.rename(columns={'Edition': 'Year', 'PR rating': 'PR_Rating', 'CL rating': 'CL_Rating', 'Total': 'Total_Score'}, inplace=True)
ratings_df.drop(columns=['Country/Territory'], inplace=True)
ratings_df['Rating_ID'] = range(1, len(ratings_df) + 1) 

connection = sqlite3.connect('rankings_database.db')
cursor = connection.cursor()

cursor.execute("DROP TABLE IF EXISTS Country")
cursor.execute("DROP TABLE IF EXISTS Ratings")

cursor.execute('''
    CREATE TABLE Country (
        Country_ID INTEGER PRIMARY KEY,
        Country_Name TEXT,
        Region TEXT,
        Status TEXT
    )
''')

cursor.execute('''
    CREATE TABLE Ratings (
        Rating_ID INTEGER PRIMARY KEY,
        Country_ID INTEGER,
        Year INTEGER,
        PR_Rating INTEGER,
        CL_Rating INTEGER,
        Total_Score INTEGER,
        FOREIGN KEY (Country_ID) REFERENCES Country (Country_ID)
    )
''')

country_df.rename(columns={'Country/Territory': 'Country_Name'}, inplace=True)
country_df.to_sql('Country', connection, if_exists='append', index=False)
ratings_df.to_sql('Ratings', connection, if_exists='append', index=False)

connection.commit()
connection.close()