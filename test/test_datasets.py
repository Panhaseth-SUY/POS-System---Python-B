
import pandas as pd

dataset = "/Users/home/Desktop/pos_system/assets/datasets/categories_dataset.csv"

# read categories.csv
df = pd.read_csv(dataset)

# # loop over categories
for index, row in df.iterrows():
    print(f"Category ID: {row['id']}, Category Name: {row['name']}, Description: {row['description']}")

# # loop over categories
# for index, row in df.iterrows():
#     print(f"Category ID: {row['id']}, Category Name: {row['name']}, Description: {row['description']}")
