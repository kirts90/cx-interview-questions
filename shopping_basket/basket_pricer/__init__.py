
class Catalogue:
    def __init__(self):
        self.catalogue = dict()
        # Name of the product (unique ID) and price
        self.catalogue["Baked Beans"] = 0.99
        self.catalogue["Biscuits"] = 1.20
        self.catalogue["Sardines"] = 1.89
        self.catalogue["Shampoo (Small)"] = 2.00
        self.catalogue["Shampoo (Medium)"] = 2.50
        self.catalogue["Shampoo (Large)"] = 3.50

    def add(self, product_name, price):
        self.catalogue[product_name] = price

    def remove(self, product_name):
        if product_name in self.catalogue:
            del self.catalogue[product_name]
