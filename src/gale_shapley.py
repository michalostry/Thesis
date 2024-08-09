print_info = 1 #1 - yes, 0 - no
from collections import defaultdict

def deferred_acceptance(student_preferences_dict, school_preferences_dict, schools_capacity, no_change_limit=100):
    if print_info == 1:
        # Print initial preferences of students
        print("\nInitial Student Preferences:")
        for student_id, preferences in student_preferences_dict.items():
            print(f"Student {student_id}: {preferences}")

        #Print initial preferences of schools
        print("\nInitial School Preferences:")
        for school_id, preferences in school_preferences_dict.items():
           print(f"School {school_id}: {preferences}")

        #Print initial capacities of schools
        print("\nInitial School Capacities:")
        for school_id, capacity in schools_capacity.items():
            print(f"School {school_id} Capacity: {capacity}")

    unmatched_students = set(student_preferences_dict.keys())
    school_slots = {school_id: capacity for school_id, capacity in schools_capacity.items()}
    school_proposals = defaultdict(list)

    # Initial empty matches
    matches = {student_id: None for student_id in student_preferences_dict}

    round_number = 0  # To track the round number
    no_change_rounds = 0  # To track consecutive rounds with no changes

    while unmatched_students and no_change_rounds < no_change_limit:
        round_number += 1
        new_unmatched_students = set()
        changes = False  # Assume no changes happen until we find otherwise

        if print_info == 1:
            print(f"\n--- Round {round_number} ---")
            print("Unmatched students:", unmatched_students)

        for student_id in unmatched_students:
            if student_preferences_dict[student_id]:  # Student still has schools to apply to
                top_choice = student_preferences_dict[student_id].pop(0)
                school_proposals[top_choice].append(student_id)
                if print_info == 1: print(f"Student {student_id} proposes to School {top_choice}")

        if print_info == 1: print("\nProposals received by schools:")
        for school_id, proposed_students in school_proposals.items():
            # print(f"School {school_id} received proposals from students: {proposed_students}")
            proposed_students.sort(key=lambda student_id: school_preferences_dict[school_id].index(student_id))

            # Combine previously accepted students and new proposals
            current_accepted_students = [student_id for student_id, match_school in matches.items() if match_school == school_id]
            all_candidates = current_accepted_students + proposed_students
            all_candidates.sort(key=lambda student_id: school_preferences_dict[school_id].index(student_id))

            # Select the top students up to the school's capacity
            newly_accepted_students = []
            accepted_students = all_candidates[:schools_capacity[school_id]]
            rejected_students = set(all_candidates[schools_capacity[school_id]:])

            # Differentiate between newly rejected and previously accepted but now rejected students
            newly_rejected_students = [student_id for student_id in proposed_students if student_id in rejected_students]
            previously_accepted_but_rejected_students = [student_id for student_id in current_accepted_students if student_id in rejected_students]

            # Update matches and school slots
            for student_id in accepted_students:
                if matches[student_id] != school_id:
                    matches[student_id] = school_id
                    newly_accepted_students.append(student_id)
                    changes = True  # A change was made in this round
            for student_id in rejected_students:
                if matches[student_id] is not None:
                    changes = True  # A change was made in this round
                matches[student_id] = None
                new_unmatched_students.add(student_id)

            if print_info == 1:
                #Print only newly accepted students for each school
                if newly_accepted_students:
                   print(f"School {school_id} newly accepts students: {newly_accepted_students}")
                if newly_rejected_students:
                   print(f"School {school_id} rejects new proposals: {newly_rejected_students}")
                if previously_accepted_but_rejected_students:
                   print(f"School {school_id} rejects previously accepted students: {previously_accepted_but_rejected_students}")

        unmatched_students = new_unmatched_students
        school_proposals.clear()

        if print_info == 1:
            print("\nCurrent matches set:")
            print(matches)

        if changes:
            no_change_rounds = 0  # Reset counter if changes occurred
        else:
            no_change_rounds += 1  # Increment counter if no changes occurred

    if no_change_rounds >= no_change_limit:
        print(f"\nNo new matches were created for {no_change_limit} consecutive rounds. Stopping the algorithm.")

    return matches
