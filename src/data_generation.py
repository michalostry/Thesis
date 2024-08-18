print_info = 0 #1 - yes, 0 - no
print_visualizations = 0
set_seed = 1 #1 - yes, 0 - no

import numpy as np
from scipy.stats import rankdata
from scipy.stats import truncnorm
from scipy.spatial.distance import pdist, squareform
from scipy.linalg import cholesky
import matplotlib.pyplot as plt
from scipy.stats import linregress

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

    ### STEP 1 ###
    # Settings

    # Give wage characteristics for log normal distribution
    median = 39.685
    mean = 46.013

    # Achievements
    achievement_mean = 50
    achievement_std = 20
    correlation = 0.39  # Correlation between income and achievement
    # Define the lower and upper bounds of achievement
    lower_bound = 0
    upper_bound = 100

    ### STEP 2 ###
    # Generating income and achievement data

    # Calculate mu and sigma for income distribution
    mu = np.log(median)
    sigma = np.sqrt(2 * (np.log(mean) - mu))

    #calculate st.deviation
    stdev = np.sqrt((np.exp(sigma ** 2) - 1) * np.exp(2 * mu + sigma ** 2))

    # Generate log normally distributed income data
    # and divide by max number to scale 0-1
    incomes = (np.clip(np.random.lognormal(mu, sigma, num_students), 0, mean + 3*stdev))/(mean+3*stdev)
    incomes_not_scaled = np.clip(np.random.lognormal(mu, sigma, num_students), 0, mean + 3 * stdev)

    # Generate random locations for students
    locations = np.random.randint(0, grid_size, (num_students, 2))

    # Calculate the parameters for the truncated normal distribution
    a = (lower_bound - achievement_mean) / achievement_std
    b = (upper_bound - achievement_mean) / achievement_std

    # Generate the achievement normal data within boundaries
    achievements_for_old = truncnorm.rvs(a, b, loc=achievement_mean, scale=achievement_std, size=num_students)


    ### STEP 3 ###
    # Introduce correlation between income and achievement

    # Apply logarithmic transformation to income to approximate normal distribution
    log_incomes = np.log(incomes)
    log_incomes_for_old = log_incomes
    # Standardize variables for calculating correlation
    log_incomes_for_old_standardized = (log_incomes_for_old - np.mean(log_incomes_for_old)) / np.std(
        log_incomes_for_old)
    achievements_for_old_standardized = (achievements_for_old - np.mean(achievements_for_old)) / np.std(
        achievements_for_old)

    # Generate correlated achievements
    achievements_for_old_correlated = correlation * log_incomes_for_old_standardized + np.sqrt(
        1 - correlation ** 2) * achievements_for_old_standardized

    # # PLOT to check distribution of achievements
    # plt.figure(figsize=(10, 6))
    # plt.hist(achievements_for_old_correlated, bins=100, color='purple', edgecolor='black')
    # plt.title('Distribution of achievements_for_old_correlated')
    # plt.xlabel('Achievement')
    # plt.ylabel('Number of Students')
    # plt.show()

    # Scale achievements back to original scale
    achievements_for_old_correlated = achievements_for_old_correlated * achievement_std + achievement_mean

    # #PLOT to check distribution of achievements
    # plt.figure(figsize=(10, 6))
    # plt.hist(achievements_for_old_correlated, bins=100, color='purple', edgecolor='black')
    # plt.title('Distribution of achievements_for_old_correlated')
    # plt.xlabel('Achievement')
    # plt.ylabel('Number of Students')
    # plt.show()

    # Convert achievements to percentiles
    percentiles_for_old = rankdata(achievements_for_old_correlated, method='average') / len(achievements_for_old_correlated) * 100

    # # PLOT to check distribution of achievements
    # plt.figure(figsize=(10, 6))
    # plt.hist(percentiles_for_old, bins=100, color='purple', edgecolor='black')
    # plt.title('Distribution of percentiles_for_old')
    # plt.xlabel('Achievement')
    # plt.ylabel('Number of Students')
    # plt.show()

    #### NOT USED APPROACH ###
    # # Apply linear regression to create a relationship between log_income and achievement
    # raw_achievements = achievement_mean + (achievement_std / np.std(log_incomes)) * (
    #             log_incomes - np.mean(log_incomes)) * correlation
    # raw_achievements += np.random.normal(0, achievement_std * np.sqrt(1 - correlation ** 2), num_students)
    # raw_achievements = np.clip(raw_achievements, 0, 100)
    # percentiles = rankdata(raw_achievements, method='average') / len(raw_achievements) * 100


    ### STEP 4 ###
    # Save the data

    # Create Student objects
    student_data = []
    for i in range(num_students):
        student_data.append(Student(i, locations[i], incomes[i], percentiles_for_old[i]))

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

        # # Visualize the initial locations of students with color-coding by income levels
        # plt.figure(figsize=(10, 10))
        #
        # # Define income brackets and corresponding colors
        # income_brackets = [0, 33, 66, 100, 1000]
        # colors = ['blue', 'green', 'orange', 'red']
        #
        # # Plot each income bracket
        # for i in range(4):
        #     lower_bound = income_brackets[i]
        #     upper_bound = income_brackets[i + 1]
        #     income_group = [student for student in student_data if lower_bound <= student.income < upper_bound]
        #     plt.scatter([student.location[0] for student in income_group],
        #                 [student.location[1] for student in income_group],
        #                 c=colors[i], label=f'Income {lower_bound}-{upper_bound}', alpha=0.5)
        #
        # plt.xlim(0, grid_size)
        # plt.ylim(0, grid_size)
        # plt.title("Initial Student Locations by Income Level")
        # plt.legend()
        # plt.show()

        # # Visualize the distribution of incomes
        # plt.figure(figsize=(10, 6))
        # plt.hist(incomes, bins=100, color='purple', edgecolor='black')
        # plt.title('Distribution of Student Incomes')
        # plt.xlabel('Income')
        # plt.ylabel('Number of Students')
        # plt.show()
        #
        # # Visualize the distribution of incomes not scaled
        # plt.figure(figsize=(10, 6))
        # plt.hist(incomes_not_scaled, bins=100, color='purple', edgecolor='black')
        # plt.title('Distribution of Student Incomes')
        # plt.xlabel('incomes_not_scaled')
        # plt.ylabel('Number of Students')
        # plt.show()
        #
        # # Visualize the distribution of achievement
        # plt.figure(figsize=(10, 6))
        # plt.hist(percentiles_for_old, bins=100, color='purple', edgecolor='black')
        # plt.title('Distribution of Student AChievement percentiles')
        # plt.xlabel('Achievement percentile')
        # plt.ylabel('Number of Students')
        # plt.show()
        #
        # # Visualize the distribution of achievement
        # plt.figure(figsize=(10, 6))
        # plt.hist(achievements_for_old_correlated, bins=100, color='purple', edgecolor='black')
        # plt.title('Distribution of Student AChievement')
        # plt.xlabel('Achievement')
        # plt.ylabel('Number of Students')
        # plt.show()

        # Calculate correlation coefficient
        correlation_coefficient_percentile_1 = np.corrcoef(incomes_not_scaled, percentiles_for_old)[0, 1]
        print(f"Correlation Coefficient between incomes_not_scaled and percentiles_for_old: {correlation_coefficient_percentile_1:.2f}")

        correlation_coefficient_percentile_2 = np.corrcoef(incomes, percentiles_for_old)[0, 1]
        print(f"Correlation Coefficient between incomes and percentiles_for_old: {correlation_coefficient_percentile_2:.2f}")

        correlation_coefficient_achievement1 = np.corrcoef(incomes_not_scaled, achievements_for_old_correlated)[0, 1]
        print(f"Correlation Coefficient between incomes_not_scaled and achievements_for_old_correlated: {correlation_coefficient_achievement1:.2f}")

        correlation_coefficient_achievement2 = np.corrcoef(incomes, achievements_for_old_correlated)[0, 1]
        print(f"Correlation Coefficient between incomes and achievements_for_old_correlated: {correlation_coefficient_achievement2:.2f}")

        # Create a figure and axis objects
        fig, axs = plt.subplots(2, 2, figsize=(14, 12))

        # Plot 1: incomes_not_scaled vs percentiles_for_old
        axs[0, 0].scatter(incomes_not_scaled, percentiles_for_old, alpha=0.5)
        slope, intercept, _, _, _ = linregress(incomes_not_scaled, percentiles_for_old)
        axs[0, 0].plot(incomes_not_scaled, slope * incomes_not_scaled + intercept, color='red', linewidth=2)
        axs[0, 0].set_title('Relationship of income with achievement percentile')
        axs[0, 0].set_xlabel('Income (thousands CZK)')
        axs[0, 0].set_ylabel('Achievement percentiles')
        axs[0, 0].grid(True)

        # Plot 2: incomes vs percentiles_for_old
        axs[0, 1].scatter(incomes, percentiles_for_old, alpha=0.5)
        slope, intercept, _, _, _ = linregress(incomes, percentiles_for_old)
        axs[0, 1].plot(incomes, slope * incomes + intercept, color='red', linewidth=2)
        axs[0, 1].set_title('incomes vs percentiles_for_old')
        axs[0, 1].set_xlabel('incomes')
        axs[0, 1].set_ylabel('percentiles_for_old')
        axs[0, 1].grid(True)

        # Plot 3: incomes_not_scaled vs achievements_for_old_correlated
        axs[1, 0].scatter(incomes_not_scaled, achievements_for_old_correlated, alpha=0.5)
        slope, intercept, _, _, _ = linregress(incomes_not_scaled, achievements_for_old_correlated)
        axs[1, 0].plot(incomes_not_scaled, slope * incomes_not_scaled + intercept, color='red', linewidth=2)
        axs[1, 0].set_title('incomes_not_scaled vs achievements_for_old_correlated')
        axs[1, 0].set_xlabel('incomes_not_scaled')
        axs[1, 0].set_ylabel('achievements_for_old_correlated')
        axs[1, 0].grid(True)

        # Plot 4: incomes vs achievements_for_old_correlated
        axs[1, 1].scatter(incomes, achievements_for_old_correlated, alpha=0.5)
        slope, intercept, _, _, _ = linregress(incomes, achievements_for_old_correlated)
        axs[1, 1].plot(incomes, slope * incomes + intercept, color='red', linewidth=2)
        axs[1, 1].set_title('incomes vs achievements_for_old_correlated')
        axs[1, 1].set_xlabel('incomes')
        axs[1, 1].set_ylabel('achievements_for_old_correlated')
        axs[1, 1].grid(True)

        # Save the plots to a file instead of showing them
        plt.tight_layout()
        plt.savefig('income_vs_achievement_plots.png')
        plt.close()

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


