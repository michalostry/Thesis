import numpy as np
from scipy.stats import rankdata
from scipy.spatial.distance import pdist, squareform

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


# Function to generate spatially correlated data
def generate_spatially_correlated_data(locations, mean, std, correlation_length):
    # Calculate pairwise distances between locations
    distances = squareform(pdist(locations))

    # Generate a spatially correlated covariance matrix
    covariance_matrix = np.exp(-distances / correlation_length)

    # Generate correlated random variables
    correlated_data = np.random.multivariate_normal(mean * np.ones(len(locations)),
                                                    std ** 2 * covariance_matrix)
    return correlated_data


# Function to generate synthetic data for a given number of students and schools
def generate_synthetic_data(num_students, num_schools, grid_size, correlation_length=1000):
    np.random.seed(46)  # Set a random seed for reproducibility

    # Mean and standard deviation for income and achievement distributions
    income_mean = 50
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
        school.capacity = np.random.randint(50, 360)
        school_data.append(school)

    return student_data, school_data
