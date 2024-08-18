print_info = 0 #1 - yes, 0 - no

import numpy as np

def compute_preference_statistics(final_matches, student_preferences, num_students):
    preference_counts = [0] * 6  # To count 1st, 2nd, 3rd, 4th, 5th, and 6th+ choices
    unmatched_count = 0

    for student_id, matched_school in final_matches.items():
        if matched_school is None:
            unmatched_count += 1
        else:
            try:
                rank = student_preferences[student_id].index(matched_school) + 1
                if rank <= 5:
                    preference_counts[rank - 1] += 1
                else:
                    preference_counts[5] += 1
            except ValueError:
                unmatched_count += 1

    percentages = [count / num_students * 100 for count in preference_counts]
    unmatched_percentage = unmatched_count / num_students * 100

    return percentages, unmatched_percentage


# def compute_average_rank_distance(final_matches_noisy, final_matches_true, true_preferences, noisy_preferences):
#     total_distance = 0
#     count = 0  # To count students with matches in both conditions
#
#     # Ensure all calculations are done within the same loop
#     for student_id, noisy_match in final_matches_noisy.items():
#         matched_school_true = final_matches_true.get(student_id)
#
#         # Only consider students matched under both conditions
#         if noisy_match is not None and matched_school_true is not None:
#             # Calculate rank in the true preferences
#             true_rank = true_preferences[student_id].index(noisy_match) if noisy_match in true_preferences[student_id] else len(true_preferences[student_id])
#             # Calculate rank in the noisy preferences
#             noisy_rank = noisy_preferences[student_id].index(noisy_match)
#             # Calculate the distance (noisy - true)
#             distance = noisy_rank - true_rank
#             total_distance += distance
#             count += 1
#
#             # Print for debugging purposes
#             print(f"Student {student_id}: True School = {matched_school_true}, Noisy School = {noisy_match}, True Rank = {true_rank + 1}, Noisy Rank = {noisy_rank + 1}, Distance = {distance}")
#
#     # Calculate the average distance
#     average_distance = total_distance / count if count > 0 else 0
#     if print_info == 1: print(f"\nFinal Average Rank Distance (Noisy - True): {average_distance:.2f}")
#     return average_distance

def compute_average_rank_distance(final_matches_noisy, final_matches_true, true_preferences, noisy_preferences, debug_ids):
    total_distance = 0
    count = 0  # To count students with matches in both conditions

    for student_id, noisy_match in final_matches_noisy.items():
        matched_school_true = final_matches_true.get(student_id)

        # Only include debug prints for the specified student
        if student_id in debug_ids:
            print("\n","Debugging student", student_id)
            print(f"Matched School (True): {matched_school_true}")
            print(f"Matched School (Noisy): {noisy_match}")

        # Only consider students matched under both conditions
        if noisy_match is not None and matched_school_true is not None:
            true_rank = true_preferences[student_id].index(matched_school_true) + 1 if matched_school_true in true_preferences[student_id] else None
            noisy_rank_in_true_preferences = true_preferences[student_id].index(noisy_match) + 1 if noisy_match in true_preferences[student_id] else None

            # If debugging this student, print ranks
            if student_id in debug_ids:
                print(f"True Rank: {true_rank}")
                print(f"Noisy Rank in True Preferences: {noisy_rank_in_true_preferences}")

            # Calculate the distance (Noisy Rank in True Preferences - True Rank)
            if true_rank is not None and noisy_rank_in_true_preferences is not None:
                rank_distance = (noisy_rank_in_true_preferences - true_rank)
                total_distance += rank_distance
                count += 1

                # If debugging this student, print rank distance
                if student_id in debug_ids:
                    print(f"Rank Distance (Noisy - True): {rank_distance}")
            elif student_id in debug_ids:
                print("Rank information missing for this student.")
        elif student_id in debug_ids:
            print("No match for this student in one or both conditions.")

    # Calculate the average distance
    average_distance = total_distance / count if count > 0 else 0

    # If debugging, print final average rank distance
    if debug_ids is not None:
        if print_info == 1: print(f"\nFinal Average Rank Distance (Noisy - True): {average_distance}")

    return average_distance


import pandas as pd
import numpy as np

