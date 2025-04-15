# Thomas Apke, Gavin Clifton, Ben Funk, Sam Jenson, Mary Catherine Shepherd
# Assume you are given a sample of sale data from an online retailer in the form of an excel file.
# The retailer wants your team to test how they could transfer their data into a postgres database
# and read data programmatically back from the database.

import sqlalchemy
import pandas as pd
import matplotlib.pyplot as plot
import psycopg2

inputOrSum = input("If you want to import data, enter 1. If you want to see summaries of stored data, enter 2. Enter any other value to exit the program.")
if inputOrSum == 1:
    salesData = pd.read_excel("/Users/samjenson/Downloads/Retail_Sales_Data.xlsx")
    
elif inputOrSum == 2:
    pass
else:
    pass