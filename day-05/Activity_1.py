class Product:
    VAT_RATE = 0.15

    def __init__(self, code, name, price):
        self.code = code
        self.name = name
        if price < 0:
            raise ValueError("Price cannot be negative.")
        self.price = price
        self._applied_discounts = []  

    def __str__(self):
        return f"{self.code} - {self.name}: R{self.price:.2f}"

    def calc_vat(self):
        return self.price * self.VAT_RATE

    def price_including_vat(self):
        return self.price + self.calc_vat()

    def apply_discount(self, percentage):
        discount = self.price * percentage / 100
        return self.price - discount

    
    def set_discount(self, percent):
        if percent < 0 or percent > 50:
            return False
        self._applied_discounts.append(percent)
        return True

    
    def get_applied_discounts(self):
        return self._applied_discounts[:]


def main():
    product1 = Product("P001", "Keyboard", 450.00)
    product2 = Product("P002", "Mouse", 250.00)

    print(product1)
    print(product2)
    print("VAT:", product1.calc_vat())
    print("Price including VAT:", product1.price_including_vat())
    print("Price after 10% discount:", product1.apply_discount(10))

    
    print("Test 1 (0% boundary):", product1.set_discount(0))      
    print("Test 2 (50% boundary):", product1.set_discount(50))    
    print("Test 3 (25% normal):", product1.set_discount(25))      
    print("Test 4 (-1% below min):", product1.set_discount(-1))    
    print("Test 5 (51% above max):", product1.set_discount(51))    

    print("Discounts log:", product1.get_applied_discounts())


main()