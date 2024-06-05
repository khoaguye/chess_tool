import matplotlib.pyplot as plt
import numpy as np

# Data definition
data_4bit = {
    "Model": ["4k FEN model", "7k FEN model", "10k FEN model", "11k FEN model", "20k FEN model", "22k FEN model", "23k FEN model","24k FEN model", "25k FEN model", "30k FEN model"],
    "Num_of_train_data": [4000, 7000, 10000, 11000, 20000, 22000, 23000, 24000, 25000, 30000],
    "Test_case": [1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000],
    "Accuracy_average": [12.4, 30.65, 39.27, 50.67, 61.28, 64.20, 64.47, 68.78, 67.64, 66.12],
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

num_of_train_data = np.array(data_nl_4bit["Num_of_train_data"])
accuracy_average = np.array(data_nl_4bit["Accuracy_average"])

# Performing non-linear regression (quadratic, degree 2)
# np.polyfit fits a polynomial of degree 2 to the data and returns the coefficients
coefficients = np.polyfit(num_of_train_data, accuracy_average, 2)

# Creating a polynomial object from the coefficients
# np.poly1d creates a polynomial function which can be used to evaluate the polynomial
non_linear_regression = np.poly1d(coefficients)

# Using the polynomial object to calculate the y-values (predicted accuracy) for the regression curve
regression_curve = non_linear_regression(num_of_train_data)


plt.figure(figsize=(10, 6))  
plt.scatter(num_of_train_data, accuracy_average, color='blue', label='Data points')  # Plot data points
plt.plot(num_of_train_data, regression_curve, color='red', label='Non-linear regression curve')  # Plot the regression curve

plt.title('Non-linear Regression of Training Data vs. Accuracy')  
plt.xlabel('Number of Training Data')  
plt.ylabel('Accuracy Average') 
plt.legend()  

plt.show()
