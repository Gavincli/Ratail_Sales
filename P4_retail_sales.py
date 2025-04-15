category_df = df.query("category == @category")

iTotalSales = category_df["total_price"].sum()
iAverageSales = category_df["total_price"].mean()
iUnitsSold = category_df["quantity_sold"].sum()

print(f"Total sales for {category}: {iTotalSales}")
print(f"Average sale amount for {category}: {iAverageSales}")
print(f"Total units sold for {category}: {iUnitsSold}")