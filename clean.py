import pandas as pd

# Load your JSON data into a pandas DataFrame (replace <your_json_file_path> with your actual file path)
df = pd.read_json('/Users/maddhavsuneja28/Downloads/SuperBowl2025/superbowl_comments.json')

# Check for duplicate timestamps and remove them
df_cleaned = df.drop_duplicates(subset=['timestamp'], keep='first')

# Save the cleaned DataFrame back to a new JSON file
df_cleaned.to_json('superbowl_comments.json', orient='records', lines=True)

print("Cleaned data has been saved to 'cleaned_data.json'")