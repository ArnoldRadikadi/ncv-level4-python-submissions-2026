def amount_due(facility_code, hours):
    """Determine the hourly rate based on the facility code, 
    calculate the amount due before VAT, and return it."""
    code = facility_code.lower()
    rate = 0.0
    
    if code == "squa":
        rate = 13.00
    elif code == "swim":
        rate = 12.00
    elif code == "gym":
        rate = 11.00
    elif code == "wei":
        rate = 8.00
        
    return rate * hours


def final_amount_due(amount):
    """Receive the amount before VAT, add 14% VAT, 
    and return the final amount payable."""
    vat_rate = 0.14
    return amount * (1 + vat_rate)


def display(name, final_amount):
    """Display the customer's name and final amount payable 
    with the 'R' prefix and two decimal places."""
    print("\n--- PAYMENT SUMMARY ---")
    print(f"Customer Name: {name}")
    print(f"Final Amount Payable: R{final_amount:.2f}")


def process_payment():
    """Prompt user for inputs, coordinate function calls, 
    and manage the payment process flow."""
    name = input("Enter customer name: ")
    facility_code = input("Enter facility code (squa, swim, gym, wei): ")
    hours = float(input("Enter number of hours: "))
    
    
    base_amount = amount_due(facility_code, hours)
    
    
    total_payable = final_amount_due(base_amount)
    
    
    display(name, total_payable)



if __name__ == "__main__":
    process_payment()