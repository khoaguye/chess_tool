import matplotlib.pyplot as plt
import numpy as np

data_fen_4bit = {
    "Model": ["Base model" "4k Fen model", "7k Fen model", "10k Fen model", "11k Fen model", "17k Fen model", "18k Fen model", "20k Fen model", "22k Fen model", "23k Fen model", "24k Fen model", "25k Fen model", "27k Fen model", "30k Fen model"],
    "Num_of_train_data": [ 0, 4000, 7000, 10000, 11000, 17000, 18000, 20000, 22000, 23000, 24000, 25000, 27000, 30000],
    "Test_case": [1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000],
    "Accuracy_average": [7.84, 12.4, 30.65, 39.27, 50.67, 61.55, 61.69, 61.28, 64.20, 64.47, 68.78, 67.6, 71.12, 66.12],
    "Invalid_move": [724, 847, 626, 496, 409, 292, 264, 300, 258, 241, 209, 226, 190, 237],
}
# Data definition
data_nl_4bit = {
    "Model": ["Base model" "500 nl model", "1k nl model", "5k", "7k", "10k", "11k", "13k", "15k", "17k", "18k", "20k"],
    "Num_of_train_data": [0, 500, 1000, 5000, 7000, 10000, 11000, 13000, 15000, 17000, 18000, 20000],
    "Test_case": [1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000],
    "Accuracy_average": [ 11.08, 52.67, 54.71, 63.49, 70.35, 73.63, 73.10, 73.97, 77.43, 76.98, 75.07, 77.96],
    "Accuracy_median": [ 0, 62.63, 71.61, 89.66, 97.17, 97.17, 97.56, 97.94, 98.91, 98.61, 97.6, 98.58],
    "Invalid_move": [ 761, 373, 348, 262, 206, 161, 165, 160, 128, 131, 147, 115],
    "Wrong_format": [ 106, 0, 5, 9, 2, 4, 5, 4, 3, 1, 2, 4]
}

data_fen_lm3_4bit = {
    "Model": ["Base model", "4k FEN model", "7k FEN model", "10k FEN model", "11k FEN model","15k FEN model","18k FEN model","20k FEN model","23k FEN model","25k FEN model"],
    "Num_of_train_data": [0,4000, 7000, 10000, 11000, 15000, 18000,20000,23000,25000],
    "Test_case": [1000, 1000, 1000, 1000, 1000, 1000,1000,1000,1000,1000],
    "Accuracy_average": [5.67,42.75,49.56,62.85,58.55,65.89,69.23,70.29,70.50,71.30],
    "Median": [0, 18.03,54.78,88.07,80.42,92.69,95.88,96.61,96.78,96.66,96.78],
    "Invalid_move": [901, 493,409,276,310,235,206,203,202,186],
    "Wrong_format": [28, 3,5,3,3,3,1,2,2,3]
}

data_nl_lm3_4bit = {
    "Model": ["Base model", "500 nl model", "1000 nl model", "2000 nl model",  "4k nl model","7k nl model", "10k nl model", "13k nl model", "15k nl model","18k nl model","20k nl model"],
    "Num_of_train_data": [0, 500, 1000, 2000,  4000, 7000, 10000, 13000, 15000, 18000,20000],
    "Test_case": [1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000,1000],
    "Accuracy_average": [12.57, 58.39, 62.82, 67.35, 73.22, 78.04, 80.21, 79.63, 80.17, 80.33, 80.32 ],
    "Median": [0, 78.66, 90,38, 94.08, 98.41, 99.25, 99.21, 99.07, 99.1, 99.12, 99.12 ],
    "Invalid_move": [476, 308,278,232, 168,121,107,114,97,92,92 ],
    "Wrong_format": [463,2,2,4, 4,7,3,4,3,6,6]
}

#ADD DATA POINT FOR INVALID MOVE 

num_of_train_data = np.array(data_nl_4bit["Num_of_train_data"])
accuracy_average = np.array(data_nl_4bit["Accuracy_average"])
invalid_move = np.array(data_nl_4bit["Invalid_move"])

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
ax1.plot(num_of_train_data, regression_curve_accuracy, color='red', label='Accuracy')
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
color = 'tab:green'
ax2.set_ylabel('Invalid Move', color=color)
ax2.scatter(num_of_train_data, invalid_move, color=color, label='Data points (Invalid Move)')
ax2.plot(num_of_train_data, regression_curve_invalid_move, color='green', label='Invalid Move')
ax2.tick_params(axis='y', labelcolor=color)



# Place legends outside of the graph
handles1, labels1 = ax1.get_legend_handles_labels()
handles2, labels2 = ax2.get_legend_handles_labels()

#fig.legend(handles1 + handles2, labels1 + labels2, loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=2)
fig.legend(handles1 + handles2, labels1 + labels2, loc='lower center', ncol=2)
plt.subplots_adjust(bottom=0.25)
plt.show()