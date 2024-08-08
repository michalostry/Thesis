import numpy as np
from src.data_generation import (Student,
                                 School,
                                 generate_synthetic_data)


# Function to calculate the utility of a student attending a specific school
def calculate_student_utility(student, school, avg_income, noisy_achievement, weight_distance, weight_quality,
                              weight_income, weight_aspiration, grid_size, debug_ids=None):
    # Calculate the Euclidean distance between the student's location and the school's location
    distance = np.linalg.norm(student.location - school.location)

    # Normalize the distance by the maximum possible distance on the grid
    max_distance = np.sqrt(2) * grid_size  # Maximum distance on a square grid of size grid_size
    normalized_distance = distance / max_distance

    # Calculate utility components
    quality_term = weight_quality * school.quality
    distance_term = weight_distance * normalized_distance
    income_term = weight_income * avg_income
    aspiration_term = -weight_aspiration * (school.quality - noisy_achievement) ** 2

    # Total utility is the sum of these components
    total_utility = quality_term - distance_term + income_term + aspiration_term

    # Debugging: Print components if student ID is in the debug list
    if debug_ids and student.id in debug_ids:
        print(f"\n--- Debugging Student {student.id} ---")
        print(f"  School {school.id}:")
        print(f"    Distance Component: -{distance_term:.2f}")
        print(f"    Quality Component: {quality_term:.2f}")
        print(f"    Income Component: {income_term:.2f}")
        print(f"    Aspiration Component: {aspiration_term:.2f}")
        print(f"    Total Utility: {total_utility:.2f}")

    return total_utility, distance_term, quality_term, income_term, aspiration_term




# Function to generate students' preferences for schools based on their utilities
def generate_student_preferences(students, schools, noisy_achievements, weights, grid_size, debug_ids=None):
    # Unpack weights
    weight_distance, weight_quality_base, weight_income, weight_aspiration = weights

    # Calculate the average income of all students
    avg_income = np.mean([student.income for student in students])

    utilities = {}  # Dictionary to store utilities for visualization

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
        student_utilities = []  # List to store utilities for this student
        for school in schools:
            utility, _, _, _, _ = calculate_student_utility(student, school, avg_income, noisy_achievement,
                                                            weight_distance, weight_quality, weight_income,
                                                            weight_aspiration, grid_size, debug_ids)
            preferences.append((utility, school.id))
            student_utilities.append(utility)  # Collect utility for visualization

        utilities[student.id] = student_utilities  # Store utilities for the student

        # Sort preferences by utility (descending order)
        preferences.sort(reverse=True, key=lambda x: x[0])
        # Store only the school IDs, sorted by preference
        student.preferences = [school_id for _, school_id in preferences]

    return utilities  # Return utilities for visualization




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