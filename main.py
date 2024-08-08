import numpy as np
import random
from src.other_functions import save_to_csv
from src.simulation import (generate_student_preferences,
                            generate_school_preferences,
                            calculate_student_utility)
from src.data_generation import (generate_synthetic_data,
                                 get_min_max_values)
from src.visualizations import (visualize_initial_locations,
                                plot_noisy_vs_true_achievements,
                                visualize_final_matches,
                                visualize_difference_in_matches,
                                visualize_utilities)
from src.gale_shapley import deferred_acceptance
from src.analysis import compute_preference_statistics, compute_average_rank_distance

if __name__ == "__main__":
    # Set parameters for the simulation
    num_students = 2000
    num_schools = 10
    grid_size = 50000
    weights = (0.3, 0.3, 0, 0.4)  # Weights for Distance, Quality, Income, Aspiration in student utility function
    #income currently 0 because it is not implemented yet
    noise_sd = 20
    debug_ids = []

    total_weight = sum(weights)
    if total_weight != 1:
        print("Total weight are not 1! Weights should add to 1.")

    # Print initial settings
    print(f"---- Initial Settings: -----\n"
          f"Number of Students: {num_students}\n"
          f"Number of Schools: {num_schools}\n"
          f"Grid Size: {grid_size}\n"
          f"Weights: {weights}\n"
          f"Weights: Distance, Quality, Income, Aspiration\n"
          f"Noise Standard Deviation: {noise_sd}\n"
          f"Students ID to debug: {debug_ids}\n")

    print("STEP 1 >>>> Starting synthetic data generation...")
    # Generate synthetic data for students and schools
    students, schools = generate_synthetic_data(num_students, num_schools, grid_size)
    print("Synthetic data generated.")

    # Visualize initial student and school locations
    #visualize_initial_locations(students, schools, grid_size)

    # Calculate min and max values for normalization
    min_max_values = get_min_max_values(students, schools)

    print("\nSTEP 2 >>>> Generating preferences based on true achievements...")
    # Define true achievements
    true_achievements = [student.achievement for student in students]  # Extract true achievements
    # Generate preferences based on true achievement
    utilities = generate_student_preferences(students,
                                             schools,
                                             true_achievements,  # Pass true achievements here
                                             weights,
                                             debug_ids,
                                             min_max_values)
    generate_school_preferences(students, schools)
    print("Preferences based on true achievements generated.")

    # Store preferences after the true condition for comparison
    true_preferences = [student.preferences[:] for student in students]

    print("\nSTEP 3 >>>> Running Deferred Acceptance with true preferences...")
    # Run DA with true preferences
    student_preferences_true_dict = {student.id: student.preferences for student in students}
    school_preferences_dict = {school.id: school.preferences for school in schools}
    schools_capacity = {school.id: school.capacity for school in schools}
    final_matches_true = deferred_acceptance(student_preferences_true_dict, school_preferences_dict, schools_capacity)
    print("Deferred Acceptance with true preferences completed.")

    print("\nSTEP 4 >>>> Introducing noise to achievements and generating preferences...")
    # Add noise to achievements
    noisy_achievements = np.random.normal([student.achievement for student in students], noise_sd)
    noisy_achievements = np.clip(noisy_achievements, 0, 100)  # Ensure values stay within 0-100
    generate_student_preferences(students,
                                 schools,
                                 noisy_achievements,
                                 weights,
                                 debug_ids,
                                 min_max_values)
    print("Preferences based on noisy achievements generated.")

    # Store preferences after the noisy condition for comparison
    noisy_preferences = [student.preferences[:] for student in students]

    print("\nSTEP 5 >>>> Running Deferred Acceptance with noisy preferences...")
    # Run DA with noisy preferences
    student_preferences_noisy_dict = {student.id: student.preferences for student in students}
    final_matches_noisy = deferred_acceptance(student_preferences_noisy_dict, school_preferences_dict, schools_capacity)
    print("Deferred Acceptance with noisy preferences completed.")

    print("\n >>> SIMULATION COMPLETED <<<")


    # Calculate total capacity
    total_capacity = sum(schools_capacity.values())
    # Print total capacity
    print(f"\nTotal School Capacity: {total_capacity}")
    print(f"Number of Students: {num_students}")
    print(f"Empty school spots: {total_capacity - num_students}")

    #Visualize the utilities
    #visualize_utilities(students[:5], schools, utilities)

    #avg RANK CALCULATION
    for student_id, noisy_match in final_matches_noisy.items():
        matched_school_true = final_matches_true.get(student_id)

        if noisy_match is not None and matched_school_true is not None:
            # Calculate rank in the true preferences for the matched school in true preferences
            true_rank = true_preferences[student_id].index(matched_school_true) + 1
            # Calculate the rank in the true preferences for the school matched in noisy conditions
            noisy_rank_in_true = true_preferences[student_id].index(noisy_match) + 1

            # Calculate the distance (noisy rank in true preferences - true rank)
            rank_distance = noisy_rank_in_true - true_rank

            #Print for debugging
            # print(f"Student {student_id}: True School = {matched_school_true}, Noisy School = {noisy_match}, "
            #      f"True Rank = {true_rank}, Noisy Rank in True Preferences = {noisy_rank_in_true}, Distance = {rank_distance}")

    # Visualize the final matches under both conditions
    #visualize_final_matches(final_matches_noisy, final_matches_true, schools)

    # Visualize the difference in matches between the true and noisy conditions
    #visualize_difference_in_matches(final_matches_noisy, final_matches_true)

    # visualize true vs noisy achievements
    #plot_noisy_vs_true_achievements(students, noisy_achievements)

# Compute statistics
    true_percentages, true_unmatched_percentage = compute_preference_statistics(final_matches_true,
                                                                                true_preferences,
                                                                                num_students)
    noisy_percentages, noisy_unmatched_percentage = compute_preference_statistics(final_matches_noisy,
                                                                                  noisy_preferences,
                                                                                  num_students)

    average_rank_distance = compute_average_rank_distance(final_matches_noisy,
                                                          final_matches_true,
                                                          true_preferences,
                                                          noisy_preferences)

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

    print(f"\nAverage rank distance between noisy and true matches: {average_rank_distance:.4f}")

# Save the data to CSV files
save_to_csv(students,
            final_matches_true,
            final_matches_noisy,
            true_preferences,
            noisy_preferences,
            noisy_achievements,
            schools)