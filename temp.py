import pandas as pd
from os import remove, rename

df = pd.read_csv("meta/matches")
bonus = 0
size = df.shape[0]
for i in range(3192, 3303):
    rename(f"games/{i}", f"games/{i - 110}")