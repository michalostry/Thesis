import numpy as np
from src.data_generation import (Student,
                                 School,
                                 generate_synthetic_data)

# Function to calculate the utility of a student attending a specific school
def calculate_student_utility(student,
                              school,
                              true_or_noisy_achievement,
                              weight_distance,
                              weight_quality,
                              weight_income,
                              weight_aspiration,
                              min_max_values,
                              debug_ids=None):
    # Unpack min_max values for normalization
    min_distance, max_distance = min_max_values['distance']
    min_quality, max_quality = min_max_values['quality']
    min_income, max_income = min_max_values['income']
    min_aspiration, max_aspiration = min_max_values['aspiration']

    # Calculate and normalize the distance
    distance = np.linalg.norm(student.location - school.location)
    normalized_distance = (distance - min_distance) / (max_distance - min_distance)

    # Normalize other components
    normalized_quality = (school.quality - min_quality) / (max_quality - min_quality)
    normalized_income = (student.income - min_income) / (max_income - min_income)
    aspiration_diff = (school.quality - true_or_noisy_achievement) ** 2
    normalized_aspiration = (aspiration_diff - min_aspiration) / (max_aspiration - min_aspiration)

    # Calculate weighted utility components
    quality_term = weight_quality * normalized_quality
    distance_term = weight_distance * normalized_distance
    income_term = weight_income * normalized_income
    aspiration_term = -weight_aspiration * normalized_aspiration
    aspiration_term = aspiration_term + 0.3 * normalized_income
    #this i shoudl reconsider

    # Sum to get total utility
    total_utility = quality_term - distance_term + income_term + aspiration_term

    # Debugging output
    if debug_ids and student.id in debug_ids:
        print(f"\n--- Debugging Student {student.id} ---")
        print(f"  School {school.id}:")
        print(f"    Distance Component: -{distance_term:.3f} (Normalized Distance: {normalized_distance:.2f})")
        print(f"    Quality Component: {quality_term:.2f} (Normalized Quality: {normalized_quality:.2f})")
        print(f"    Income Component: {income_term:.2f} (Normalized Income: {normalized_income:.2f})")
        print(f"    Aspiration Component: {aspiration_term:.3f} (Normalized Aspiration: {normalized_aspiration:.2f})")
        print(f"    Total Utility: {total_utility:.2f}")

    return total_utility, distance_term, quality_term, income_term, aspiration_term


# Function to generate students' preferences for schools based on their utilities
def generate_student_preferences(students, schools, true_or_noisy_achievements, weights, debug_ids, min_max_values):
    #print("All students:", students)
    # Unpack weights
    weight_distance, weight_quality, weight_income, weight_aspiration = weights

    utilities = {}  # Dictionary to store utilities for visualization

    # For each student, calculate preferences for schools based on utilities
    for student, true_or_noisy_achievement in zip(students, true_or_noisy_achievements):
        #print("Processing student:", student)

        # Calculate utility for each school and store the preference list
        preferences = []
        student_utilities = []  # List to store utilities for this student
        for school in schools:
            (utility,
             distance_term,
             quality_term,
             income_term,
             aspiration_term) = calculate_student_utility(
                student,
                school,
                true_or_noisy_achievement,
                weight_distance,
                weight_quality,
                weight_income,
                weight_aspiration,
                min_max_values,
                debug_ids
            )

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
    #income_term = weight_income * student.income  # Contribution of student's income to school's utility
    income_term = 0 #for now let's disable it
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