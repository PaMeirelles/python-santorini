import pandas as pd
from board import fix_hash, unhash_position

df = pd.read_csv("meta/matches")
df["starting_pos"] = df["starting_pos"].apply(fix_hash)
df.to_csv("meta/matches")