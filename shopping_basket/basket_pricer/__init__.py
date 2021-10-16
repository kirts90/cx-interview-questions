
class Catalogue:
    def __init__(self):
        # Name of the product (unique ID) and price
        self.catalogue = dict()

    def add(self, product_name, price):
        if isinstance(price, float) or isinstance(price, int):
            self.catalogue[product_name] = round(price, 2)
        else:
            raise ValueError("Value provided is not a float or integer")

    def remove(self, product_name):
        if product_name in self.catalogue:
            del self.catalogue[product_name]
