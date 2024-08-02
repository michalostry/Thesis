import csv
import pandas as pd

def save_to_csv(students, schools, final_matches_true, final_matches_noisy, true_preferences, noisy_preferences):
    # Save Students data
    with open('students.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Student ID', 'Location X', 'Location Y', 'Income', 'Achievement'])
        for student in students:
            writer.writerow([student.id, student.location[0], student.location[1], student.income, student.achievement])

    # Save Schools data
    with open('schools.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['School ID', 'Location X', 'Location Y', 'Quality', 'Capacity'])
        for school in schools:
            writer.writerow([school.id, school.location[0], school.location[1], school.quality, school.capacity])

    # Save Preferences data
    preferences_data = []
    for student_id, prefs in enumerate(true_preferences):
        for rank, school_id in enumerate(prefs):
            preferences_data.append([student_id, school_id, 'true', rank + 1])
    for student_id, prefs in enumerate(noisy_preferences):
        for rank, school_id in enumerate(prefs):
            preferences_data.append([student_id, school_id, 'noisy', rank + 1])
    preferences_df = pd.DataFrame(preferences_data, columns=['Student ID', 'School ID', 'Condition', 'Preference Rank'])
    preferences_df.to_csv('preferences.csv', index=False)

    # Save Matches data
    matches_data = []
    for student_id, school_id in final_matches_true.items():
        matches_data.append([student_id, school_id, 'true'])
    for student_id, school_id in final_matches_noisy.items():
        matches_data.append([student_id, school_id, 'noisy'])
    matches_df = pd.DataFrame(matches_data, columns=['Student ID', 'School ID', 'Condition'])
    matches_df.to_csv('matches.csv', index=False)
