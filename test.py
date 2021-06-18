import pandas as pd

data = {
  "calories": [420, 380, 390],
  "duration": [50, 40, 45]
}

#load data into a DataFrame object:
df = pd.DataFrame(data)

count = 0
for list in df["calories"]:
    print(list)
    if list == 380:
        print(df.loc[count]["calories"])
    count += 1
