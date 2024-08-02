import numpy as np
from scipy.stats import rankdata

# Define the Student class to store attributes and preferences of each student
class Student:
    def __init__(self, id, location, income, achievement):
        # Each student has an ID, a location on the grid, an income level, and an academic achievement level
        self.id = id #A unique identifier for each student.
        self.location = location #A 2D location on a grid representing where the student lives.
        self.income = income #The income level of the student, which influences their preferences.
        self.achievement = achievement #The academic achievement level of the student, correlated with income.
        self.preferences = []  # This will store the student's preferences for schools
        self.matched_school = None  # This will store the ID of the school the student is matched to

    def __repr__(self):
        # Representation method to easily view student information
        return f"Student({self.id}, Loc: {self.location}, Inc: {self.income}, Ach: {self.achievement})"

# Define the School class to store attributes and preferences of each school
class School:
    def __init__(self, id, location, quality):
        # Each school has an ID, a location on the grid, and a quality level
        self.id = id
        self.location = location
        self.quality = quality
        self.capacity = 0  # This will store the number of students the school can admit
        self.preferences = []  # This will store the school's preferences for students

    def __repr__(self):
        # Representation method to easily view school information
        return f"School({self.id}, Loc: {self.location}, Qual: {self.quality})"

# Function to generate synthetic data for a given number of students and schools
def generate_synthetic_data(num_students, num_schools, grid_size):
    # disable next line later for monte carlo simulation
    np.random.seed(46)  # Set a random seed for reproducibility

    student_data = []
    # Mean and standard deviation for income and achievement distributions
    income_mean = 50
    achievement_mean = 50
    income_std = 10
    achievement_std = 30
    correlation = 0.3  # Correlation between income and achievement

    raw_achievements = []

    # Generate student data
    for i in range(num_students):
        location = np.random.randint(0, grid_size, 2)  # Random location on the grid

        if i == 0:
            # For the first student, generate income randomly based on normal distribution
            income = np.random.normal(income_mean, income_std)
        else:
            # WHY DID I INCLUDE THIS\???
            # For subsequent students, generate income correlated with the previous student's income
            income = np.random.normal(income_mean + correlation * (student_data[-1].income - income_mean),
                                      income_std * (1 - correlation ** 2) ** 0.5)

        # Generate achievement level correlated with income
        achievement = np.random.normal(achievement_mean + correlation * (income - income_mean),
                                       achievement_std * (1 - correlation ** 2) ** 0.5)

        raw_achievements.append(achievement)
        student_data.append(Student(i, location, income, achievement))

    # Calculate percentiles for achievement scores
    percentiles = rankdata(raw_achievements, method='average') / len(raw_achievements) * 100

    # Update student achievements with percentiles
    for student, percentile in zip(student_data, percentiles):
        student.achievement = percentile

    school_data = []
    # Generate school data
    for j in range(num_schools):
        location = np.random.randint(0, grid_size, 2)  # Random location on the grid
        quality = np.random.normal(50, 20)  # School quality with a mean of x and standard deviation of x
        school = School(j, location, quality)
        school.capacity = np.random.randint(50, 360)  # Random capacity between low x and high students
        school_data.append(school)

    # Return the generated student and school data
    return student_data, school_data
