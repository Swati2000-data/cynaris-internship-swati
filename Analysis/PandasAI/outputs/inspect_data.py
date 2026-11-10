import pandas as pd

df = pd.read_csv("city_day.csv")

print("Dataset Shape:", df.shape)

print("\nFirst 5 Records:")
print(df.head())

print("\nColumn Names:")
print(df.columns.tolist())

print("\nData Types:")
print(df.dtypes)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nAQI Categories:")
print(df["AQI_Bucket"].value_counts(dropna=False))