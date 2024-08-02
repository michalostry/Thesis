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

def compute_average_rank_distance(final_matches_noisy, true_preferences, noisy_preferences, num_students):
    total_distance = 0
    for student_id, noisy_match in final_matches_noisy.items():
        if noisy_match is not None:
            true_rank = true_preferences[student_id].index(noisy_match) if noisy_match in true_preferences[student_id] else len(true_preferences[student_id])
            noisy_rank = noisy_preferences[student_id].index(noisy_match)
            total_distance += abs(noisy_rank - true_rank)
    average_distance = total_distance / num_students
    return average_distance
