import pandas as pd
pd.set_option('display.max_columns', 500)

data = pd.read_csv("/Users/sahilnagpal/PycharmProjects/MapsPython/data/ActualData.txt", sep='\t')
lonRow = int(input("Index of Langitude Column : "))
colname = input("colname : ")

maindata = data[colname]
for row in data.itertuples():
    print(row[lonRow])
