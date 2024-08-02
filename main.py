import numpy as np
import pandas as pd
from src.simulation import generate_student_preferences, generate_school_preferences
from src.data_generation import generate_synthetic_data
from src.visualizations import (visualize_initial_locations,
                                plot_noisy_vs_true_achievements,
                                visualize_final_matches,
                                visualize_difference_in_matches)
from src.gale_shapley import deferred_acceptance
from src.analysis import compute_preference_statistics, compute_average_rank_distance


if __name__ == "__main__":
    # Set parameters for the simulation
    num_students = 1800
    num_schools = 10
    grid_size = 500
    weights = (0.2, 0.2, 0.2, 0.4)  # Weights for Distance, Quality, Income, Aspiration in student utility function
    noise_sd = 20

    # Print initial settings
    print(f"Initial Settings: \n"
          f"Number of Students: {num_students}\n"
          f"Number of Schools: {num_schools}\n"
          f"Grid Size: {grid_size}\n"
          f"Weights: {weights}\n"
          f"Weights: Distance, Quality, Income, Aspiration\n"
          f"Noise Standard Deviation: {noise_sd}\n")

    print("Starting synthetic data generation...")
    # Generate synthetic data for students and schools
    students, schools = generate_synthetic_data(num_students, num_schools, grid_size)
    print("Synthetic data generated.")

    # Visualize initial student and school locations
    visualize_initial_locations(students, schools, grid_size)

    print("\nGenerating preferences based on true achievements...")
    # Generate preferences based on true achievement
    generate_student_preferences(students, schools, [student.achievement for student in students], weights)
    generate_school_preferences(students, schools)
    print("Preferences based on true achievements generated.")

    # Store preferences after the true condition for comparison
    true_preferences = [student.preferences[:] for student in students]

    print("\nRunning Deferred Acceptance with true preferences...")
    # Run DA with true preferences
    student_preferences_true_dict = {student.id: student.preferences for student in students}
    school_preferences_dict = {school.id: school.preferences for school in schools}
    schools_capacity = {school.id: school.capacity for school in schools}
    final_matches_true = deferred_acceptance(student_preferences_true_dict, school_preferences_dict, schools_capacity)
    print("Deferred Acceptance with true preferences completed.")

    print("\nIntroducing noise to achievements and generating preferences...")
    # Add noise to achievements
    noisy_achievements = np.random.normal([student.achievement for student in students], noise_sd)
    noisy_achievements = np.clip(noisy_achievements, 0, 100)  # Ensure values stay within 0-100
    generate_student_preferences(students, schools, noisy_achievements, weights)
    print("Preferences based on noisy achievements generated.")

    # Store preferences after the noisy condition for comparison
    noisy_preferences = [student.preferences[:] for student in students]

    print("\nRunning Deferred Acceptance with noisy preferences...")
    # Run DA with noisy preferences
    student_preferences_noisy_dict = {student.id: student.preferences for student in students}
    final_matches_noisy = deferred_acceptance(student_preferences_noisy_dict, school_preferences_dict, schools_capacity)
    print("Deferred Acceptance with noisy preferences completed.")

    # # Print preferences for 5 random students under both conditions
    # print("\nComparing preferences and matches for 5 random students:")
    # for student in np.random.choice(students, 5, replace=False):
    #     print(f"\nStudent {student.id}:")
    #     print(f"  Location: {student.location}")
    #     print(f"  Income: {student.income:.2f}")
    #     print(f"  Achievement true: {student.achievement:.2f}")
    #     print(f"  Achievement noisy: {noisy_achievements[student.id]:.2f}")
    #     print(f"  Preferences (True): {true_preferences[student.id]}")
    #     print(f"  Preferences (Noisy): {noisy_preferences[student.id]}")
    #     print(f"  Matched School (True): {final_matches_true.get(student.id)}")
    #     print(f"  Matched School (Noisy): {final_matches_noisy.get(student.id)}")

    # # Print details and matched students for 5 random schools after each DA run
    # print("\nDetails and matched students for 5 random schools after DA run with true achievement:")
    # for school_id in np.random.choice(list(school_preferences_dict.keys()), 5, replace=False):
    #     matched_students_true = [student_id for student_id, matched_school_id in final_matches_true.items() if matched_school_id == school_id]
    #     print(f"\nSchool {school_id}:")
    #     school = schools[school_id]
    #     print(f"  Location: {school.location}")
    #     print(f"  Quality: {school.quality:.2f}")
    #     print(f"  Capacity: {school.capacity}")
    #     print(f"  Matched Students (True): {matched_students_true}")
    #
    # print("\nDetails and matched students for 5 random schools after DA run with noisy achievement:")
    # for school_id in np.random.choice(list(school_preferences_dict.keys()), 5, replace=False):
    #     matched_students_noisy = [student_id for student_id, matched_school_id in final_matches_noisy.items() if matched_school_id == school_id]
    #     print(f"\nSchool {school_id}:")
    #     school = schools[school_id]
    #     print(f"  Location: {school.location}")
    #     print(f"  Quality: {school.quality:.2f}")
    #     print(f"  Capacity: {school.capacity}")
    #     print(f"  Matched Students (Noisy): {matched_students_noisy}")

    # Visualize the final matches under both conditions
    visualize_final_matches(final_matches_noisy, final_matches_true, schools)

    # Visualize the difference in matches between the true and noisy conditions
    visualize_difference_in_matches(final_matches_noisy, final_matches_true)

    # visualize true vs noisy achievements
    plot_noisy_vs_true_achievements(students, noisy_achievements)

    # Export the data to an Excel file
    # print("\nExporting results to Excel...")
    # export_to_excel(students, final_matches_noisy, final_matches_true)
    # print("Data export completed.")

# Compute statistics
    true_percentages, true_unmatched_percentage = compute_preference_statistics(final_matches_true,
                                                                                true_preferences,
                                                                                num_students)
    noisy_percentages, noisy_unmatched_percentage = compute_preference_statistics(final_matches_noisy,
                                                                                  noisy_preferences,
                                                                                  num_students)
    average_rank_distance = compute_average_rank_distance(final_matches_noisy, true_preferences, noisy_preferences, num_students)

    print("\nStatistics for True Preferences:")
    print(f"1st choice: {true_percentages[0]:.2f}%")
    print(f"2nd choice: {true_percentages[1]:.2f}%")
    print(f"3rd choice: {true_percentages[2]:.2f}%")
    print(f"4th choice: {true_percentages[3]:.2f}%")
    print(f"5th choice: {true_percentages[4]:.2f}%")
    print(f"Other choices: {true_percentages[5]:.2f}%")
    print(f"Unmatched: {true_unmatched_percentage:.2f}%")

    print("\nStatistics for Noisy Preferences:")
    print(f"1st choice: {noisy_percentages[0]:.2f}%")
    print(f"2nd choice: {noisy_percentages[1]:.2f}%")
    print(f"3rd choice: {noisy_percentages[2]:.2f}%")
    print(f"4th choice: {noisy_percentages[3]:.2f}%")
    print(f"5th choice: {noisy_percentages[4]:.2f}%")
    print(f"Other choices: {noisy_percentages[5]:.2f}%")
    print(f"Unmatched: {noisy_unmatched_percentage:.2f}%")

    print(f"\nAverage rank distance between noisy and true matches: {average_rank_distance:.2f}")
