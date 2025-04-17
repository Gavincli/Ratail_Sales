# Thomas Apke, Gavin Clifton, Ben Funk, Sam Jenson, Mary Catherine Shepherd
# Assume you are given a sample of sale data from an online retailer in the form of an excel file.
# The retailer wants your team to test how they could transfer their data into a postgres database
# and read data programmatically back from the database.

from sqlalchemy import create_engine, text
import pandas as pd
import matplotlib.pyplot as plot
import psycopg2
import openpyxl


#setup for use in both options:
# Step 4
username = 'postgres'
password = 'admin'
host = 'localhost'
port = '5432'
database = 'is303'

engine = create_engine(f'postgresql://{username}:{password}@{host}:{port}/{database}')

conn = engine.connect()


# setting up our if statement to help us run the rest of the program
inputOrSum = int(input("If you want to import data, enter 1. If you want to see summaries of stored data, enter 2. Enter any other value to exit the program."))
if inputOrSum == 1:
#     importing the original excel file
        dfImportedFile = pd.read_excel(r"C:\Users\gavin\Downloads\Retail_Sales_Data.xlsx")
#     seperating our names into multiple columns
        seperatedNames = dfImportedFile['name'].str.split("_", expand = True)
        dfImportedFile.insert(1, 'First Name', seperatedNames[0])
        dfImportedFile.insert(2, 'Last Name', seperatedNames[1])
        dfImportedFile.drop('name', axis=1, inplace=True)

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
        dfImportedFile['category'] = dfImportedFile['product'].map(productCategoriesDict)

        dfImportedFile.to_sql("sale", conn, if_exists='replace', index=False)


        # Step 5
        print("You've imported the excel file into your postgres database.")

elif inputOrSum == 2:
        """category_df = dfImportedFile.query("category == @category")

        iTotalSales = category_df["total_price"].sum()
        iAverageSales = category_df["total_price"].mean()
        iUnitsSold = category_df["quantity_sold"].sum()"""


        #Part 2 step 1
        #print instructions
        print('The following are all the categories that have been sold:')

        #step 2
        #query for the distinct categories, print a numbered list
        query = 'SELECT DISTINCT category FROM sales ORDER BY category;'
        dfCategories = pd.read_sql( text(query), conn)

        print('Read sql')

        #assign numbers and create dictionary
        dictCategories = {}
        for iCount, category in enumerate(dfCategories['category'], start = 1):
                dictCategories[iCount] = category
                print(f'{iCount}: {category}')

        #step 3
        #receive input for which category to summarize
        choice_category = input('Please enter the number of the category you want to see summarized: ')

        if choice_category.isdigit():
                category = dictCategories[choice_category]

        #df isn't defined?
        category_df = df.query("category == @category")

        iTotalSales = category_df["total_price"].sum()
        iAverageSales = category_df["total_price"].mean()
        iUnitsSold = category_df["quantity_sold"].sum()

        print(f"Total sales for {category}: {iTotalSales}")
        print(f"Average sale amount for {category}: {iAverageSales}")
        print(f"Total units sold for {category}: {iUnitsSold}")


        print(f"Total sales for {category}: {iTotalSales}")
        print(f"Average sale amount for {category}: {iAverageSales}")
        print(f"Total units sold for {category}: {iUnitsSold}")

else:
        print("Closing the program")