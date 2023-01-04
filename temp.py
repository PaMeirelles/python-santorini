import pandas as pd

df = pd.read_csv("meta/matches")
del df["Unnamed: 0.1"]
del df["Unnamed: 0"]
print(df.columns)
df.to_csv("meta/matches", index=False)