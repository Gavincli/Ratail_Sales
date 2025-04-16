# Thomas Apke, Gavin Clifton, Ben Funk, Sam Jenson, Mary Catherine Shepherd
# Assume you are given a sample of sale data from an online retailer in the form of an excel file.
# The retailer wants your team to test how they could transfer their data into a postgres database
# and read data programmatically back from the database.

import sqlalchemy
import pandas as pd
import matplotlib.pyplot as plot
import psycopg2


product_sales.plot(kind='bar')

plot.title(f"Total Sales by Product in {selected_category}")
plot.xlabel("Product")
plot.ylabel("Total Sales")
plot.tight_layout()  # Neaten up spacing
plot.show() 