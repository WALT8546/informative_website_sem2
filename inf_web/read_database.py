import sqlite3
import pandas as pd
from pathlib import Path

path = Path(".")
database = path / "rankings_database.db"
conn = sqlite3.connect(database)

query_country = "SELECT * FROM Country"
query_ratings = "SELECT * FROM Ratings"

df_country = pd.read_sql_query(query_country, conn)
df_ratings = pd.read_sql_query(query_ratings, conn)

print("Country Table:")
print(df_country.head())

print("\nRatings Table:")
print(df_ratings.head())

df_country.to_csv("country_table_export.csv", index=False)
df_ratings.to_csv("ratings_table_export.csv", index=False)

conn.close()