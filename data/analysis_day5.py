#!/usr/bin/env python
# coding: utf-8

# In[4]:


import pandas as pd

df = pd.read_csv("olist_customers_dataset.csv")

print("Dataset loaded successfully!")
print("Rows and columns:", df.shape)


# In[7]:


# Display first five rows
display(df.head())

# Display last five rows
display(df.tail())

# Check data types, non-null counts and memory usage
df.info()

# Statistical summary
display(df.describe())

# Count customers by state
print(df["customer_state"].value_counts().head(10))


# In[8]:


# Select relevant customer location columns
location_data = df[
    ["customer_city", "customer_state"]
]

display(location_data.head())

# Filter customers whose state is SP
sp_customers = df[df["customer_state"] == "SP"]

print("Customer records in SP:", len(sp_customers))
display(sp_customers.head())

# Find customer records with ZIP-code prefixes above 90000
high_zip_prefix = df[
    df["customer_zip_code_prefix"] > 90000
]

display(high_zip_prefix.head())


# In[9]:


# Count missing values in each column
print("Missing values:")
print(df.isnull().sum())

# Count duplicate rows
print("Duplicate rows:", df.duplicated().sum())

# Check duplicate customer IDs
print("Duplicate customer IDs:",
      df["customer_id"].duplicated().sum())

# Create a cleaned copy
df_clean = df.drop_duplicates().copy()

print("Shape before cleaning:", df.shape)
print("Shape after cleaning:", df_clean.shape)


# In[10]:


state_summary = (
    df.groupby("customer_state")
      .agg(
          customer_records=("customer_id", "count"),
          unique_customers=("customer_unique_id", "nunique"),
          cities=("customer_city", "nunique")
      )
      .sort_values(
          "customer_records",
          ascending=False
      )
      .reset_index()
)

display(state_summary.head(10))


# In[11]:


city_summary = (
    df.groupby("customer_city")
      .agg(
          customer_records=("customer_id", "count"),
          states=("customer_state", "nunique")
      )
      .sort_values(
          "customer_records",
          ascending=False
      )
      .head(10)
      .reset_index()
)

display(city_summary)


# In[13]:


df_clean.to_csv(
    "olist_customers_cleaned.csv",
    index=False
)

print("Cleaned dataset exported successfully!")


# ### Conclusion
# 
# Exploratory Data Analysis was performed on the Olist customer dataset using Python and Pandas. The dataset contains 99,441 records and five columns describing customer identifiers and locations.
# 
# The analysis found no missing values or fully duplicated rows. São Paulo state had the highest number of customer records, with 41,746 records, while São Paulo city was the most represented city, with 15,540 records.
# 
# The analysis also identified 96,096 distinct customer identifiers across 99,441 records. This suggests that some customer identifiers occur more than once and may warrant further investigation using order-level data.
# 

# In[ ]:




