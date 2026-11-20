import random


def generate_minutes():
    """Return a random usage duration between 30 and 180 minutes (inclusive)."""
    return random.randint(30, 180)


def calc_amount(machine_type, minutes):
    """Calculate the amount before VAT using initial cost + hourly rate * hours."""
    machine = machine_type.strip().upper()
    hours_used = minutes / 60

    if machine == "A":
        initial_cost = 50.00
        hourly_rate = 30.00
    elif machine == "B":
        initial_cost = 62.50
        hourly_rate = 36.25
    elif machine == "C":
        initial_cost = 74.87
        hourly_rate = 40.50
    else:
        return 0.0

    return initial_cost + (hourly_rate * hours_used)


def calc_total_amount(amount):
    """Calculate 14% VAT and total payable; return (vat_amount, total_payable)."""
    vat_rate = 0.14
    vat_amount = amount * vat_rate
    total_payable = amount + vat_amount
    return vat_amount, total_payable


def display_summary(payments):
    """Display summary statistics from the list of total payments."""
    count = len(payments)

    print("\n===== DAILY PAYMENT SUMMARY =====")
    print(f"Customers processed : {count}")

    if count == 0:
        print("Combined total      : R0.00")
        print("Average payment     : R0.00")
        print("Highest payment     : R0.00")
        print("Lowest payment      : R0.00")
        return

    total_payable_all = 0.0
    highest_payment = payments[0]
    lowest_payment = payments[0]

    for payment in payments:
        total_payable_all = total_payable_all + payment
        if payment > highest_payment:
            highest_payment = payment
        if payment < lowest_payment:
            lowest_payment = payment

    average_payment = total_payable_all / count

    print(f"Combined total      : R{total_payable_all:.2f}")
    print(f"Average payment     : R{average_payment:.2f}")
    print(f"Highest payment     : R{highest_payment:.2f}")
    print(f"Lowest payment      : R{lowest_payment:.2f}")


def process_payments():
    """Prompt for customer data, process rentals, print invoices, and show summary."""
    num_customers = int(input("Enter number of customers to process: "))
    payments = []

    for customer_num in range(1, num_customers + 1):
        print(f"\n--- Customer {customer_num} ---")
        name = input("Enter customer name: ")
        machine_type = input("Enter machine type (A, B, or C): ")

        minutes = generate_minutes()
        amount_before_vat = calc_amount(machine_type, minutes)
        vat_amount, total_payable = calc_total_amount(amount_before_vat)

        payments.append(total_payable)

        print("\n----- CUSTOMER INVOICE -----")
        print(f"Customer Name   : {name}")
        print(f"Machine Type    : {machine_type.strip().upper()}")
        print(f"Minutes Used    : {minutes}")
        print(f"Amount (ex VAT) : R{amount_before_vat:.2f}")
        print(f"VAT (14%)       : R{vat_amount:.2f}")
        print(f"Total Payable   : R{total_payable:.2f}")

    display_summary(payments)


process_payments()