print_info = 1 #1 - yes, 0 - no
set_seed = 0 #1 - yes, 0 - no

import numpy as np
from scipy.stats import rankdata
from scipy.spatial.distance import pdist, squareform
from scipy.linalg import cholesky

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

def generate_spatially_correlated_data(locations, mean, std, correlation_length, epsilon=1e-6):
    if print_info == 1:print("Step 1: Calculating pairwise distances...")
    # Calculate pairwise distances between locations
    distances = squareform(pdist(locations))

    if print_info == 1:print("Step 2: Generating covariance matrix...")
    # Generate a spatially correlated covariance matrix
    covariance_matrix = np.exp(-distances / correlation_length)

    # Add a small value to the diagonal to ensure positive definiteness
    covariance_matrix += np.eye(covariance_matrix.shape[0]) * epsilon

    if print_info == 1:print("Step 3: Performing Cholesky decomposition...")
    # Use Cholesky decomposition instead of SVD
    L = cholesky(covariance_matrix, lower=True)

    if print_info == 1:print("Step 4: Generating independent normal variables...")
    # Generate independent standard normal variables
    independent_normals = np.random.normal(size=len(locations))

    if print_info == 1:print("Step 5: Applying Cholesky factor to generate correlated data...")
    # Apply Cholesky factor to get correlated data
    correlated_data = mean + std * np.dot(L, independent_normals)

    if print_info == 1:print("Step 6: Correlated data generation complete.")
    return correlated_data


# Function to generate synthetic data for a given number of students and schools
def generate_synthetic_data(num_students, num_schools, grid_size, correlation_length=1000):
    if print_info == 1: print("generate_synthetic_data")
    if set_seed == 1: np.random.seed(46)  # Set a random seed for reproducibility

    # Mean and standard deviation for income and achievement distributions
    income_mean = 50
    #let's change this distribution to reflect reality more later
    achievement_mean = 50
    income_std = 10
    achievement_std = 30
    correlation = 0.3  # Correlation between income and achievement

    # Generate random locations for students
    locations = np.random.randint(0, grid_size, (num_students, 2))

    # Generate spatially correlated income data
    incomes = generate_spatially_correlated_data(locations, income_mean, income_std, correlation_length)

    # Generate achievements correlated with income
    raw_achievements = np.random.normal(achievement_mean + correlation * (incomes - income_mean),
                                        achievement_std * (1 - correlation ** 2) ** 0.5)

    # Convert achievements to percentiles
    percentiles = rankdata(raw_achievements, method='average') / len(raw_achievements) * 100

    # Create Student objects
    student_data = []
    for i in range(num_students):
        student_data.append(Student(i, locations[i], incomes[i], percentiles[i]))

    # Generate school data
    school_data = []
    for j in range(num_schools):
        location = np.random.randint(0, grid_size, 2)
        quality = np.random.normal(50, 20)
        school = School(j, location, quality)
        school.capacity = np.random.randint(25, 75)
        school_data.append(school)

    return student_data, school_data

def get_min_max_values(students, schools):
    if print_info == 1: print("get_min_max")
    distances = []
    qualities = []
    incomes = [student.income for student in students]
    aspirations = []

    for student in students:
        for school in schools:
            distance = np.linalg.norm(student.location - school.location)
            distances.append(distance)
            qualities.append(school.quality)
            aspiration = (school.quality - student.achievement) ** 2
            aspirations.append(aspiration)

    min_distance, max_distance = min(distances), max(distances)
    min_quality, max_quality = min(qualities), max(qualities)
    min_income, max_income = min(incomes), max(incomes)
    min_aspiration, max_aspiration = min(aspirations), max(aspirations)

    return {
        'distance': (min_distance, max_distance),
        'quality': (min_quality, max_quality),
        'income': (min_income, max_income),
        'aspiration': (min_aspiration, max_aspiration)
    }
