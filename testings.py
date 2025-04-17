from sqlalchemy import create_engine, text
import pandas as pd
import matplotlib.pyplot as plt
import openpyxl

# Config for DB
username = 'postgres'
password = 'admin'
host = 'localhost'
port = '5433'
database = 'is303'
engine = create_engine(f'postgresql://{username}:{password}@{host}:{port}/{database}')
conn = engine.connect()

# Ask user
inputOrSum = int(input("If you want to import data, enter 1. If you want to see summaries of stored data, enter 2. Enter any other value to exit the program: "))

if inputOrSum == 1:
    # Load Excel file
    salesData = pd.read_excel("/Users/thoma/Downloads/Retail_Sales_Data.xlsx")
    
    # Split names
    separatedNames = salesData['name'].str.split("_", expand=True)
    salesData.insert(1, 'First Name', separatedNames[0])
    salesData.insert(2, 'Last Name', separatedNames[1])
    salesData.drop('name', axis=1, inplace=True)
    
    # Assign categories
    productCategoriesDict = {
        'Camera': 'Technology', 'Laptop': 'Technology', 'Gloves': 'Apparel',
        'Smartphone': 'Technology', 'Watch': 'Accessories', 'Backpack': 'Accessories',
        'Water Bottle': 'Household Items', 'T-shirt': 'Apparel', 'Notebook': 'Stationery',
        'Sneakers': 'Apparel', 'Dress': 'Apparel', 'Scarf': 'Apparel',
        'Pen': 'Stationery', 'Jeans': 'Apparel', 'Desk Lamp': 'Household Items',
        'Umbrella': 'Accessories', 'Sunglasses': 'Accessories', 'Hat': 'Apparel',
        'Headphones': 'Technology', 'Charger': 'Technology'
    }
    salesData['category'] = salesData['product'].map(productCategoriesDict)
    
    # Upload to DB
    salesData.to_sql("sales", conn, if_exists='replace', index=False)
    print("✅ Excel data successfully imported to the database.")

elif inputOrSum == 2:
    print("\nThe following are all the categories that have been sold:")

    # Fetch categories from DB
    query = 'SELECT DISTINCT category FROM sales ORDER BY category;'
    dfCategories = pd.read_sql(text(query), conn)

    dictCategories = {}
    for i, category in enumerate(dfCategories['category'], start=1):
        dictCategories[i] = category
        print(f"{i}: {category}")

    # User selects category
    choice = input("Please enter the number of the category you want to see summarized: ")

    if choice.isdigit() and int(choice) in dictCategories:
        selected_category = dictCategories[int(choice)]

        # Pull data from DB for selected category
        query = text("SELECT * FROM sales WHERE category = :cat")
        df = pd.read_sql(query, conn, params={"cat": selected_category})

        total_sales = df["total_price"].sum()
        average_sales = df["total_price"].mean()
        total_units = df["quantity_sold"].sum()

        print(f"\n📊 Summary for {selected_category}:")
        print(f"Total Sales: ${total_sales:.2f}")
        print(f"Average Sale Amount: ${average_sales:.2f}")
        print(f"Total Units Sold: {total_units}")

        # Create product-level bar chart
        dfProductSales = df.groupby("product")["total_price"].sum()
        dfProductSales.plot(kind='bar')
        plt.title(f"Total Sales in {selected_category}")
        plt.xlabel("Product")
        plt.ylabel("Total Sales ($)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    else:
        print("⚠️ Invalid category selection.")

else:
    print("👋 Exiting the program.")
