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
                              weight_income_aspiration,
                              weight_aspiration,
                              min_max_values,
                              aspiration_range,
                              debug_ids=None):
    # Unpack min_max values for normalization
    min_distance, max_distance = min_max_values['distance']
    min_income, max_income = min_max_values['income']

    # Use individual student's aspiration range
    min_aspiration = aspiration_range['min_aspiration']
    max_aspiration = aspiration_range['max_aspiration']

    # Calculate and normalize the distance
    distance = np.linalg.norm(student.location - school.location)
    normalized_distance = (distance - min_distance) / (max_distance - min_distance)

    # Normalize other components
    #normalized_quality = (school.quality - min_quality) / (max_quality - min_quality)
    quality = school.quality/100
    normalized_income = (student.income - min_income) / (max_income - min_income)
    aspiration_diff = (school.quality - true_or_noisy_achievement) ** 2
    normalized_aspiration = (aspiration_diff - min_aspiration) / (max_aspiration - min_aspiration)

    # Calculate weighted utility components
    utility_any_school = 0.05
    quality_term =  utility_any_school + (weight_quality * quality)
    distance_term = -weight_distance * normalized_distance
    income_aspiration_term = weight_income_aspiration * normalized_income * quality
    aspiration_term = -weight_aspiration * normalized_aspiration

    # Sum to get total utility
    total_utility = quality_term + distance_term + income_aspiration_term + aspiration_term


    # Debugging output
    if debug_ids and student.id in debug_ids:
        print(f"\n--- Debugging Student {student.id} ---")
        print(f"  School {school.id}:")

        print(f"    Distance Component: {distance_term:.3f}")
        print(f"        Calculation: {weight_distance:.3f} * {normalized_distance:.3f} (normalized distance)")

        print(f"    Quality Component: {quality_term:.2f}")
        print(
            f"        Calculation: ({utility_any_school:.3f} (Utility from attending any school) + ({weight_quality:.3f} * {quality:.3f} (quality))")

        print(f"    Income Aspiration Component: {income_aspiration_term:.2f}")
        print(
            f"        Calculation: {weight_income_aspiration:.3f} * {normalized_income:.3f} (normalized income) * {quality:.3f} (quality)")

        print(f"    Aspiration Component: {aspiration_term:.3f}")
        print(f"        Calculation: {weight_aspiration:.3f} * {normalized_aspiration:.3f} (normalized aspiration)")

        print(f"    Total Utility: {total_utility:.2f}")

    return total_utility, distance_term, quality_term, income_aspiration_term, aspiration_term


# Function to calculate the min and max aspiration for an individual student
def calculate_student_aspiration_range(student, schools, true_or_noisy_achievement):
    aspirations = []
    for school in schools:
        aspiration_diff = (school.quality - true_or_noisy_achievement) ** 2
        aspirations.append(aspiration_diff)

    min_aspiration = min(aspirations)
    max_aspiration = max(aspirations)

    return {'min_aspiration': min_aspiration, 'max_aspiration': max_aspiration}


# Function to generate students' preferences for schools based on their utilities
def generate_student_preferences(students, schools, true_or_noisy_achievements, weights, debug_ids, min_max_values):
    #print("All students:", students)
    # Unpack weights
    weight_distance, weight_quality, weight_income_aspiration, weight_aspiration = weights

    full_preferences = {}  # Full preference list
    positive_preferences = {}  # Preference list with only positive utilities
    utilities = {}  # Dictionary to store utilities for visualization

    # For each student, calculate preferences for schools based on utilities
    for student, true_or_noisy_achievement in zip(students, true_or_noisy_achievements):
        # Calculate individual aspiration range
        aspiration_range = calculate_student_aspiration_range(student, schools, true_or_noisy_achievement)

        # Calculate utility for each school and store the preference list
        preferences = []
        positive_pref_list = []
        student_utilities = []
        for school in schools:
            (utility,
             distance_term,
             quality_term,
             income_aspiration_term,
             aspiration_term) = calculate_student_utility(
                student,
                school,
                true_or_noisy_achievement,
                weight_distance,
                weight_quality,
                weight_income_aspiration,
                weight_aspiration,
                min_max_values,
                aspiration_range,
                debug_ids
            )

            preferences.append((utility, school.id))
            student_utilities.append(utility)  # Collect utility for visualization

            # Add to positive preferences if utility is positive
            if utility > 0:
                positive_pref_list.append((utility, school.id))

        utilities[student.id] = student_utilities  # Store utilities for the student

        # Sort preferences by utility (descending order)
        preferences.sort(reverse=True, key=lambda x: x[0])
        positive_pref_list.sort(reverse=True, key=lambda x: x[0])

        # Store only the school IDs, sorted by preference
        full_preferences[student.id] = [school_id for _, school_id in preferences]
        positive_preferences[student.id] = [school_id for _, school_id in positive_pref_list]

    return full_preferences, positive_preferences, utilities  # Return both preference lists and utilities


# Function to calculate the utility of a school from admitting a specific student
def calculate_school_utility(school, student, weight_income_aspiration, weight_achievement):
    # The school's utility depends on the student's income and achievement
    #income_term = weight_income * student.income  # Contribution of student's income to school's utility
    income_term = 0 #for now let's disable it
    achievement_term = weight_achievement * student.achievement  # Contribution of student's achievement to utility

    # Total utility is the sum of these components
    utility = income_term + achievement_term
    return utility


# Function to generate schools' preferences for students based on their utilities
def generate_school_preferences(students, schools, weight_income_aspiration=1.0, weight_achievement=1.0):
    # For each school, calculate preferences for students based on utilities
    for school in schools:
        preferences = []
        for student in students:
            utility = calculate_school_utility(school, student, weight_income_aspiration, weight_achievement)
            preferences.append((utility, student.id))

        # Sort preferences by utility (descending order)
        preferences.sort(reverse=True, key=lambda x: x[0])
        # Store only the student IDs, sorted by preference
        school.preferences = [student_id for _, student_id in preferences]