import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv('iphone_reviews.csv')
df2 = pd.read_csv('iphone_ratings.csv')

# Delete every even line (starting from the second line)
df = df.iloc[1::2]
df2 = df2[df2['Ratings'] != 4.6]  

# Reset the index to rearrange the remaining lines sequentially
df.reset_index(drop=True, inplace=True)
df2.reset_index(drop=True, inplace=True)
df = pd.concat([df,df2], axis=1)

# Save the modified DataFrame back to a CSV file
df.to_csv('modified_iphone_reviews.csv', index=False)
df2.to_csv('modified_iphone_ratings.csv', index = False)
