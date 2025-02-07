import pandas as pd
import cbsodata

# tables = cbsodata.get_table_list()
# for table in tables:
#     if "home" in table["Title"]:
#         print(f"{table['Identifier']}: {table['Title']}")

data = cbsodata.get_data("85773ENG")

df = pd.DataFrame(data)

print(df.shape)
print(df.describe())
print(df.head())
print(df.tail())
print(df.iloc[0])
