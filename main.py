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
    num_iterations = 6  # Number of Monte Carlo iterations
    num_students = 1000
    num_schools = 20
    grid_size = 5000
    weights = (0.3, 0.3, 0, 0.4)
    # Distance, Quality, Income, Aspiration in student utility function
    # income currently 0 because it is not implemented yet
    noise_sd = 20 # 0 for no noise
    debug_ids = []  # empty for no debug
    school_capacity_min = 25
    school_capacity_max = 75


    # 1 - yes, 0 - no
    print_info = 0
    visualize_info = 0
    export_individual_run_data = 0

    # Initialize list to store results of each iteration
    all_results = []

    total_weight = sum(weights)
    if total_weight != 1:
        print("Total weight are not 1! Weights should add to 1.")

    for iteration in range(num_iterations):
        print(f"Running iteration {iteration + 1}/{num_iterations}...")
        # Print initial settings
        if print_info == 1:
            print(f"---- Initial Settings: -----\n"
                  f"Number of Students: {num_students}\n"
                  f"Number of Schools: {num_schools}\n"
                  f"Grid Size: {grid_size}\n"
                  f"Weights: {weights}\n"
                  f"Weights: Distance, Quality, Income, Aspiration\n"
                  f"Noise Standard Deviation: {noise_sd}\n"
                  f"Students ID to debug: {debug_ids}\n")

        if print_info == 1: print("STEP 1 >>>> Starting synthetic data generation...")
        # Generate synthetic data for students and schools
        students, schools = generate_synthetic_data(num_students, num_schools, grid_size, school_capacity_min, school_capacity_max)
        if print_info == 1: print("Synthetic data generated.")

        # Visualize initial student and school locations
        if visualize_info == 1: visualize_initial_locations(students, schools, grid_size)

        # Calculate min and max values for normalization
        min_max_values = get_min_max_values(students, schools)

        if print_info == 1: print("\nSTEP 2 >>>> Generating preferences based on true achievements...")
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
        if print_info == 1: print("Preferences based on true achievements generated.")

        # Store preferences after the true condition for comparison
        true_preferences = [student.preferences[:] for student in students]

        if print_info == 1: print("\nSTEP 3 >>>> Running Deferred Acceptance with true preferences...")
        # Run DA with true preferences
        student_preferences_true_dict = {student.id: student.preferences for student in students}
        school_preferences_dict = {school.id: school.preferences for school in schools}
        schools_capacity = {school.id: school.capacity for school in schools}
        final_matches_true = deferred_acceptance(student_preferences_true_dict, school_preferences_dict,
                                                 schools_capacity, debug_ids)
        if print_info == 1: print("Deferred Acceptance with true preferences completed.")

        if print_info == 1: print("\nSTEP 4 >>>> Introducing noise to achievements and generating preferences...")
        # Add noise to achievements
        noisy_achievements = np.random.normal([student.achievement for student in students], noise_sd)
        noisy_achievements = np.clip(noisy_achievements, 0, 100)  # Ensure values stay within 0-100
        generate_student_preferences(students,
                                     schools,
                                     noisy_achievements,
                                     weights,
                                     debug_ids,
                                     min_max_values)
        if print_info == 1: print("Preferences based on noisy achievements generated.")

        # Store preferences after the noisy condition for comparison
        noisy_preferences = [student.preferences[:] for student in students]

        if print_info == 1: print("\nSTEP 5 >>>> Running Deferred Acceptance with noisy preferences...")
        # Run DA with noisy preferences
        student_preferences_noisy_dict = {student.id: student.preferences for student in students}
        final_matches_noisy = deferred_acceptance(student_preferences_noisy_dict, school_preferences_dict,
                                                  schools_capacity, debug_ids)
        if print_info == 1: print("Deferred Acceptance with noisy preferences completed.")

        if print_info == 1: print("\n >>> SIMULATION COMPLETED <<<")

        # Calculate total capacity
        total_capacity = sum(schools_capacity.values())
        # Print total capacity
        if print_info == 1:
            print(f"\nTotal School Capacity: {total_capacity}")
            print(f"Number of Students: {num_students}")
            print(f"Empty school spots: {total_capacity - num_students}")

        # Visualize the utilities
        if visualize_info == 1: visualize_utilities(students[:5], schools, utilities)

        # avg RANK CALCULATION
        for student_id, noisy_match in final_matches_noisy.items():
            matched_school_true = final_matches_true.get(student_id)

            if noisy_match is not None and matched_school_true is not None:
                # Calculate rank in the true preferences for the matched school in true preferences
                true_rank = true_preferences[student_id].index(matched_school_true) + 1
                # Calculate the rank in the true preferences for the school matched in noisy conditions
                noisy_rank_in_true = true_preferences[student_id].index(noisy_match) + 1

                # Calculate the distance (noisy rank in true preferences - true rank)
                rank_distance = noisy_rank_in_true - true_rank

                # Print for debugging
                # # if print_info == 1:
                #     print(f"Student {student_id}: True School = {matched_school_true},"
                #           f" Noisy School = {noisy_match},"
                #           f" "f"True Rank = {true_rank},"
                #           f" Noisy Rank in True Preferences = {noisy_rank_in_true},"
                #           f" Distance = {rank_distance}")

        # Visualize the final matches under both conditions
        if visualize_info == 1: visualize_final_matches(final_matches_noisy, final_matches_true, schools)

        # Visualize the difference in matches between the true and noisy conditions
        if visualize_info == 1: visualize_difference_in_matches(final_matches_noisy, final_matches_true)

        # visualize true vs noisy achievements
        if visualize_info == 1: plot_noisy_vs_true_achievements(students, noisy_achievements)

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
                                                              noisy_preferences,
                                                              debug_ids)

        if print_info == 1:
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

        # Store results for this iteration
        iteration_results = {
            'iteration': iteration + 1,
            'num_students': num_students,
            'num_schools': num_schools,
            'total_capacity': total_capacity,
            'average_rank_distance': average_rank_distance,
            'true_1st_choice': true_percentages[0],
            'true_2nd_choice': true_percentages[1],
            'true_3rd_choice': true_percentages[2],
            'true_4th_choice': true_percentages[3],
            'true_5th_choice': true_percentages[4],
            'true_other_choices': true_percentages[5],
            'true_unmatched': true_unmatched_percentage,
            'noisy_1st_choice': noisy_percentages[0],
            'noisy_2nd_choice': noisy_percentages[1],
            'noisy_3rd_choice': noisy_percentages[2],
            'noisy_4th_choice': noisy_percentages[3],
            'noisy_5th_choice': noisy_percentages[4],
            'noisy_other_choices': noisy_percentages[5],
            'noisy_unmatched': noisy_unmatched_percentage,
            'weights_distance': weights[0],
            'weights_quality': weights[1],
            'weights_income': weights[2],
            'weights_aspiration': weights[3],
            'noise_standard_deviation': noise_sd,
            'grid_size': grid_size
        }

        all_results.append(iteration_results)

        # Save the data to CSV files
        if export_individual_run_data == 1:
            save_to_csv(students,
                        final_matches_true,
                        final_matches_noisy,
                        true_preferences,
                        noisy_preferences,
                        noisy_achievements,
                        schools)

# After all iterations, save or analyze the aggregated results
import os
import pandas as pd

# Specify the path to the data folder
data_folder = "data"

# Create the full path for the CSV file
csv_file_path = os.path.join(data_folder, "monte_carlo_results.csv")

# Convert results to a DataFrame
results_df = pd.DataFrame(all_results)

# Save the DataFrame to a CSV file in the data folder
results_df.to_csv(csv_file_path, index=False)

# After all iterations, calculate the average of average_rank_distance
average_rank_distance_all_runs = np.mean([result['average_rank_distance'] for result in all_results])

print(f"\nMonte Carlo simulation completed with {num_iterations} iterations.")
print(f"Average rank distance across all runs: {average_rank_distance_all_runs:.4f}")
print(f"Results saved to '{csv_file_path}'.")
