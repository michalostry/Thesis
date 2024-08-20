import numpy as np
import os
import pandas as pd
import random
import multiprocessing as mp
from src.other_functions import (save_to_csv)
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
from src.analysis import (compute_preference_statistics, compute_average_rank_distance,
                          compute_statistics, aggregate_simulation_results)
from configuration import configurations


def run_simulation_iteration(config, iteration, current_value, config_name):
    # Unpack the configuration and override the necessary fields
    num_iterations = config['num_iterations']
    num_students = config['num_students']
    num_schools = config['num_schools']
    grid_size = config['grid_size']
    weights = config['weights']
    noise_sd = config['noise_sd']
    noise_type = config['noise_type']
    income_scaling_factor = config['income_scaling_factor']
    debug_ids = config['debug_ids']
    school_capacity_min = config['school_capacity_min']
    school_capacity_max = config['school_capacity_max']
    config_name_base = config['config_name']

    variable_to_iterate = config['variable_to_iterate']
    start_value = config['start_value']
    increment = config['increment']
    variable_iterations = config['variable_iterations']

    # 1 - yes, 0 - no
    print_info = 0
    visualize_info = 0
    export_individual_run_data = 1
    save_as_csv = False  # Enable saving as CSV True or False
    save_mode = 'append'  # Options: 'append', 'new_each_run', 'new_on_first_iteration'

    save_single_iteration_results = True

    # Initialize a DataFrame to accumulate results for this configuration
    accumulated_iteration_results = pd.DataFrame()

    each_config_variable_iteration_iterated_results = []

    print(f"Running iteration {iteration + 1}/{num_iterations} for configuration {config_name}...")
    # Print initial settings

    if print_info == 1:
        print(f"---- Initial Settings: -----\n"
              f"Number of Students: {num_students}\n"
              f"Number of Schools: {num_schools}\n"
              f"Grid Size: {grid_size}\n"
              f"Weights: {weights}\n"
              f"Weights: Distance, Quality, Income Aspiration, Aspiration\n"
              f"Noise Standard Deviation: {noise_sd}\n"
              f"Students ID to debug: {debug_ids}\n")

    if print_info == 1: print("STEP 1 >>>> Starting synthetic data generation...")
    # Generate synthetic data for students and schools
    students, schools = generate_synthetic_data(num_students, num_schools, grid_size, school_capacity_min,
                                                school_capacity_max)
    if print_info == 1: print("Synthetic data generated.")

    # Visualize initial student and school locations
    if visualize_info == 1: visualize_initial_locations(students, schools, grid_size)

    if print_info == 1: print("\nSTEP 2 >>>> Generating preferences based on true achievements...")
    # Calculate min and max values for normalization
    min_max_values = get_min_max_values(students, schools)
    # Define true achievements
    true_achievements = [student.achievement for student in students]  # Extract true achievements
    # Generate preferences based on true achievement
    true_full_preferences, true_positive_preferences, utilities, saved_noise_utility = generate_student_preferences(
        students,
        schools,
        true_achievements,
        weights,
        debug_ids,
        min_max_values,
        saved_noise_utility=None,
        preference_type="True",  # Indicate true preferences,
    )
    generate_school_preferences(students, schools)
    if print_info == 1: print("Preferences based on true achievements generated.")

    # Store preferences after the true condition for comparison
    true_preferences = true_full_preferences

    if print_info == 1: print("\nSTEP 3 >>>> Running Deferred Acceptance with true preferences...")
    # Run DA with positive utility preferences
    student_preferences_true_dict = {student.id: true_positive_preferences[student.id] for student in
                                     students}
    school_preferences_dict = {school.id: school.preferences for school in schools}
    schools_capacity = {school.id: school.capacity for school in schools}
    final_matches_true = deferred_acceptance(student_preferences_true_dict, school_preferences_dict,
                                             schools_capacity, debug_ids)
    if print_info == 1: print("Deferred Acceptance with true preferences completed.")

    if print_info == 1: print(
        "\nSTEP 4 >>>> Introducing noise to achievements and generating preferences...")
    # Add noise to achievements
    # Introduce noise to achievements based on noise_type
    if noise_type == 'constant':
        noisy_achievements = np.random.normal(true_achievements, noise_sd)
    if noise_type == 'income_based_tiered_noise':
        # Calculate the probability of applying large noise
        noise_application_prob = np.clip(
            0.9 - income_scaling_factor * np.array([student.income for student in students]), 0.1,
            0.9)
        # Generate potential large and small noise
        base_noise_large = np.random.normal(0, noise_sd, num_students)
        base_noise_small = np.random.normal(0, 5, num_students)

        # Generate random values to decide whether to apply large noise
        random_values = np.random.rand(num_students)

        # Apply large noise where the random value is less than the noise application probability
        noise = np.where(random_values < noise_application_prob, base_noise_large, base_noise_small)

        # Generate noisy achievements
        noisy_achievements = np.array(true_achievements) + noise

        # Ensure noisy achievements stay within the range 0-100
        noisy_achievements = np.clip(noisy_achievements, 0, 100)

    noisy_achievements = np.clip(noisy_achievements, 0, 100)  # Ensure values stay within 0-100
    noisy_full_preferences, noisy_positive_preferences, noisy_utilities, saved_noise_utility = generate_student_preferences(
        students,
        schools,
        noisy_achievements,
        weights,
        debug_ids,
        min_max_values,
        saved_noise_utility,
        preference_type="Noisy",  # Indicate noisy preferences
    )
    if print_info == 1: print("Preferences based on noisy achievements generated.")

    # Store full preferences after the noisy condition for later comparison
    noisy_preferences = noisy_full_preferences

    if print_info == 1: print("\nSTEP 5 >>>> Running Deferred Acceptance with noisy preferences...")
    # Run DA with positive utility preferences for noisy achievements
    student_preferences_noisy_dict = {student.id: noisy_positive_preferences[student.id] for student in
                                      students}
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

    # Visualize the final matches under both conditions
    if visualize_info == 1: visualize_final_matches(final_matches_noisy, final_matches_true, schools)

    # Visualize the difference in matches between the true and noisy conditions
    if visualize_info == 1: visualize_difference_in_matches(final_matches_noisy, final_matches_true)

    # visualize true vs noisy achievements
    if visualize_info == 1: plot_noisy_vs_true_achievements(students, noisy_achievements)

    # The results for this iteration
    iteration_results = {
        'iteration': iteration + 1,
        'config_name': config_name,
        'num_students': config['num_students'],
        'num_schools': config['num_schools'],
        'total_capacity': total_capacity,
        'weights_distance': config['weights'][0],
        'weights_quality': config['weights'][1],
        'weights_income': config['weights'][2],
        'weights_aspiration': config['weights'][3],
        'noise_standard_deviation': config['noise_sd'],
        'grid_size': config['grid_size'],
    }

    iteration_name = f"iteration_{iteration + 1}"

    # Save the data to CSV files
    if export_individual_run_data == 1:
        df, df_schools = save_to_csv(students,
                                     final_matches_true,
                                     final_matches_noisy,
                                     true_preferences,
                                     noisy_preferences,
                                     noisy_achievements,
                                     utilities,
                                     schools,
                                     config_name,
                                     iteration_name,
                                     save_as_csv,
                                     save_mode,
                                     current_iteration=iteration + 1)

    # COMPUTING and saving STATISTICS FOR EACH ITERATION
    single_iteration_results = compute_statistics(df, df_schools)

    # Append current iteration results to the accumulated DataFrame
    accumulated_iteration_results = pd.concat([accumulated_iteration_results, single_iteration_results],
                                              ignore_index=True)

    # Consolidate additional columns into a new DataFrame
    additional_columns = pd.DataFrame({
        'Iteration Number': [iteration + 1],
        'Config Name': [config_name],
        'Iteration Name': [iteration_name]
    })

    # Concatenate these additional columns to the single_iteration_results DataFrame
    single_iteration_results = pd.concat([additional_columns, single_iteration_results], axis=1)

    single_results_file_path = os.path.join('data', 'single_iteration_results.csv')
    if save_single_iteration_results:
        single_iteration_results.to_csv(single_results_file_path, index=False, mode='a',
                                        header=not os.path.isfile(single_results_file_path))
    print("finished simulation")
    return single_iteration_results


