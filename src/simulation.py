import numpy as np
from src.data_generation import Student, School, generate_synthetic_data


# Function to calculate the utility of a student attending a specific school
def calculate_student_utility(student, school, avg_income, noisy_achievement, weight_distance, weight_quality,
                              weight_income, weight_aspiration):
    # Calculate the Euclidean distance between the student's location and the school's location
    distance = np.linalg.norm(student.location - school.location)

    # The utility components are calculated based on the specified weights
    quality_term = weight_quality * school.quality  # Contribution of school quality to utility
    distance_term = weight_distance * distance  # Contribution of distance to utility (negative since distance is a cost)
    income_term = weight_income * avg_income  # Contribution of average income to utility
    aspiration_term = -weight_aspiration * (
                school.quality - noisy_achievement) ** 2  # Aspiration term penalizes mismatch

    # Total utility is the sum of these components
    utility = quality_term - distance_term + income_term + aspiration_term
    return utility


# Function to generate students' preferences for schools based on their utilities
def generate_student_preferences(students, schools, noisy_achievements, weights):
    # Unpack weights
    weight_distance, weight_quality_base, weight_income, weight_aspiration = weights

    # Calculate the average income of all students
    avg_income = np.mean([student.income for student in students])

    # For each student, calculate preferences for schools based on utilities
    for student, noisy_achievement in zip(students, noisy_achievements):
        # Adjust weight for quality based on student's income (higher income -> more weight on quality)
        weight_quality = weight_quality_base + 0.01 * student.income

        # Normalize weights to ensure they sum to 1
        total_weight = weight_distance + weight_quality + weight_income + weight_aspiration
        weight_quality /= total_weight
        weight_distance /= total_weight
        weight_income /= total_weight
        weight_aspiration /= total_weight

        # Calculate utility for each school and store the preference list
        preferences = []
        for school in schools:
            utility = calculate_student_utility(student, school, avg_income, noisy_achievement, weight_distance,
                                                weight_quality, weight_income, weight_aspiration)
            preferences.append((utility, school.id))

        # Sort preferences by utility (descending order)
        preferences.sort(reverse=True, key=lambda x: x[0])
        # Store only the school IDs, sorted by preference
        student.preferences = [school_id for _, school_id in preferences]


# Function to calculate the utility of a school from admitting a specific student
def calculate_school_utility(school, student, weight_income, weight_achievement):
    # The school's utility depends on the student's income and achievement
    income_term = weight_income * student.income  # Contribution of student's income to school's utility
    achievement_term = weight_achievement * student.achievement  # Contribution of student's achievement to utility

    # Total utility is the sum of these components
    utility = income_term + achievement_term
    return utility


# Function to generate schools' preferences for students based on their utilities
def generate_school_preferences(students, schools, weight_income=1.0, weight_achievement=1.0):
    # For each school, calculate preferences for students based on utilities
    for school in schools:
        preferences = []
        for student in students:
            utility = calculate_school_utility(school, student, weight_income, weight_achievement)
            preferences.append((utility, student.id))

        # Sort preferences by utility (descending order)
        preferences.sort(reverse=True, key=lambda x: x[0])
        # Store only the student IDs, sorted by preference
        school.preferences = [student_id for _, student_id in preferences]


# Function to run the overall simulation
def run_simulation(num_students, num_schools, grid_size, weights):
    # Generate synthetic data for students and schools
    students, schools = generate_synthetic_data(num_students, num_schools, grid_size)

    # Condition 1: Students observe a noisy signal of their achievement
    # Generate noisy achievements for students
    noisy_achievements = np.random.normal([student.achievement for student in students], 5)

    print("Condition 1: Noisy Achievement")
    # Generate student and school preferences based on noisy achievements
    generate_student_preferences(students, schools, noisy_achievements, weights)
    generate_school_preferences(students, schools)

    # Print out the preferences of the first few students for inspection
    for student in students[:5]:
        print(f"Student {student.id} preferences: {student.preferences}")

    print("\nCondition 2: True Achievement")
    # Condition 2: Students know their true achievement
    # Generate student and school preferences based on true achievements
    generate_student_preferences(students, schools, [student.achievement for student in students], weights)
    generate_school_preferences(students, schools)

    # Print out the preferences of the first few students and schools for inspection
    for student in students[:5]:
        print(f"Student {student.id} preferences: {student.preferences}")

    for school in schools[:5]:
        print(f"School {school.id} preferences: {school.preferences}")
