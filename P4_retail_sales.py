# Thomas Apke, Gavin Clifton, Ben Funk, Sam Jenson, Mary Catherine Shepherd
# Assume you are given a sample of sale data from an online retailer in the form of an excel file.
# The retailer wants your team to test how they could transfer their data into a postgres database
# and read data programmatically back from the database.

from sqlalchemy import create_engine, text
import pandas as pd
import matplotlib.pyplot as plot
import psycopg2
import openpyxl

 # Step 4
username = 'postgres'
password = 'admin'
host = 'localhost'
port = '5433'
database = 'is303'

engine = create_engine(f'postgresql://{username}:{password}@{host}:{port}/{database}')

conn = engine.connect()

# setting up our if statement to help us run the rest of the program
inputOrSum = int(input("If you want to import data, enter 1. If you want to see summaries of stored data, enter 2. Enter any other value to exit the program."))
if inputOrSum == 1:
#     importing the original excel file
    salesData = pd.read_excel("/Users/samjenson/Downloads/Retail_Sales_Data.xlsx")
#     seperating our names into multiple columns
    seperatedNames = salesData['name'].str.split("_", expand = True)
    salesData.insert(1, 'First Name', seperatedNames[0])
    salesData.insert(2, 'Last Name', seperatedNames[1])
    salesData.drop('name', axis=1, inplace=True)
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
    salesData['category'] = salesData['product'].map(productCategoriesDict)

    salesData['total_price'] = salesData['quantity_sold'] * salesData['unit_price']

    salesData.to_sql("sales", conn, if_exists='replace', index=False)

    # Step 5
    print("You've imported the excel file into your postgres database.")

elif inputOrSum == 2:
    print('The following are all the categories that have been sold:')

    query = 'SELECT DISTINCT category FROM sales ORDER BY category;'
    dfCategories = pd.read_sql(text(query), conn)

    dictCategories = {}
    for iCount, category in enumerate(dfCategories['category'], start=1):
        dictCategories[iCount] = category
        print(f'{iCount}: {category}')

    choice_category = input('Please enter the number of the category you want to see summarized: ')

    if choice_category.isdigit():
        selected_category = dictCategories[int(choice_category)]

        # Correct query to filter by category
        filter_query = text("SELECT * FROM sales WHERE category = :cat")
        df = pd.read_sql(filter_query, conn, params={"cat": selected_category})

        iTotalSales = df["total_price"].sum()
        iAverageSales = df["total_price"].mean()
        iUnitsSold = df["quantity_sold"].sum()

        print(f"Total sales for {selected_category}: {iTotalSales}")
        print(f"Average sale amount for {selected_category}: {iAverageSales}")
        print(f"Total units sold for {selected_category}: {iUnitsSold}")

        dfProductSales = df.groupby('product')['total_price'].sum()

        dfProductSales.plot(kind='bar')
        plot.title(f"Total sales in {selected_category}")
        plot.xlabel("Product")
        plot.ylabel("Total Sales")
        plot.tight_layout()
        plot.show()

    print("Closing the program")
