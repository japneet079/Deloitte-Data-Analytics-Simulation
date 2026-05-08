import pandas as pd
import json

# 1. Load the data with explicit UTF-8 encoding to fix the UnicodeDecodeError
with open('daikibo-telemetry-data.json', 'r', encoding='utf-8') as f:
    raw_data = json.load(f)

# 2. Flatten the nested JSON (this turns 'data': {'status': 'healthy'} into 'data.status')
df = pd.json_normalize(raw_data)

# 3. Create the Downtime column using the correct flattened name: 'data.status'
# Note: Check if it's 'unhealthy' (lowercase) based on your printout
df['Downtime_Minutes'] = df['data.status'].apply(lambda x: 10 if str(x).lower() == 'unhealthy' else 0)

# 4. Question 1: Location with most downtime
# Based on your printout, the factory name is likely in 'location.city' or 'location.factory'
# Let's use 'location.city' first as it was visible in your output
factory_col = 'location.city' 
factory_summary = df.groupby(factory_col)['Downtime_Minutes'].sum().sort_values(ascending=False)

print("--- Total Downtime per City/Factory ---")
print(factory_summary)

# 5. Question 2: Worst machine in that specific city
top_city = factory_summary.index[0]
worst_city_data = df[df[factory_col] == top_city]

device_summary = worst_city_data.groupby('deviceType')['Downtime_Minutes'].sum().sort_values(ascending=False)
print(f"\n--- Machine Downtime in {top_city.upper()} ---")
print(device_summary)

# Optional: Quick check of the first few rows to be sure
print("\nVerified flattened columns:", df.columns.tolist()[:10])
import matplotlib.pyplot as plt
import seaborn as sns

# Set a professional style
sns.set_theme(style="whitegrid")

# 1. Create the Factory Chart
plt.figure(figsize=(10, 6))
sns.barplot(x=factory_summary.index, y=factory_summary.values, palette="viridis")

# Add labels and title
plt.title('Total Machine Downtime by Factory (May 2021)', fontsize=15)
plt.xlabel('Factory Location', fontsize=12)
plt.ylabel('Total Downtime (Minutes)', fontsize=12)

# 2. Save the file to your desktop folder
plt.savefig('deloitte_dashboard_task1.png')

# 3. Force the window to pop up
print("\nGraph saved as 'deloitte_dashboard_task1.png' in your folder.")
plt.show()