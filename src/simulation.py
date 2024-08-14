import numpy as np
from src.data_generation import (Student,
                                 School,
                                 generate_synthetic_data)

# Function to calculate the utility of a student attending a specific school
def calculate_student_utility(students, schools, true_or_noisy_achievements, weights, min_max_values, preference_type, saved_noise_utility, debug_ids=None):
    weight_distance, weight_quality, weight_income_aspiration, weight_aspiration = weights
    num_students = len(students)
    num_schools = len(schools)

    # Extract locations and qualities into NumPy arrays
    student_locations = np.array([student.location for student in students])
    student_incomes = np.array([student.income for student in students])
    school_locations = np.array([school.location for school in schools])
    school_qualities = np.array([school.quality for school in schools])

    # Calculate distances between students and schools
    distances = np.linalg.norm(student_locations[:, np.newaxis, :] - school_locations[np.newaxis, :, :], axis=2)

    # Scale distances so that the maximum distance becomes 1, while preserving relative differences
    max_distance = np.max(distances)
    scaled_distances = distances / (max_distance + 1e-6)

    # Normalize distances
    #min_distance, max_distance = min_max_values['distance']
    #normalized_distances = (distances - min_distance) / (max_distance - min_distance + 1e-6)

    # not normalized anymore, income is scaled to max = 1 alredy in the data generation
    # Normalize incomes
    # min_income, max_income = min_max_values['income']
    # normalized_incomes = (student_incomes - min_income) / (max_income - min_income + 1e-6)

    # Calculate individual aspiration range for each student
    aspiration_diffs = (school_qualities[np.newaxis, :] - np.array(true_or_noisy_achievements)[:, np.newaxis]) ** 2
    # max_aspiration_diff = np.max(aspiration_diffs)
    # scaled_aspirations = aspiration_diffs / (max_aspiration_diff + 1e-6)

    # old approach to min max normalization
    min_aspirations = np.min(aspiration_diffs, axis=1, keepdims=True)
    max_aspirations = np.max(aspiration_diffs, axis=1, keepdims=True)
    normalized_aspirations = (aspiration_diffs - min_aspirations) / (max_aspirations - min_aspirations + 1e-6)
    scaled_aspirations =normalized_aspirations

    # Add noise to the utility calculation
    if preference_type == "True":
        noise_utility = np.random.normal(0, 0.01, (num_students, num_schools))
        #noise_utility = 0
        saved_noise_utility = noise_utility
    else:
        noise_utility = saved_noise_utility

    attending_utility = 0.05
    # Calculate utility for each student-school pair
    utilities = (
            attending_utility + weight_quality * (school_qualities / 100)
            # now muted - old approach
            # - weight_distance * normalized_distances
            - weight_distance * scaled_distances
            + weight_income_aspiration * student_incomes[:, np.newaxis] * (school_qualities / 100)
            - weight_aspiration * normalized_aspirations
            + noise_utility
    )

    # Debugging
    if debug_ids:
        for i, student in enumerate(students):
            if student.id in debug_ids:
                print(f"\n--- Debugging Student {student.id} ---")
                for j, school in enumerate(schools):
                    print(f"  School {school.id}:")
                    print(f"    Achievement: {true_or_noisy_achievements[i]:.3f}")
                    print(
                        f"    Distance Component: {-weight_distance * scaled_distances[i, j]:.3f} = {weight_distance:.1f} * scaled distance: {scaled_distances[i, j]:.1f}")
                    print(
                        f"    Quality Component: {attending_utility + weight_quality * (school_qualities[j] / 100):.3f} = attending u {attending_utility:.3f} + {weight_quality:.1f} * School qualities: {school_qualities[j]:.1f} / 100")
                    print(
                        f"    Income Aspiration Component: {weight_income_aspiration * student_incomes[i] * (school_qualities[j] / 100):.3f} = {weight_income_aspiration:.1f} * scaled_incomes {student_incomes[i]:.3f} * School qualities: {school_qualities[j]:.1f} / 100")
                    print(
                        f"    Aspiration Component: {-weight_aspiration * normalized_aspirations[i, j]:.3f} = {weight_aspiration:.1f} * scaled aspiration {normalized_aspirations[i, j]:.1f}"),
                    print(f"    Noise Added: {noise_utility[i, j]:.3f}")
                    print(f"    Total Utility: {utilities[i, j]:.3f}")

    return utilities, saved_noise_utility

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
def generate_student_preferences(students, schools, true_or_noisy_achievements, weights, debug_ids, min_max_values, saved_noise_utility, preference_type):
    utilities, saved_noise_utility = calculate_student_utility(students, schools, true_or_noisy_achievements, weights, min_max_values, preference_type, saved_noise_utility, debug_ids)

    # Sort preferences by utility (descending order)
    sorted_indices = np.argsort(-utilities, axis=1)

    # Prepare the full and positive preferences
    full_preferences = {}
    positive_preferences = {}
    for i, student in enumerate(students):
        sorted_utilities = utilities[i][sorted_indices[i]]
        full_preferences[student.id] = sorted_indices[i].tolist()
        positive_preferences[student.id] = sorted_indices[i][sorted_utilities > 0].tolist()  # Direct utility check

    # Debugging output for preferences
    if debug_ids:
        for student_id in debug_ids:
            print(f"\n--- Debugging Preferences for Student {student_id} ---")
            print(f"Full Preferences: {full_preferences[student_id]}")
            print(f"Positive Preferences: {positive_preferences[student_id]}")
            print(f"Utilities: {utilities[student_id]}")

    return full_preferences, positive_preferences, utilities, saved_noise_utility

# Function to calculate the utility of a school from admitting a specific student
def calculate_school_utility(school, student, weight_income_aspiration, weight_achievement):
    achievement_term = weight_achievement * student.achievement
    return achievement_term


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