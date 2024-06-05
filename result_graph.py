import pandas as pd
import matplotlib.pyplot as plt

# Organizing the data
data_16bit = {
    "Model": ["4k FEN model", "4k FEN model", "5k FEN model", "10k FEN model", "10k FEN model", "11k FEN model"],
    "Num_of_train_data": [4000, 4000, 5000, 10000, 10000, 11000],
    "Test_case": [800, 1000, 1000, 1999, 1000, 1000],
    "Accuracy_average": [12.3, 11.3, 23.4, 31.2, 30.4, 38.97]
}

data_4bit = {
    "Model": ["4k FEN model", "7k FEN model", "10k FEN model", "11k FEN model", "20k FEN model", "22k FEN model", "23k FEN model","24k FEN model", "25k FEN model", "30k FEN model"],
    "Num_of_train_data": [4000, 7000, 10000, 11000, 20000,22000, 23000, 24000, 25000, 30000],
    "Test_case": [1000, 1000, 1000, 1000, 1000,1000,1000,1000,1000,1000],
    "Accuracy_average": [12.4, 30.65, 39.27, 50.67, 61.28, 64.20, 64.47, 68.78, 67.64, 66.12],
    # "Median": [0, 0.55, 38.46, 100],
    # "Invalid_move": [847, 496, 409, 300],
    # "Invalid_move_percentage": [84.7, 49.6, 40.9, 29.8],
    # "Wrong_format": [0, 0, 0, 2]
}

data_nl_4bit = {
    "Model": [ "500 model", "1k model", "4k model", "7k model", "10k model", "11k model", "13k model", "15k model", "17k model", "18k model", "20k model"],
    "Num_of_train_data": [500,1000,4000, 7000, 10000,11000,13000,15000, 17000, 18000, 20000],
    "Test_case": [1000, 1000, 1000, 1000, 1000,1000, 1000, 1000,1000,1000, 1000],
    "Accuracy_average": [52.67, 54.71, 63.49, 70.35, 73.63,73.10,73.97,77.43, 76.98, 75.07, 77.96],
    # "Median": [0, 0.55, 38.46, 100],
    # "Invalid_move": [847, 496, 409, 300],
    # "Invalid_move_percentage": [84.7, 49.6, 40.9, 29.8],
    # "Wrong_format": [0, 0, 0, 2]
}


def training_Data_vs_Accuracy_Average_graph():
    df = pd.DataFrame(data_nl_4bit)

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

def non_nl_vs_nl_model_graph():
    # Creating DataFrames for both datasets
    df_4bit = pd.DataFrame(data_4bit)
    df_nl_4bit = pd.DataFrame(data_nl_4bit)

    # Filtering data to include only rows with Test_case == 1000
    filtered_df_4bit = df_4bit[df_4bit["Test_case"] == 1000]
    filtered_df_nl_4bit = df_nl_4bit[df_nl_4bit["Test_case"] == 1000]

    # Plotting Num_of_train_data vs Accuracy_average for both datasets
    plt.figure(figsize=(10, 6))
    plt.plot(filtered_df_4bit["Num_of_train_data"], filtered_df_4bit["Accuracy_average"], marker='o', linestyle='-', color='b', label='fen_4bit model')
    plt.plot(filtered_df_nl_4bit["Num_of_train_data"], filtered_df_nl_4bit["Accuracy_average"], marker='o', linestyle='-', color='r', label='nl_4bit model')
    
    plt.title('Number of Training Data vs Accuracy Average')
    plt.xlabel('Number of Training Data')
    plt.ylabel('Accuracy Average (%)')
    plt.grid(True)
    plt.legend()

    # Show the plot
    plt.show()

#non_nl_vs_nl_model_graph()