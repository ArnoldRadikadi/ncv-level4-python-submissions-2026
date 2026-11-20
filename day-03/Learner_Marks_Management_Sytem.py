
STARTER_LEARNERS = {
    "2024001": {"name": "Thandi", "marks": [65, 72, 58]},
    "2024002": {"name": "Sipho", "marks": [48, 90, 55]},
    "2024003": {"name": "Lerato", "marks": [81, 39, 77]},
    "2024004": {"name": "Dumisani", "marks": [72, 72, 48]},
    "2024005": {"name": "Naledi", "marks": [90, 55, 72]},
}


SAMPLE_DATA = [65, 72, 48, 90, 55, 72, 48, 72]



def question_1_collections(records):
    print("\n--- QUESTION 1: COLLECTIONS AND DATA STRUCTURES ---")

    
    marks_2024001 = records["2024001"]["marks"][:]  
    print("All marks for 2024001:", marks_2024001)
    print("First mark:", marks_2024001[0])
    print("Last mark:", marks_2024001[-1])
    print("First two marks:", marks_2024001[:2])

    
    classroom_seat = (3, 4)
    row, seat = classroom_seat
    print(f"Classroom coordinate -> Row: {row}, Seat: {seat}")
   

    
    module_codes = {"CS1", "CS2", "CS1", "CS3"}
    print("Unique module codes count:", len(module_codes))
    print("Is 'CS3' in module_codes?", "CS3" in module_codes)

   



def total_of(values):
    total = 0
    for v in values:
        total = total + v
    return total


def mean_of(values):
    if len(values) == 0:
        return None
    return total_of(values) / len(values)


def max_of(values):
    if len(values) == 0:
        return None
    best = values[0]
    for v in values:
        if v > best:
            best = v
    return best


def min_of(values):
    if len(values) == 0:
        return None
    smallest = values[0]
    for v in values:
        if v < smallest:
            smallest = v
    return smallest


def range_of(values):
    if len(values) == 0:
        return None
    return max_of(values) - min_of(values)


def above_mean(values):
    if len(values) == 0:
        return []
    avg = mean_of(values)
    result = []
    for v in values:
        if v > avg:
            result.append(v)
    return result


def question_2_aggregates(values):
    print("\n--- QUESTION 2: FIRST-PRINCIPLES LIST ALGORITHMS ---")
    print("Data:", values)
    print("Total:", total_of(values))
    print("Mean:", mean_of(values))
    print("Highest:", max_of(values))
    print("Lowest:", min_of(values))
    print("Range:", range_of(values))
    print("Values above mean:", above_mean(values))



def find_first(values, target):
    for i in range(len(values)):
        if values[i] == target:
            return i
    return -1


def find_all(values, target):
    positions = []
    for i in range(len(values)):
        if values[i] == target:
            positions.append(i)
    return positions


def count_of(values, target):
    count = 0
    for v in values:
        if v == target:
            count = count + 1
    return count


def mode_of(values):
    if len(values) == 0:
        return []
    counts = {}
    for v in values:
        if v in counts:
            counts[v] = counts[v] + 1
        else:
            counts[v] = 1

    best = 0
    for v in counts:
        if counts[v] > best:
            best = counts[v]

    modes = []
    for v in counts:
        if counts[v] == best:
            modes.append(v)
    return modes


def question_3_search_and_mode(values):
    print("\n--- QUESTION 3: SEARCH, DUPLICATES AND MODE ---")
    print("First index of 72:", find_first(values, 72))
    print("All indices of 72:", find_all(values, 72))
    print("Count of 72:", count_of(values, 72))
    print("Mode of data:", mode_of(values))
    tied_sample = [1, 2, 2, 3, 3]
    print("Tied modes on", tied_sample, "->", mode_of(tied_sample))



def bubble_sort(values):
    items = values[:]
    n = len(items)
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            if items[j] > items[j + 1]:
                items[j], items[j + 1] = items[j + 1], items[j]
                swapped = True
        if not swapped:
            break
    return items


def selection_sort(values):
    items = values[:]
    for i in range(len(items) - 1):
        smallest = i
        for j in range(i + 1, len(items)):
            if items[j] < items[smallest]:
                smallest = j
        items[i], items[smallest] = items[smallest], items[i]
    return items


def question_4_sorting(values):
    print("\n--- QUESTION 4: SORTING ALGORITHMS ---")
    print("Bubble sort (ascending):", bubble_sort(values))
    print("Selection sort (ascending):", selection_sort(values))
    print("Original list unchanged:", values)
    
def is_valid_number(text):
    return text.isdigit() and len(text) == 7


def is_valid_mark(text):
    return text.isdigit() and 0 <= int(text) <= 100


def add_learner(records, number, name, marks=None):
    if number in records:
        return False
    if marks is None:
        marks = []
    records[number] = {"name": name, "marks": marks}
    return True


def search_learner(records, number):
    if number not in records:
        return None
    return records[number]


def update_learner_name(records, number, new_name):
    if number not in records:
        return False
    records[number]["name"] = new_name
    return True


def add_learner_mark(records, number, mark):
    if number not in records:
        return False
    records[number]["marks"].append(mark)
    return True


