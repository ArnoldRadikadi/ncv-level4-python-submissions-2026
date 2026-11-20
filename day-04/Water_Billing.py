
INPUT_FILE = "water_readings.txt"
REPORT_FILE = "billing_report.txt"
ERROR_LOG_FILE = "errors.log"


def read_lines(filename):
    """Reads non-blank stripped lines from a file; raises FileNotFoundError if missing."""
    lines = []
    with open(filename, "r") as f:
        for raw_line in f:
            cleaned = raw_line.strip()
            if cleaned != "":
                lines.append(cleaned)
    return lines



def is_non_negative_int(text):
    """Checks if text represents a non-negative integer without crashing on int()."""
    if text == "":
        return False
    return text.isdigit()


def validate_and_parse_line(text):
    """
    Validates a single record line: MeterNumber,HouseholdName,PreviousReading,CurrentReading,Area
    Returns (True, record_dict, "") if valid, or (False, None, reason) if invalid.
    """
    parts = text.split(",")
    if len(parts) != 5:
        return False, None, f"Expected 5 fields, got {len(parts)}"

    meter_no = parts[0].strip()
    household_name = parts[1].strip()
    prev_text = parts[2].strip()
    curr_text = parts[3].strip()
    area = parts[4].strip()

    if meter_no == "":
        return False, None, "Missing meter number"
    if household_name == "":
        return False, None, "Missing household name"
    if area == "":
        return False, None, "Missing area"

    if not is_non_negative_int(prev_text) or not is_non_negative_int(curr_text):
        return False, None, "Non-numeric or negative meter reading"

    prev_reading = int(prev_text)
    curr_reading = int(curr_text)

    if curr_reading < prev_reading:
        return (
            False,
            None,
            f"Current reading ({curr_reading}) below previous reading ({prev_reading})",
        )

    record = {
        "meter": meter_no,
        "name": household_name,
        "prev": prev_reading,
        "curr": curr_reading,
        "area": area,
    }
    return True, record, ""


def load_water_records(filename):
    """
    Loads valid household records into a dictionary keyed by MeterNumber,
    rejecting missing fields, duplicates, non-numeric/negative readings,
    and reversed readings. Returns (records_dict, error_entries_list).
    """
    raw_lines = read_lines(filename)
    records = {}
    errors = []

    line_number = 0
    for text in raw_lines:
        line_number = line_number + 1
        is_valid, rec, reason = validate_and_parse_line(text)

        if not is_valid:
            errors.append(f"Line {line_number}: {reason} | Raw: {text}")
            continue

        meter_no = rec["meter"]
        if meter_no in records:
            errors.append(f"Line {line_number}: Duplicate meter number '{meter_no}' | Raw: {text}")
            continue

        records[meter_no] = rec

    return records, errors



def calculate_consumption(prev_reading, curr_reading):
    """Returns monthly water usage in kilolitres (kL)."""
    return curr_reading - prev_reading


def calculate_progressive_bill(consumption_kl):
    """
    Calculates progressive tariff:
    - First 6 kL: Free (R0.00)
    - Next 14 kL (above 6 up to 20 kL): R8.50 per kL
    - Above 20 kL: R12.00 per additional kL
    """
    if consumption_kl <= 6:
        charge = 0.0
    elif consumption_kl <= 20:
        charge = (consumption_kl - 6) * 8.50
    else:
        band_2_kl = 14
        band_3_kl = consumption_kl - 20
        charge = (band_2_kl * 8.50) + (band_3_kl * 12.00)
    return round(charge, 2)


def classify_consumption(consumption_kl):
    """Classifies kL usage as LOW (0-20), MODERATE (>20 to 50), or HIGH (>50)."""
    if consumption_kl <= 20:
        return "LOW"
    elif consumption_kl <= 50:
        return "MODERATE"
    else:
        return "HIGH"


def enrich_records(records):
    """Adds consumption_kl, bill_amount, and category to each valid record."""
    for meter_no in records:
        rec = records[meter_no]
        kl = calculate_consumption(rec["prev"], rec["curr"])
        bill = calculate_progressive_bill(kl)
        band = classify_consumption(kl)
        rec["consumption"] = kl
        rec["bill"] = bill
        rec["band"] = band



