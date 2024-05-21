import pandas as pd
import matplotlib.pyplot as plt

# Organizing the data
data = {
    "Model": ["4k FEN model", "4k FEN model", "5k FEN model", "10k FEN model", "10k FEN model", "11k FEN model"],
    "Num_of_train_data": [4000, 4000, 5000, 10000, 10000, 11000],
    "Test_case": [800, 1000, 1000, 1999, 1000, 1000],
    "Accuracy_average": [12.2, 11.3, 23.4, 31.2, 30.4, 38.97]
}

df = pd.DataFrame(data)

# Filtering data to include only rows with Test_case == 1000
filtered_df = df[df["Test_case"] == 1000]

# Plotting Num_of_train_data vs Accuracy_average for 1000 Test_case
plt.figure(figsize=(10, 6))
plt.plot(filtered_df["Num_of_train_data"], filtered_df["Accuracy_average"], marker='o', linestyle='-', color='b')
plt.title('Number of Training Data vs Accuracy Average (1000 Test Cases)')
plt.xlabel('Number of Training Data')
plt.ylabel('Accuracy Average (%)')
plt.grid(True)

# Show the plot
plt.show()
