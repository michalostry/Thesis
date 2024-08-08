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


def compute_average_rank_distance(final_matches_noisy, final_matches_true, true_preferences, noisy_preferences):
    total_distance = 0
    count = 0  # To count students with matches in both conditions

    # Ensure all calculations are done within the same loop
    for student_id, noisy_match in final_matches_noisy.items():
        matched_school_true = final_matches_true.get(student_id)

        # Only consider students matched under both conditions
        if noisy_match is not None and matched_school_true is not None:
            # Calculate rank in the true preferences
            true_rank = true_preferences[student_id].index(noisy_match) if noisy_match in true_preferences[student_id] else len(true_preferences[student_id])
            # Calculate rank in the noisy preferences
            noisy_rank = noisy_preferences[student_id].index(noisy_match)
            # Calculate the distance (noisy - true)
            distance = noisy_rank - true_rank
            total_distance += distance
            count += 1

            # Print for debugging purposes
            print(f"Student {student_id}: True School = {matched_school_true}, Noisy School = {noisy_match}, True Rank = {true_rank + 1}, Noisy Rank = {noisy_rank + 1}, Distance = {distance}")

    # Calculate the average distance
    average_distance = total_distance / count if count > 0 else 0
    print(f"\nFinal Average Rank Distance (Noisy - True): {average_distance:.2f}")
    return average_distance





