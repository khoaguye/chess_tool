import pandas as pd
import matplotlib.pyplot as plt

# Organizing the data
data_16bit = {
    "Model": ["4k FEN model", "4k FEN model", "5k FEN model", "10k FEN model", "10k FEN model", "11k FEN model"],
    "Num_of_train_data": [4000, 4000, 5000, 10000, 10000, 11000],
    "Test_case": [800, 1000, 1000, 1999, 1000, 1000],
    "Accuracy_average": [12.2, 11.3, 23.4, 31.2, 30.4, 38.97]
}

data_4bit = {
    "Model": ["4k FEN model", "10k FEN model", "11k FEN model", "20k FEN model"],
    "Num_of_train_data": [4000, 10000, 11000, 20000],
    "Test_case": [1000, 1000, 1000, 1000],
    "Accuracy_average": [11.28, 39.27, 47.43, 82.39],
    "Median": [0, 0.55, 38.46, 100],
    "Invalid_move": [847, 496, 409, 298],
    "Invalid_move_percentage": [84.7, 49.6, 40.9, 29.8],
    "Wrong_format": [0, 0, 0, 2]
}


def training_Data_vs_Accuracy_Average_graph():
    df = pd.DataFrame(data_4bit)

    # Filtering data to include only rows with Test_case == 1000
    filtered_df = df[df["Test_case"] == 1000]

    # Plotting Num_of_train_data vs Accuracy_average for 1000 Test_case
    plt.figure(figsize=(10, 6))
    plt.plot(filtered_df["Num_of_train_data"], filtered_df["Accuracy_average"], marker='o', linestyle='-', color='b')
    plt.title('Number of Training Data vs Accuracy Average for 4bit model')
    plt.xlabel('Number of Training Data')
    plt.ylabel('Accuracy Average (%)')
    plt.grid(True)

    # Show the plot
    plt.show()

training_Data_vs_Accuracy_Average_graph()