def compute_statistics(df, df_schools):
    # Replace None or missing values with NaN to handle unmatched cases
    df = df.replace({None: np.nan})

    # Add flags to indicate if a student matched in the first and second rounds
    df['Matched in First Round'] = df['Matched School ID (True)'].notna()
    df['Matched in Second Round'] = df['Matched School ID (Noisy)'].notna()

    # Select only numeric columns for statistical calculations, excluding ID and Location columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    numeric_cols = numeric_cols.drop(['Student ID', 'Location X', 'Location Y'], errors='ignore')

    # 1. School-Level Statistics
    average_quality = df_schools['Quality'].mean()
    average_capacity = df_schools['Capacity'].mean()
    total_capacity = df_schools['Capacity'].sum()

    # 2. Student-Level Statistics (Overall)
    overall_stats = df[numeric_cols].mean(skipna=True)

    # Number and Percentage of Unchanged Matches
    unchanged_matches = df['Matched School ID (True)'] == df['Matched School ID (Noisy)']
    num_unchanged_matches = unchanged_matches.sum()
    percentage_unchanged_matches = (num_unchanged_matches / len(df)) * 100

    # Statistics for Students Matched in the First Round Only
    first_round_stats = df[df['Matched in First Round'] & ~df['Matched in Second Round']][numeric_cols].mean(skipna=True)

    # Statistics for Students Matched in the Second Round Only
    second_round_stats = df[df['Matched in Second Round'] & ~df['Matched in First Round']][numeric_cols].mean(skipna=True)

    # Statistics for Students Matched in Both Rounds
    both_rounds_stats = df[df['Matched in First Round'] & df['Matched in Second Round']][numeric_cols].mean(skipna=True)

    # 3. Statistics by Income Quintiles
    df['Income Quintile'] = pd.qcut(df['Income'], 5, labels=False) + 1
    quintile_group_stats = df.groupby('Income Quintile')[numeric_cols].mean()

    # 4. Statistics for Students with Match Change
    df_changed = df[~unchanged_matches]
    changed_stats = df_changed[numeric_cols].mean(skipna=True)

    # 5. Preference Statistics
    # Treat NaN as unmatched (i.e., fill with 0) and count them as such
    true_choices = df['Rank in True Preferences (True)'].fillna(0).astype(int).value_counts(normalize=True).sort_index()
    noisy_choices = df['Rank in True Preferences (Noisy)'].fillna(0).astype(int).value_counts(normalize=True).sort_index()

    true_percentages = [
        true_choices.get(1, 0) * 100,
        true_choices.get(2, 0) * 100,
        true_choices.get(3, 0) * 100,
        true_choices.get(4, 0) * 100,
        true_choices.get(5, 0) * 100,
        true_choices[true_choices.index > 5].sum() * 100
    ]

    noisy_percentages = [
        noisy_choices.get(1, 0) * 100,
        noisy_choices.get(2, 0) * 100,
        noisy_choices.get(3, 0) * 100,
        noisy_choices.get(4, 0) * 100,
        noisy_choices.get(5, 0) * 100,
        noisy_choices[noisy_choices.index > 5].sum() * 100
    ]

    true_unmatched_percentage = 100 - df['Matched in First Round'].mean() * 100
    noisy_unmatched_percentage = 100 - df['Matched in Second Round'].mean() * 100

    # Debugging print statements to verify statistics
    # print("True Percentages:", true_percentages)
    # print("Noisy Percentages:", noisy_percentages)
    # print("True Unmatched Percentage:", true_unmatched_percentage)
    # print("Noisy Unmatched Percentage:", noisy_unmatched_percentage)

    # Consolidate Results
    single_iteration_results = pd.DataFrame({
        'average_school_quality': [average_quality],
        'average_school_capacity': [average_capacity],
        'total_school_capacity': [total_capacity],

        'average_income': [overall_stats['Income']],
        'average_achievement': [overall_stats['Achievement']],
        'average_noisy_achievement': [overall_stats['Noisy Achievement']],
        'average_rank_true': [overall_stats['Rank in True Preferences (True)']],
        'average_utility_true': [overall_stats['Utility of Matched School (True)']],
        'average_utility_noisy_under_true': [overall_stats['Utility of Matched School under Noisy (True)']],
        'average_utility_distance': [overall_stats['Utility Distance']],
        'average_relative_utility_difference': [overall_stats['Relative Utility Difference']],
        'average_rank_noisy': [overall_stats['Rank in True Preferences (Noisy)']],
        'average_rank_distance': [overall_stats['Rank Distance (Noisy - True)']],
        'average_relative_rank_difference': [overall_stats['Relative Rank Difference']],

        'num_unchanged_matches': [num_unchanged_matches],
        'percentage_unchanged_matches': [percentage_unchanged_matches],

        'average_income_first_round_only': [first_round_stats['Income']],
        'average_achievement_first_round_only': [first_round_stats['Achievement']],
        'average_utility_true_first_round_only': [first_round_stats['Utility of Matched School (True)']],

        'average_income_second_round_only': [second_round_stats['Income']],
        'average_achievement_second_round_only': [second_round_stats['Achievement']],
        'average_utility_noisy_under_true_second_round_only': [
            second_round_stats['Utility of Matched School under Noisy (True)']],

        'average_income_both_rounds': [both_rounds_stats['Income']],
        'average_achievement_both_rounds': [both_rounds_stats['Achievement']],
        'average_utility_both_rounds': [both_rounds_stats['Utility of Matched School under Noisy (True)']],

        'true_1st_choice': [true_percentages[0]],
        'true_2nd_choice': [true_percentages[1]],
        'true_3rd_choice': [true_percentages[2]],
        'true_4th_choice': [true_percentages[3]],
        'true_5th_choice': [true_percentages[4]],
        'true_other_choices': [true_percentages[5]],
        'true_unmatched': [true_unmatched_percentage],
        'noisy_1st_choice': [noisy_percentages[0]],
        'noisy_2nd_choice': [noisy_percentages[1]],
        'noisy_3rd_choice': [noisy_percentages[2]],
        'noisy_4th_choice': [noisy_percentages[3]],
        'noisy_5th_choice': [noisy_percentages[4]],
        'noisy_other_choices': [noisy_percentages[5]],
        'noisy_unmatched': [noisy_unmatched_percentage],
    })

    # Append quintile stats to the results
    for quintile in range(1, 6):
        for col in quintile_group_stats.columns:
            single_iteration_results[f'{col}_quintile_{quintile}'] = [quintile_group_stats.loc[quintile, col]]

    # Append changed stats to the results
    for col in changed_stats.index:
        single_iteration_results[f'average_{col}_changed'] = [changed_stats[col]]

    return single_iteration_results



