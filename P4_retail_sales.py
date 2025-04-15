# Thomas Apke, Gavin Clifton, Ben Funk, Sam Jenson, Mary Catherine Shepherd
# Assume you are given a sample of sale data from an online retailer in the form of an excel file.
# The retailer wants your team to test how they could transfer their data into a postgres database
# and read data programmatically back from the database.

from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plot
import psycopg2

# Step 3
productCategoriesDict = {
        'Camera': 'Technology',
        'Laptop': 'Technology',
        'Gloves': 'Apparel',
        'Smartphone': 'Technology',
        'Watch': 'Accessories',
        'Backpack': 'Accessories',
        'Water Bottle': 'Household Items',
        'T-shirt': 'Apparel',
        'Notebook': 'Stationery',
        'Sneakers': 'Apparel',
        'Dress': 'Apparel',
        'Scarf': 'Apparel',
        'Pen': 'Stationery',
        'Jeans': 'Apparel',
        'Desk Lamp': 'Household Items',
        'Umbrella': 'Accessories',
        'Sunglasses': 'Accessories',
        'Hat': 'Apparel',
        'Headphones': 'Technology',
        'Charger': 'Technology'}

df['category'] = df['product'].map(productCategoriesDict)


# Step 4
username = 'postgres'
password = 'admin'
host = 'localhost'
port = '5433'
database = 'is303'

engine = create_engine(f'postgresql://{username}:{password}@{host}:{port}/{database}')

conn = engine.connect()

dfImportedFile.to_sql("sale", conn, if_exists='replace', index=False)


# Step 5
print("You've imported the excel file into your postgres database.")