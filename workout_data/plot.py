import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Connect to SQLite database
conn = sqlite3.connect("workouts.db")

# Query top 10 exercises by max weight
query = """
SELECT 
    exercise_title, 
    MAX(weight_lbs) AS max_weight, 
    MAX(reps) AS max_reps
FROM workouts
WHERE weight_lbs IS NOT NULL AND reps IS NOT NULL
GROUP BY exercise_title
ORDER BY max_weight DESC
LIMIT 10;
"""
df = pd.read_sql(query, conn)
conn.close()

# Sort values for better visualization
df = df.sort_values(by="max_weight", ascending=True)  # Sort for horizontal bars

# Plot max weight (Horizontal Bar Chart with Smaller Font)
plt.figure(figsize=(10, 6))
sns.barplot(y=df["exercise_title"], x=df["max_weight"])

# Adjust font size for labels
plt.xlabel("Max Weight (lbs)", fontsize=12)
plt.ylabel("Exercise", fontsize=12)
plt.title("Top 10 Exercises by Max Weight", fontsize=14)

# Reduce Y-axis label font size
plt.yticks(fontsize=6)  # Adjust this value if needed

plt.show()