def rank_top_consumers(records, top_n=5):
    """
    Manually sorts households by consumption (descending) using a loop swap
    without sorted(), max(), min(), or sum(). Returns the top N entries.
    """
    ranked = []
    for meter_no in records:
        rec = records[meter_no]
        ranked.append(
            {
                "meter": meter_no,
                "name": rec["name"],
                "area": rec["area"],
                "consumption": rec["consumption"],
                "bill": rec["bill"],
                "band": rec["band"],
            }
        )

    count = len(ranked)
    for i in range(count - 1):
        swapped = False
        for j in range(count - 1 - i):
            if ranked[j]["consumption"] < ranked[j + 1]["consumption"]:
                ranked[j], ranked[j + 1] = ranked[j + 1], ranked[j]
                swapped = True
        if not swapped:
            break

    top_list = []
    limit = top_n if top_n < len(ranked) else len(ranked)
    for idx in range(limit):
        top_list.append(ranked[idx])

    return top_list


def build_report_lines(records, top_five, accepted_count, rejected_count):
    """Builds formatted lines for billing_report.txt using loop accumulation."""
    total_kl = 0
    total_revenue = 0.0
    low_count = 0
    moderate_count = 0
    high_count = 0

    for meter_no in records:
        rec = records[meter_no]
        total_kl = total_kl + rec["consumption"]
        total_revenue = total_revenue + rec["bill"]
        if rec["band"] == "LOW":
            low_count = low_count + 1
        elif rec["band"] == "MODERATE":
            moderate_count = moderate_count + 1
        else:
            high_count = high_count + 1

    lines = []
    lines.append("COMMUNITY WATER CONSUMPTION AND BILLING REPORT")
    lines.append("=" * 78)
    lines.append(f"Accepted Records : {accepted_count}")
    lines.append(f"Rejected Records : {rejected_count}")
    lines.append(f"Total Consumption: {total_kl} kL")
    lines.append(f"Total Billed     : R{total_revenue:.2f}")
    lines.append(f"Bands            : LOW={low_count}, MODERATE={moderate_count}, HIGH={high_count}")
    lines.append("")
    lines.append("HOUSEHOLD BILLING DETAILS")
    lines.append("-" * 78)
    lines.append(f"{'Meter':<8}{'Household Name':<22}{'Area':<18}{'kL':>6}{'Bill (R)':>12}{'Band':<10}")
    lines.append("-" * 78)

    for meter_no in records:
        rec = records[meter_no]
        lines.append(
            f"{rec['meter']:<8}"
            f"{rec['name']:<22}"
            f"{rec['area']:<18}"
            f"{rec['consumption']:>6}"
            f"{rec['bill']:>12.2f}"
            f"{'  ' + rec['band']:<10}"
        )

    lines.append("")
    lines.append("TOP FIVE HIGHEST-CONSUMING HOUSEHOLDS")
    lines.append("-" * 78)
    rank_pos = 1
    for entry in top_five:
        lines.append(
            f"{rank_pos}. {entry['meter']} - {entry['name']} ({entry['area']}): "
            f"{entry['consumption']} kL | Bill: R{entry['bill']:.2f} | {entry['band']}"
        )
        rank_pos = rank_pos + 1

    return lines


def write_text_lines(filename, lines):
    """Writes a list of text lines to filename."""
    with open(filename, "w") as f:
        for line in lines:
            f.write(line + "\n")



def main():
    try:
        records, errors = load_water_records(INPUT_FILE)
    except FileNotFoundError:
        print(f"Error: '{INPUT_FILE}' was not found in the current working folder.")
        return

    enrich_records(records)
    top_five = rank_top_consumers(records, 5)

    accepted_count = len(records)
    rejected_count = len(errors)

    report_lines = build_report_lines(records, top_five, accepted_count, rejected_count)
    write_text_lines(REPORT_FILE, report_lines)
    write_text_lines(ERROR_LOG_FILE, errors)

    print("Processing complete.")
    print(f"Accepted records: {accepted_count}")
    print(f"Rejected records: {rejected_count}")
    print(f"Report written to : {REPORT_FILE}")
    print(f"Error log written : {ERROR_LOG_FILE}")


if __name__ == "__main__":
    main()