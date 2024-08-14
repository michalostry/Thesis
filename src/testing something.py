import numpy as np

# Given parameters
median = 39.685
mean = 46.013

# Calculate mu and sigma
mu = np.log(median)
print('mu',mu)
sigma_squared = 2 * (np.log(mean) - mu)
print('sigma_squared',sigma_squared)
sigma = np.sqrt(sigma_squared)
print("sigma",sigma)

# Generate lognormally distributed income data
num_students = 1000  # Example: number of students
incomes = np.random.lognormal(mu, sigma, num_students)

# Print out mu, sigma, and some generated income samples
print(f"Calculated mu: {mu}")
print(f"Calculated sigma: {sigma}")
print(f"Sample incomes: {incomes[:10]}")  # Display first 10 generated incomes
