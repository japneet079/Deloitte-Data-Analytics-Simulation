import pandas as pd
import openpyxl

# 1. Load the Excel file provided by Deloitte
# Make sure this filename matches the one you downloaded!
input_file = 'Task 5 Equality Table.xlsx'
df = pd.read_excel(input_file)

# 2. Define the classification logic requested by the client
def classify_equality(score):
    abs_score = abs(score) # This handles both positive and negative gaps
    
    if abs_score <= 10:
        return "Fair"
    elif abs_score <= 20:
        return "Unfair"
    else:
        return "Highly Discriminative"

# 3. Create the new "Equality Class" column
# This runs our function on every row automatically
df['Equality Class'] = df['Equality Score'].apply(classify_equality)

# 4. Save the results into a NEW Excel file for submission
output_file = 'Deloitte_Equality_Final_Submission.xlsx'
df.to_excel(output_file, index=False)

print(f"--- Task 2 Complete ---")
print(f"New file created: {output_file}")
print("\nPreview of the classification:")
print(df[['Equality Score', 'Equality Class']].head(10))