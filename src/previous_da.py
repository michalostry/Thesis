# Updated Students' preferences with 4 schools
students_preferences = {
    "Student_1": ["School_A", "School_B", "School_C", "School_D"],
    "Student_2": ["School_A", "School_C", "School_D", "School_B"],
    "Student_3": ["School_C", "School_D", "School_A", "School_B"],
    "Student_4": ["School_A", "School_D", "School_B", "School_C"],
    "Student_5": ["School_A", "School_B", "School_C", "School_D"],
    "Student_6": ["School_B", "School_C", "School_D", "School_A"],
    "Student_7": ["School_C", "School_D", "School_A", "School_B"],
    "Student_8": ["School_D", "School_A", "School_B", "School_C"],
    "Student_9": ["School_A", "School_B", "School_C", "School_D"],
    "Student_10": ["School_B", "School_C", "School_D", "School_A"]
}

# Updated Schools' preferences with 4 schools
schools_preferences = {
    "School_A": ["Student_1", "Student_2", "Student_3", "Student_4", "Student_5", "Student_6", "Student_7", "Student_8", "Student_9", "Student_10"],
    "School_B": ["Student_1", "Student_2", "Student_3", "Student_4", "Student_5", "Student_6", "Student_7", "Student_8", "Student_9", "Student_10"],
    "School_C": ["Student_1", "Student_2", "Student_3", "Student_4", "Student_5", "Student_6", "Student_7", "Student_8", "Student_9", "Student_10"],
    "School_D": ["Student_1", "Student_2", "Student_3", "Student_4", "Student_5", "Student_6", "Student_7", "Student_8", "Student_9", "Student_10"]
}



def deferred_acceptance_with_reassessment(students_preferences, schools_preferences, schools_capacity, max_iterations=5000, convergence_threshold=5):
    # Initialize matches for students and proposals for schools
    matches = {student: None for student in students_preferences}
    proposals = {school: [] for school in schools_preferences}
    rejections = {school: [] for school in schools_preferences}  # New data structure to track rejections
    proposed_this_round = {school: [] for school in schools_preferences}  # Track students who proposed to schools in this round

    iteration = 0
    consecutive_stable_iterations = 0  # Counter to track consecutive iterations with no changes
    while iteration < max_iterations:
        print(f"Iteration {iteration}:")
        new_proposals_made = False

        # Proposal Phase
        print("  Proposal Phase:")
        for student, preferences in list(students_preferences.items()):
            if matches[student] is None and preferences:
                top_choice = preferences[0]
                if student not in proposed_this_round[top_choice] and student not in rejections[top_choice]:  # Check for previous rejections
                    proposals[top_choice].append(student)
                    proposed_this_round[top_choice].append(student)
                    new_proposals_made = True
                    print(f"    {student} proposes to {top_choice}")

        # Acceptance and Reassessment Phase
        print("  Acceptance and Reassessment Phase:")
        for school, school_prefs in schools_preferences.items():
            if proposals[school]:
                all_candidates = proposals[school] + [s for s, m_school in matches.items() if m_school == school]
                all_candidates.sort(key=lambda x: school_prefs.index(x))

                accepted_students = all_candidates[:schools_capacity[school]]
                for student in accepted_students:
                    matches[student] = school
                    print(f"    {school} tentatively accepts {student}")

                for student in all_candidates[schools_capacity[school]:]:
                    if matches[student] == school:
                        matches[student] = None
                        rejections[school].append(student)
                        print(f"    {school} rejects {student}")
                        if student in proposed_this_round[school]:
                            proposals[school].remove(student)

                proposals[school] = []
                proposed_this_round[school] = []

        for student, preferences in list(students_preferences.items()):
            if matches[student] is None and preferences:
                top_choice = preferences[0]
                if student not in proposals[top_choice] and student not in rejections[top_choice]:  # Check for previous rejections
                    rejections[top_choice].append(student)

        proposals = {school: [] for school in schools_preferences}
        proposed_this_round = {school: [] for school in schools_preferences}

        print("  Current Matches:", matches)
        print("  Rejections:", rejections)

        # Update student preferences based on rejections
        for school, rejected_students in rejections.items():
            for student in rejected_students:
                if student in students_preferences and school in students_preferences[student]:
                    students_preferences[student].remove(school)

        # Check for convergence
        if not new_proposals_made:
            consecutive_stable_iterations += 1
            if consecutive_stable_iterations >= convergence_threshold or iteration >= 50:
                break  # Exit the loop if no changes for several consecutive iterations or iteration exceeds 50
        else:
            consecutive_stable_iterations = 0  # Reset counter if there are new proposals

        iteration += 1

    return matches, rejections




# Define school capacities
capacity = 1
schools_capacity = {
    "School_A": capacity,  # Replace with the desired capacity for School_X
    "School_B": capacity,
    "School_C": capacity,  # Replace with the desired capacity for School_Y
    "School_D": capacity   # Replace with the desired capacity for School_Z
}

# Run the Deferred Acceptance algorithm with reassessment
final_matches, rejections = deferred_acceptance_with_reassessment(students_preferences, schools_preferences, schools_capacity)
print("\nFinal Matches:", final_matches)
print("Rejections:", rejections)
