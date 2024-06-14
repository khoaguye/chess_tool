import matplotlib.pyplot as plt
import numpy as np

data_fen_4bit = {
    "Model": ["4k Fen model", "7k Fen model", "10k Fen model", "11k Fen model", "17k Fen model", "18k Fen model", "20k Fen model", "22k Fen model", "23k Fen model", "24k Fen model", "25k Fen model", "27k Fen model", "30k Fen model"],
    "Num_of_train_data": [ 4000, 7000, 10000, 11000, 17000, 18000, 20000, 22000, 23000, 24000, 25000, 27000, 30000],
    "Test_case": [ 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000],
    "Accuracy_average": [12.4, 30.65, 39.27, 50.67, 61.55, 61.69, 61.28, 64.20, 64.47, 68.78, 67.6, 71.12, 66.12],
    "Invalid_move": [847, 626, 496, 409, 292, 264, 300, 258, 241, 209, 226, 190, 237],
}
# Data definition
data_nl_4bit = {
    "Model": ["Base", "500", "1k nl model", "5k", "7k", "10k", "11k", "13k", "15k", "17k", "18k", "20k"],
    "Num_of_train_data": [0, 500, 1000, 5000, 7000, 10000, 11000, 13000, 15000, 17000, 18000, 20000],
    "Test_case": [1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000],
    "Accuracy_average": [5.2, 52.67, 54.71, 63.49, 70.35, 73.63, 73.10, 73.97, 77.43, 76.98, 75.07, 77.96],
    "Accuracy_median": [0, 62.63, 71.61, 89.66, 97.17, 97.17, 97.56, 97.94, 98.91, 98.61, 97.6, 98.58],
    "Invalid_move": [820, 373, 348, 262, 206, 161, 165, 160, 128, 131, 147, 115],
    "Wrong_format": [116, 0, 5, 9, 2, 4, 5, 4, 3, 1, 2, 4]
}

num_of_train_data = np.array(data_fen_4bit["Num_of_train_data"])
accuracy_average = np.array(data_fen_4bit["Accuracy_average"])
invalid_move = np.array(data_fen_4bit["Invalid_move"])

# Performing non-linear regression (quadratic, degree 2)
coefficients_accuracy = np.polyfit(num_of_train_data, accuracy_average, 2)
coefficients_invalid_move = np.polyfit(num_of_train_data, invalid_move, 2)

non_linear_regression_accuracy = np.poly1d(coefficients_accuracy)
non_linear_regression_invalid_move = np.poly1d(coefficients_invalid_move)

regression_curve_accuracy = non_linear_regression_accuracy(num_of_train_data)
regression_curve_invalid_move = non_linear_regression_invalid_move(num_of_train_data)

fig, ax1 = plt.subplots(figsize=(10, 6))

color = 'tab:blue'
ax1.set_xlabel('Number of Training Data')
ax1.set_ylabel('Accuracy Average', color=color)
ax1.scatter(num_of_train_data, accuracy_average, color=color, label='Data points (Accuracy)')
ax1.plot(num_of_train_data, regression_curve_accuracy, color='red', label='Non-linear regression (Accuracy)')
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
color = 'tab:green'
ax2.set_ylabel('Invalid Move', color=color)
ax2.plot(num_of_train_data, regression_curve_invalid_move, color='green', label='Non-linear regression (Invalid Move)')
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()  # otherwise the right y-label is slightly clipped
fig.suptitle('Non-linear Regression of Training Data vs. Accuracy and Invalid Moves for Natural Language Model', y=1.05)

ax1.legend(loc='upper left')
ax2.legend(loc='upper right')

plt.show()
