# Exercise: race qualifiers (6 km fun run)
# Rules: loops and if statements only; no min(), sorted(), or sum().

QUALIFYING_LIMIT_SECONDS = 25 * 60  # 25:00 = 1500 seconds

names = []
times_str = []
times_sec = []

entry = input("Enter athlete name and mm:ss time (or x to finish): ").strip()

while entry.lower() != "x":
    parts = entry.split()

    # Expecting "<name> <mm:ss>" (handling single-word names cleanly)
    if len(parts) < 2:
        print("Invalid entry ignored.")
    else:
        time_part = parts[-1]
        name_part = " ".join(parts[:-1]).strip()

        if name_part == "" or ":" not in time_part:
            print("Invalid time ignored.")
        else:
            time_pieces = time_part.split(":")
            if len(time_pieces) != 2:
                print("Invalid time ignored.")
            else:
                mm_str, ss_str = time_pieces[0], time_pieces[1]

                # Validate digits BEFORE calling int() to avoid ValueError
                if len(mm_str) > 0 and len(ss_str) == 2 and mm_str.isdigit() and ss_str.isdigit():
                    minutes = int(mm_str)
                    seconds = int(ss_str)

                    if minutes >= 0 and 0 <= seconds <= 59:
                        total_seconds = minutes * 60 + seconds
                        names.append(name_part)
                        times_str.append(time_part)
                        times_sec.append(total_seconds)
                    else:
                        print("Invalid time ignored.")
                else:
                    print("Invalid time ignored.")

    entry = input("Enter athlete name and mm:ss time (or x to finish): ").strip()

# Handle empty / no valid entries
if len(times_sec) == 0:
    print("No valid athletes entered.")
    print("Qualified: 0 of 0")
else:
    # First-principles count of qualifiers (25:00 or less)
    qualified_count = 0
    for t in times_sec:
        if t <= QUALIFYING_LIMIT_SECONDS:
            qualified_count = qualified_count + 1

    # First-principles lowest time (strict < keeps the first athlete on a tie)
    best_index = 0
    for i in range(1, len(times_sec)):
        if times_sec[i] < times_sec[best_index]:
            best_index = i

    print(f"Winner: {names[best_index]} ({times_str[best_index]})")
    print(f"Qualified: {qualified_count} of {len(times_sec)}")