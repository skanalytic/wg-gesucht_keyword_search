import pandas as pd

df = pd.read_json('result.json')

print(df[['avalible_from','avalible_to','online_since']])
