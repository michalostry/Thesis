import os
import csv
import pandas as pd
from datetime import datetime
import numpy as np


def save_to_csv(students,
                final_matches_true,
                final_matches_noisy,
                true_preferences,
                noisy_preferences,
                noisy_achievements,
                utilities_true,
                schools,
                config_name,
                iteration_name,
                save_as_csv,  # Option to save as CSV or not
                save_mode,  # Options: 'append', 'new_each_run', 'new_on_first_iteration'
                current_iteration=1):  # Track the current iteration for conditional saving

    # Create an empty list to store each student's data
    data_rows = []

    for student, noisy_achievement in zip(students, noisy_achievements):
        student_id = student.id
        location_x, location_y = student.location
        income = student.income
        achievement = student.achievement

        # Matched school and rank in true condition
        matched_school_true = final_matches_true.get(student_id)
        if matched_school_true is not None:
            rank_true = true_preferences[student_id].index(matched_school_true) + 1
            utility_true = utilities_true[student_id][matched_school_true]
        else:
            rank_true = None
            utility_true = None

        # Matched school and rank in noisy condition
        matched_school_noisy = final_matches_noisy.get(student_id)
        if matched_school_noisy is not None:
            rank_noisy = true_preferences[student_id].index(matched_school_noisy) + 1 if matched_school_noisy in \
                                                                                         true_preferences[
                                                                                             student_id] else None
            utility_noisy_under_true = utilities_true[student_id][
                matched_school_noisy] if rank_noisy is not None else None
        else:
            rank_noisy = None
            utility_noisy_under_true = None

        # Calculate rank distance
        if rank_true is not None and rank_noisy is not None:
            rank_distance = rank_noisy - rank_true
        else:
            rank_distance = None

        # Calculate utility distance
        if utility_true is not None and utility_noisy_under_true is not None:
            utility_distance = utility_true - utility_noisy_under_true
        else:
            utility_distance = None

        # Calculate relative utility difference
        if utility_true is not None and utility_true != 0 and utility_distance is not None:
            relative_utility_difference = np.clip(utility_distance / abs(utility_true),-10,10)
        else:
            relative_utility_difference = None

        # Calculate relative rank difference (ordinal measure)
        if rank_true is not None and rank_noisy is not None and rank_true != 0:
            relative_rank_difference = (rank_distance / rank_true)
        else:
            relative_rank_difference = None

        # Append the data for this student to the list as a dictionary
        data_rows.append({
            'Config Name': config_name,
            'Iteration': iteration_name,
            'Student ID': student_id,
            'Location X': location_x,
            'Location Y': location_y,
            'Income': income,
            'Achievement': achievement,
            'Noisy Achievement': noisy_achievement,
            'Matched School ID (True)': matched_school_true,
            'Rank in True Preferences (True)': rank_true,
            'Utility of Matched School (True)': utility_true,
            'Utility of Matched School under Noisy (True)': utility_noisy_under_true,
            'Utility Distance': utility_distance,
            'Relative Utility Difference': relative_utility_difference,
            'Matched School ID (Noisy)': matched_school_noisy,
            'Rank in True Preferences (Noisy)': rank_noisy,
            'Rank Distance (Noisy - True)': rank_distance,
            'Relative Rank Difference': relative_rank_difference
        })

    # Convert the list of dictionaries into a DataFrame
    df = pd.DataFrame(data_rows)

    # Now save school data as well
    school_data_rows = []
    for school in schools:
        school_id = school.id
        location_x, location_y = school.location
        quality = school.quality
        capacity = school.capacity

        # Append the data for this school to the list as a dictionary
        school_data_rows.append({
            'Config Name': config_name,
            'Iteration': iteration_name,
            'School ID': school_id,
            'Location X': location_x,
            'Location Y': location_y,
            'Quality': quality,
            'Capacity': capacity
        })

    # Convert the list of dictionaries into a DataFrame
    df_schools = pd.DataFrame(school_data_rows)

    # Ensure that data directory exists
    data_directory = 'data/student_data'
    if not os.path.exists(data_directory):
        os.makedirs(data_directory)

    if save_as_csv:
        # Generate file names based on the mode
        if save_mode == 'new_each_run':
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            student_file_path = os.path.join(data_directory, f'student_information_{config_name}_{timestamp}.csv')
            school_file_path = os.path.join(data_directory, f'school_information_{config_name}_{timestamp}.csv')
        elif save_mode == 'new_on_first_iteration' and current_iteration == 1:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            student_file_path = os.path.join(data_directory, f'student_information_{config_name}_{timestamp}.csv')
            school_file_path = os.path.join(data_directory, f'school_information_{config_name}_{timestamp}.csv')
        elif save_mode == 'append':  # Default to appending
            student_file_path = os.path.join(data_directory, 'student_information.csv')
            school_file_path = os.path.join(data_directory, 'school_information.csv')
        else:
            raise ValueError("Invalid save_mode provided.")

        # Save the DataFrame to CSV (Students)
        df.to_csv(student_file_path, index=False, mode='a', header=not os.path.isfile(student_file_path))

        # Save the DataFrame to CSV (Schools)
        df_schools.to_csv(school_file_path, index=False, mode='a', header=not os.path.isfile(school_file_path))

    return df, df_schools  # Return the DataFrames for further manipulation if needed

