import os
import csv
import pandas as pd

def save_to_csv(students, final_matches_true, final_matches_noisy, true_preferences, noisy_preferences, noisy_achievements, schools, iteration):
    # Create the data directory if it doesn't exist
    data_folder = 'data'
    os.makedirs(data_folder, exist_ok=True)

    # Save comprehensive student data
    with open(os.path.join(data_folder, 'student_information.csv'), 'a', newline='') as file:
        writer = csv.writer(file)
        if iteration == 1:  # Write header only once
            writer.writerow(['Iteration', 'Student ID', 'Location X', 'Location Y', 'Income', 'Achievement', 'Noisy Achievement',
                             'Matched School ID (True)', 'Rank in True Preferences (True)',
                             'Matched School ID (Noisy)', 'Rank in True Preferences (Noisy)',
                             'Rank Distance (Noisy - True)'])

        for student, noisy_achievement in zip(students, noisy_achievements):
            student_id = student.id
            location_x, location_y = student.location
            income = student.income
            achievement = student.achievement

            # Matched school and rank in true condition
            matched_school_true = final_matches_true.get(student_id)
            if matched_school_true is not None:
                rank_true = true_preferences[student_id].index(matched_school_true) + 1
            else:
                rank_true = None

            # Matched school and rank in noisy condition
            matched_school_noisy = final_matches_noisy.get(student_id)
            if matched_school_noisy is not None:
                rank_noisy = true_preferences[student_id].index(matched_school_noisy) + 1 if matched_school_noisy in true_preferences[student_id] else None
            else:
                rank_noisy = None

            # Calculate rank distance
            if rank_true is not None and rank_noisy is not None:
                rank_distance = rank_noisy - rank_true
            else:
                rank_distance = None

            # Write data to CSV
            writer.writerow([iteration, student_id, location_x, location_y, income, achievement, noisy_achievement,
                             matched_school_true, rank_true,
                             matched_school_noisy, rank_noisy,
                             rank_distance])

    # Save school data
    with open(os.path.join(data_folder, 'school_information.csv'), 'a', newline='') as file:
        writer = csv.writer(file)
        if iteration == 1:  # Write header only once
            writer.writerow(['Iteration', 'School ID', 'Location X', 'Location Y', 'Quality', 'Capacity'])

        for school in schools:
            school_id = school.id
            location_x, location_y = school.location
            quality = school.quality
            capacity = school.capacity

            # Write school data to CSV
            writer.writerow([iteration, school_id, location_x, location_y, quality, capacity])
