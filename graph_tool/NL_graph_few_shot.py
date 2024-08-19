import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Function to read and process the CSV file
def read_csv_data(file_path):
    data = pd.read_csv(file_path)
    # Convert the 'Shot_number' column to numeric, setting non-numeric values to NaN
    data['Shot_number'] = pd.to_numeric(data['Shot_number'].str.extract('(\d+)', expand=False), errors='coerce')
    # Drop rows with NaN values in 'Shot_number' or 'Average'
    data = data.dropna(subset=['Shot_number', 'Average'])
    shot_number = np.array(data["Shot_number"], dtype=float)
    average = np.array(data["Average"], dtype=float)
    return shot_number, average

# File paths for the two CSV files
file_path_1 = "Few_shot_output/Pretrain_M8x7B_Model_FEN_Results.csv"
file_path_2 = "Few_shot_output/Pretrain_M8x7B_Model_NL_Results.csv"



# Reading the data from the CSV files
shot_number_1, average_1 = read_csv_data(file_path_1)
shot_number_2, average_2 = read_csv_data(file_path_2)

# Performing non-linear regression (quadratic, degree 2)
coefficients_1 = np.polyfit(shot_number_1, average_1, 2)
coefficients_2 = np.polyfit(shot_number_2, average_2, 2)

non_linear_regression_1 = np.poly1d(coefficients_1)
non_linear_regression_2 = np.poly1d(coefficients_2)

regression_curve_1 = non_linear_regression_1(shot_number_1)
regression_curve_2 = non_linear_regression_2(shot_number_2)

# Plotting the data
fig, ax = plt.subplots(figsize=(10, 6))

# Plotting the first CSV data and regression curve
ax.scatter(shot_number_1, average_1, color='blue', label='Data points (FEN)')
ax.plot(shot_number_1, regression_curve_1, color='red', label='Accuracy (FEN)')

# Plotting the second CSV data and regression curve
ax.scatter(shot_number_2, average_2, color='green', label='Data points (NL)')
ax.plot(shot_number_2, regression_curve_2, color='orange', label='Accuracy (NL)')

ax.set_xlabel('Shot Number')
ax.set_ylabel('Average')
ax.legend()

plt.show()