def run_simulation_for_config(config):
    accumulated_iteration_results = pd.DataFrame()

    # Unpack the configuration and override the necessary fields
    variable_to_iterate = config.get('variable_to_iterate')
    start_value = config.get('start_value')
    increment = config.get('increment')
    variable_iterations = config.get('variable_iterations', 1)
    config_name_base = config['config_name']

    for i in range(max(variable_iterations, 1)):  # Ensure at least one iteration
        if variable_to_iterate is not None:
            current_value = start_value + i * increment

            # Update the corresponding variable based on the iteration
            if variable_to_iterate == 'noise_sd':
                config['noise_sd'] = current_value
            elif variable_to_iterate == 'income_scaling_factor':
                config['income_scaling_factor'] = current_value
            else:
                raise ValueError(f"Unknown variable to iterate: {variable_to_iterate}")

            # Create a unique configuration name for this iteration
            config_name = f"{config_name_base}_{i + 1}/{variable_iterations}_{variable_to_iterate}_{current_value:.1f}"
        else:
            # No iteration, use the base configuration name
            config_name = config_name_base

        total_weight = sum(config['weights'])
        if total_weight != 1:
            print("Total weights are not 1! Weights should add to 1.")

        # Run the simulations in parallel
        with mp.Pool() as pool:
            results = pool.starmap(run_simulation_iteration, [
                (config, iteration, current_value, config_name)
                for iteration in range(config['num_iterations'])
            ])

        # Collect the results
        for result in results:
            accumulated_iteration_results = pd.concat([accumulated_iteration_results, result], ignore_index=True)

    # Filter out non-numeric columns before aggregation
    numeric_columns = accumulated_iteration_results.select_dtypes(include=[np.number])

    # After all iterations are complete, aggregate the numeric results
    MC_RESULTS = aggregate_simulation_results([numeric_columns], config)

    # Save the final summary to a CSV file
    MC_RESULTS_file_path = os.path.join('data', 'MC_RESULTS.csv')
    MC_RESULTS.to_csv(MC_RESULTS_file_path, index=False, mode='a', header=not os.path.isfile(MC_RESULTS_file_path))

    # Calculate and print summary statistics
    average_rank_distance_all_runs = accumulated_iteration_results['average_rank_distance'].mean()
    print(
        f"\nMonte Carlo simulation completed with {config['num_iterations']} iterations for configuration {config_name_base}.")
    print(f"Average rank distance across all runs: {average_rank_distance_all_runs:.4f}")

    average_unchanged_matches_all_runs = accumulated_iteration_results['percentage_unchanged_matches'].mean()
    print(f"Average percentage of unchanged matches across all runs: {average_unchanged_matches_all_runs:.2f}%")
    print(f"Results saved to '{MC_RESULTS_file_path}'.\n_____")

    return accumulated_iteration_results


if __name__ == "__main__":
    all_config_results = []

    for config in configurations:
        config_results = run_simulation_for_config(config)  # Get results for this config
        all_config_results.append(config_results)  # Store results for all configs

    print("Monte Carlo simulation completed and results have been aggregated and saved.")
