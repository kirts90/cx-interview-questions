
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


class Offers:
    def __init__(self):
        pass

    def calculate_discount(self, basket):
        pass

    def buy_x_get_y_free(self, product, quantity, free_product, free_quantity):
        pass

    def percentage_discount(self, product, percentage_discount):
        pass


class Basket:
    def __init__(self, catalogue):
        self.catalogue = catalogue
        # Name of the product (unique ID) and quantity
        self.basket = dict()

    def add(self, name, quantity):
        pass

    def remove(self, name, quantity):
        pass