def delete_learner(records, number):
    if number not in records:
        return False
    del records[number]
    return True


def rank_learners(records):
    rows = []
    for number in records:
        avg = mean_of(records[number]["marks"])
        if avg is not None:
            rows.append((avg, number))

    n = len(rows)
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            if rows[j][0] < rows[j + 1][0]:
                rows[j], rows[j + 1] = rows[j + 1], rows[j]
                swapped = True
        if not swapped:
            break
    return rows


def display_ranking(records):
    rows = rank_learners(records)
    if len(rows) == 0:
        print("No marks captured yet.")
        return
    print("\nRank  Number    Name          Average")
    for idx in range(len(rows)):
        avg, number = rows[idx]
        name = records[number]["name"]
        print(f"{idx + 1:<6}{number:<10}{name:<14}{avg:>6.1f}")


def show_menu():
    print("\nLEARNER MARKS MANAGEMENT SYSTEM ")
    print("1. Add learner")
    print("2. Search learner by student number")
    print("3. Update learner name")
    print("4. Add mark (0-100) to a learner")
    print("5. Delete a learner")
    print("6. Show ranking by average (highest will be first)")
    print("7. Run automated checks")
    print("8. Exit")



def run_check(label, actual, expected):
    status = "PASS" if actual == expected else "FAIL"
    print(f"[{status}] {label} -> Expected: {expected} | Actual: {actual}")


def question_6_tests(records, values):
    print("\n--- QUESTION 6: TESTING AND VERIFICATION ---")
    
    run_check("Sample total", total_of(values), 522)
    run_check("Sample mean", mean_of(values), 65.25)
    run_check("Sample max", max_of(values), 90)
    run_check("Sample min", min_of(values), 48)
    run_check("Sample find_first(72)", find_first(values, 72), 1)
    run_check("Sample find_all(72)", find_all(values, 72), [1, 5, 7])
    run_check("Sample count_of(72)", count_of(values, 72), 3)
    run_check("Sample ascending sort", bubble_sort(values), [48, 48, 55, 65, 72, 72, 72, 90])

    
    run_check("Empty list mean", mean_of([]), None)
    run_check("One mark mean", mean_of([70]), 70.0)
    run_check("Repeated marks mode", mode_of([50, 50, 50]), [50])
    run_check("Tied modes", mode_of([1, 2, 2, 3, 3]), [2, 3])
    run_check("Missing learner search", search_learner(records, "9999999"), None)
    run_check("Missing target index", find_first(values, 99), -1)


def main():
    
    learners = {}
    for num, info in STARTER_LEARNERS.items():
        learners[num] = {"name": info["name"], "marks": info["marks"][:]}

    choice = ""
    while choice != "8":
        show_menu()
        choice = input("Choose option (1-8): ").strip()

        if choice == "1":
            number = input("7-digit student number: ").strip()
            name = input("Learner name: ").strip()
            if not is_valid_number(number) or name == "":
                print("Invalid student number or name.")
                continue
            if number in learners:
                print("Duplicate student number rejected.")
                continue

            marks = []
            raw = input("Enter marks (0-100) separated by spaces, or press Enter: ").strip()
            if raw != "":
                valid = True
                for item in raw.split():
                    if is_valid_mark(item):
                        marks.append(int(item))
                    else:
                        print(f"Invalid mark '{item}'. Must be 0 to 100.")
                        valid = False
                        break
                if not valid:
                    continue

            add_learner(learners, number, name, marks)
            print("Learner added.")

        elif choice == "2":
            number = input("Student number to search: ").strip()
            rec = search_learner(learners, number)
            if rec is None:
                print("Learner not found.")
            else:
                print(f"Number: {number} | Name: {rec['name']} | Marks: {rec['marks']}")

        elif choice == "3":
            number = input("Student number to rename: ").strip()
            if number not in learners:
                print("Learner not found.")
                continue
            new_name = input("New learner name: ").strip()
            if new_name == "":
                print("Name cannot be empty.")
            elif update_learner_name(learners, number, new_name):
                print("Learner name updated.")

        elif choice == "4":
            number = input("Student number to add mark to: ").strip()
            if number not in learners:
                print("Learner not found.")
                continue
            mark_text = input("Mark (0-100): ").strip()
            if not is_valid_mark(mark_text):
                print("Invalid mark. Must be 0 to 100.")
            elif add_learner_mark(learners, number, int(mark_text)):
                print("Mark added.")

        elif choice == "5":
            number = input("Student number to delete: ").strip()
            if delete_learner(learners, number):
                print("Learner deleted.")
            else:
                print("Learner not found.")

        elif choice == "6":
            display_ranking(learners)

        elif choice == "7":
            question_1_collections(learners)
            question_2_aggregates(SAMPLE_DATA)
            question_3_search_and_mode(SAMPLE_DATA)
            question_4_sorting(SAMPLE_DATA)
            question_6_tests(learners, SAMPLE_DATA)

        elif choice == "8":
            print("Have a good day.")

        else:
            print("Invalid choice. Please enter a number from 1 to 8.")


if __name__ == "__main__":
    main()