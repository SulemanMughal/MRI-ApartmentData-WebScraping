import pandas as pd
df = pd.read_csv("apartment_links.csv")
split_values = df['id']
print(split_values.__len__())

number_of_batchese = (int(split_values.__len__()/10))
# print(number_of_batchese)
remaining_elements = split_values.__len__() - (number_of_batchese*10)
# print(remaining_elements)
# print(int(split_values.__len__()/10))

# print(df.iloc[])
# print(df.iloc[:10])

for i in range(0, split_values.__len__(), 10):
    df_1 = df.iloc[i:i+10,:]
    df_1.to_csv(f'output_batches/batch_{i}.csv', index=False)

df_1 = df.iloc[number_of_batchese*10,:]
df_1.to_csv(f'output_batches/batch_{number_of_batchese+1}.csv', index=False)