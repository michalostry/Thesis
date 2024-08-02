import matplotlib.pyplot as plt
import numpy as np


def visualize_initial_locations(students, schools, grid_size):
    plt.figure(figsize=(10, 10))
    plt.scatter([student.location[0] for student in students],
                [student.location[1] for student in students], c='blue', label='Students', alpha=0.5)
    plt.scatter([school.location[0] for school in schools],
                [school.location[1] for school in schools], c='red', label='Schools', marker='x')
    plt.xlim(0, grid_size)
    plt.ylim(0, grid_size)
    plt.title("Initial Student and School Locations")
    plt.legend()
    plt.show()


def plot_noisy_vs_true_achievements(students, noisy_achievements):
    true_achievements = [student.achievement for student in students]

    plt.figure(figsize=(8, 6))
    plt.scatter(true_achievements, noisy_achievements, c='blue', alpha=0.5)
    plt.plot([0, 100], [0, 100], 'r--')
    plt.xlabel("True Achievement")
    plt.ylabel("Noisy Achievement")
    plt.title("Noisy vs. True Achievements")
    plt.xlim(0, 100)
    plt.ylim(0, 100)
    plt.show()

def visualize_final_matches(final_matches_noisy, final_matches_true, schools):
    school_ids = [school.id for school in schools]
    num_students_noisy = [list(final_matches_noisy.values()).count(school_id) for school_id in school_ids]
    num_students_true = [list(final_matches_true.values()).count(school_id) for school_id in school_ids]

    x = np.arange(len(school_ids))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width / 2, num_students_noisy, width, label='Noisy')
    rects2 = ax.bar(x + width / 2, num_students_true, width, label='True')

    # Add some text for labels, title, and custom x-axis tick labels, etc.
    ax.set_xlabel('School ID')
    ax.set_ylabel('Number of Matched Students')
    ax.set_title('Number of Matched Students per School (Noisy vs True Achievement)')
    ax.set_xticks(x)
    ax.set_xticklabels(school_ids)
    ax.legend()

    fig.tight_layout()

    plt.show()

def visualize_difference_in_matches(final_matches_noisy, final_matches_true):
    same_match_count = sum(final_matches_noisy[student_id] == final_matches_true[student_id] for student_id in final_matches_noisy)
    different_match_count = len(final_matches_noisy) - same_match_count

    labels = ['Same Match', 'Different Match']
    counts = [same_match_count, different_match_count]

    plt.figure(figsize=(8, 6))
    plt.bar(labels, counts, color=['green', 'orange'])
    plt.ylabel('Number of Students')
    plt.title('Comparison of Matches: True vs Noisy Achievement')
    plt.show()

def visualize_utilities(students, schools, utilities):
    plt.figure(figsize=(10, 6))
    for student_id, student_utilities in utilities.items():
        plt.plot(range(len(schools)), student_utilities, label=f'Student {student_id}')
    plt.xlabel('School ID')
    plt.ylabel('Utility')
    plt.title('Utility Distribution Across Schools for Sample Students')
    plt.legend()
    plt.show()