import pandas as pd
def aggregate_simulation_results(all_iterations_results, config):
    """
    Aggregates the results of all iterations in the Monte Carlo simulation.

    Parameters:
    - all_iterations_results: List of DataFrames, where each DataFrame is the result of a single iteration.
    - config: Dictionary containing the settings of the current configuration.

    Returns:
    - final_summary: DataFrame with the aggregated results of the simulation.
    """

    # Concatenate all iteration results into a single DataFrame
    aggregated_results = pd.concat(all_iterations_results, ignore_index=True)

    # Calculate the mean for each variable across all iterations
    mean_results = aggregated_results.mean()

    # Convert the mean results to a DataFrame
    final_summary = pd.DataFrame(mean_results).T  # Transpose to get variables as columns

    # Add configuration details to the final summary
    final_summary['config_name'] = config['config_name']
    final_summary['weights_distance'] = config['weights'][0]
    final_summary['weights_quality'] = config['weights'][1]
    final_summary['weights_income'] = config['weights'][2]
    final_summary['weights_aspiration'] = config['weights'][3]
    final_summary['noise_standard_deviation'] = config['noise_sd']
    final_summary['grid_size'] = config['grid_size']
    final_summary['num_iterations'] = config['num_iterations']
    final_summary['num_students'] = config['num_students']
    final_summary['num_schools'] = config['num_schools']
    final_summary['noise_type'] = config['noise_type']
    final_summary['income_scaling_factor'] = config['income_scaling_factor']

    # Reorder columns to place config_name at the beginning
    cols = ['config_name'] + [col for col in final_summary.columns if col != 'config_name']
    final_summary = final_summary[cols]

    return final_summary








