print_info = 0 #1 - yes, 0 - no
print_visualizations = 0
set_seed = 0 #1 - yes, 0 - no

import numpy as np
from scipy.stats import rankdata
from scipy.spatial.distance import pdist, squareform
from scipy.linalg import cholesky
import matplotlib.pyplot as plt

# Define the Student class to store attributes and preferences of each student
class Student:
    def __init__(self, id, location, income, achievement):
        self.id = id
        self.location = location
        self.income = income
        self.achievement = achievement
        self.preferences = []
        self.matched_school = None

    def __repr__(self):
        return f"Student({self.id}, Loc: {self.location}, Inc: {self.income}, Ach: {self.achievement})"


# Define the School class to store attributes and preferences of each school
class School:
    def __init__(self, id, location, quality):
        self.id = id
        self.location = location
        self.quality = quality
        self.capacity = 0
        self.preferences = []

    def __repr__(self):
        return f"School({self.id}, Loc: {self.location}, Qual: {self.quality})"


# #Function to generate spatially correlated data
# def generate_spatially_correlated_data(locations, mean, std, correlation_length):
#     if print_info == 1: print("spatially_correlated_data")
#     # Calculate pairwise distances between locations
#     distances = squareform(pdist(locations))
#
#     # Generate a spatially correlated covariance matrix
#     covariance_matrix = np.exp(-distances / correlation_length)
#
#     if print_info == 1: print("covariance matrix")
#
#     # Generate correlated random variables
#     correlated_data = np.random.multivariate_normal(mean * np.ones(len(locations)),
#                                                     std ** 2 * covariance_matrix)
#
#     if print_info == 1: print("correlated_data")
#     return correlated_data

# disable spatially correlated data for now
# def generate_spatially_correlated_data(locations, mean, std, correlation_length, epsilon=1e-6):
#     if print_info == 1:print("Step 1: Calculating pairwise distances...")
#     # Calculate pairwise distances between locations
#     distances = squareform(pdist(locations))
#
#     if print_info == 1:print("Step 2: Generating covariance matrix...")
#     # Generate a spatially correlated covariance matrix
#     covariance_matrix = np.exp(-distances / correlation_length)
#
#     # Add a small value to the diagonal to ensure positive definiteness
#     covariance_matrix += np.eye(covariance_matrix.shape[0]) * epsilon
#
#     if print_info == 1:print("Step 3: Performing Cholesky decomposition...")
#     # Use Cholesky decomposition instead of SVD
#     L = cholesky(covariance_matrix, lower=True)
#
#     if print_info == 1:print("Step 4: Generating independent normal variables...")
#     # Generate independent standard normal variables
#     independent_normals = np.random.normal(size=len(locations))
#
#     if print_info == 1:print("Step 5: Applying Cholesky factor to generate correlated data...")
#     # Apply Cholesky factor to get correlated data
#     correlated_data = mean + std * np.dot(L, independent_normals)
#
#     if print_info == 1:print("Step 6: Correlated data generation complete.")
#     return correlated_data


# Function to generate synthetic data for a given number of students and schools
def generate_synthetic_data(num_students, num_schools, grid_size, school_capacity_min, school_capacity_max, correlation_length=1000):
    if print_info == 1: print("generate_synthetic_data")
    if set_seed == 1: np.random.seed(46)  # Set a random seed for reproducibility

    # Given wage characteristics for log normal distribution
    median = 39.685
    mean = 46.013

    # Calculate mu and sigma
    mu = np.log(median)
    sigma = np.sqrt(2 * (np.log(mean) - mu))

    #calculate st.deviation
    stdev = np.sqrt((np.exp(sigma ** 2) - 1) * np.exp(2 * mu + sigma ** 2))

    # Generate lognormally distributed income data
    # and divide by max number to normalize 0-1
    incomes = (np.clip(np.random.lognormal(mu, sigma, num_students),0,mean+3*stdev))/(mean+3*stdev)

    # Generate random locations for students
    locations = np.random.randint(0, grid_size, (num_students, 2))

    # Generate achievements correlated with income
    achievement_mean = 50
    achievement_std = 20
    correlation = 0.39  # Correlation between income and achievement
    raw_achievements = np.random.normal(achievement_mean + correlation * (incomes - np.mean(incomes)),
                                        achievement_std * (1 - correlation ** 2) ** 0.5)

    # Convert achievements to percentiles
    percentiles = rankdata(raw_achievements, method='average') / len(raw_achievements) * 100

    # Create Student objects
    student_data = []
    for i in range(num_students):
        student_data.append(Student(i, locations[i], incomes[i], percentiles[i]))

    # Generate school data
    school_data = []
    school_qualities = []  # To store qualities for visualization
    for j in range(num_schools):
        location = np.random.randint(0, grid_size, 2)
        quality = np.random.normal(50, 20)
        quality = np.clip(quality, 0, 100)  # Clip quality to the range [0, 100]
        school_qualities.append(quality)
        school = School(j, location, quality)
        school.capacity = np.random.randint(school_capacity_min, school_capacity_max + 1)
        school_data.append(school)

    if print_visualizations == 1:
        # Visualize the distribution of school qualities
        plt.hist(school_qualities, bins=20, color='blue', edgecolor='black')
        plt.title('Distribution of School Quality')
        plt.xlabel('School Quality')
        plt.ylabel('Number of Schools')
        plt.show()

        # Visualize the initial locations of students with color-coding by income levels
        plt.figure(figsize=(10, 10))

        # Define income brackets and corresponding colors
        income_brackets = [0, 33, 66, 100, 1000]
        colors = ['blue', 'green', 'orange', 'red']

        # Plot each income bracket
        for i in range(4):
            lower_bound = income_brackets[i]
            upper_bound = income_brackets[i + 1]
            income_group = [student for student in student_data if lower_bound <= student.income < upper_bound]
            plt.scatter([student.location[0] for student in income_group],
                        [student.location[1] for student in income_group],
                        c=colors[i], label=f'Income {lower_bound}-{upper_bound}', alpha=0.5)

        plt.xlim(0, grid_size)
        plt.ylim(0, grid_size)
        plt.title("Initial Student Locations by Income Level")
        plt.legend()
        plt.show()

        # Visualize the distribution of incomes
        plt.figure(figsize=(10, 6))
        plt.hist(incomes, bins=100, color='purple', edgecolor='black')
        plt.title('Distribution of Student Incomes')
        plt.xlabel('Income')
        plt.ylabel('Number of Students')
        plt.show()


    return student_data, school_data


def get_min_max_values(students, schools):
    if print_info == 1:
        print("get_min_max")

    # Extract locations into NumPy arrays
    student_locations = np.array([student.location for student in students])
    school_locations = np.array([school.location for school in schools])

    # Calculate the distances between each student and each school
    distances = np.linalg.norm(
        student_locations[:, np.newaxis, :] - school_locations[np.newaxis, :, :],
        axis=2
    )

    # Get min and max distances
    min_distance = np.min(distances)
    max_distance = np.max(distances)

    # Get min and max incomes
    incomes = np.array([student.income for student in students])
    min_income = np.min(incomes)
    max_income = np.max(incomes)

    return {
        'distance': (min_distance, max_distance),
        'income': (min_income, max_income)
    }


