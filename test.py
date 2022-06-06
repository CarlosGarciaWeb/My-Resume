import pandas as pd
import numpy

dataframe1 = pd.read_excel("professional experiences.xlsx", sheet_name="Sheet2")

print(len(dataframe1))

for n in range(4):
    print( dataframe1.img[n], dataframe1.cert[n])