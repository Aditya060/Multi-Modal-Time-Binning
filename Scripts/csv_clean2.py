# import pandas as pd

# # Read the CSV file into a DataFrame
# df = pd.read_csv('modified_iphone_reviews.csv')  # Replace 'your_file.csv' with your CSV file's name

# # Convert the date column to Pandas datetime format
# df['Date'] = pd.to_datetime(df['Reviews'], format='%b,%Y')  # Replace 'Date' with your actual date column name

# # Sort the DataFrame by the date column
# df = df.sort_values(by='Date')

# # Reset the index
# df.reset_index(drop=True, inplace=True)

# # Save the sorted DataFrame back to a CSV file
# df.to_csv('sorted_file.csv', index=False)  # Replace 'sorted_file.csv' with your desired output filename
import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv('modified_iphone_reviews.csv')  # Replace 'your_file.csv' with your CSV file's name

# Define a function to convert "X months ago" to a valid date
month_mapping = {
    1: 'Aug',
    2: 'Jul',
    3: 'Jun',
    4: 'May',
    5: 'Apr',
    6: 'Mar',
    7: 'Feb',
    8: 'Jan',
    9: 'Dec',
    10: 'Nov',
    11: 'Oct',
    12: 'Sep'
}
# Mapping to register the date entries that follow the format x months ago

def convert_months_ago(months_ago):
    # Split the input into month and year
    parts = months_ago.split(' ')
    month = month_mapping.get(int(parts[0].strip()))
    # print(month)
    year = 2023
    if(int(parts[0].strip())>8):
        year = 2022

    # year = 2023
    
    # Convert to a valid date format (the 1st day of the month)
    date = pd.to_datetime(f'01-{month}-{year}', format='%d-%b-%Y')
    return date.strftime('%b, %Y')

# Process the "X months ago" entries and convert them to valid dates
df['Processed_Date'] = df['Reviews'].apply(lambda x: convert_months_ago(x) if 'ago' in x else x)

# Convert the combined date column to Pandas datetime format
df['Processed_Date'] = pd.to_datetime(df['Processed_Date'], format='%b, %Y')

# Sort the DataFrame by the date column
df = df.sort_values(by='Processed_Date')

# Reset the index
df.reset_index(drop=True, inplace=True)

#Re group the dataframe to index, date, 5,4,3,2,1 (counts of individual ratings for each month)
 df['Processed_Date'] = pd.to_datetime(df['Processed_Date'])
 df['Month'] = df['Processed_Date'].dt.to_period('M')
 result = df.groupby(['Month', 'Index']).size().unstack(fill_value=0).reset_index()
 #print(result)


# Save the sorted DataFrame back to a CSV file
df.to_csv('sorted_file.csv', index=False)  # Replace 'sorted_file.csv' with your desired output filename
