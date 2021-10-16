
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
        if product_name not in self.catalogue:
            raise ValueError("Product name provided is not found in the catalogue")
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

    def add(self, product_name, quantity):
        if product_name not in self.catalogue.catalogue:
            raise ValueError("Product provided not found in the catalogue")
        if isinstance(quantity, int):
            if quantity > 0:
                self.basket[product_name] = quantity
            else:
                self.remove(product_name)
        else:
            raise ValueError("Value provided is not an integer")

    def remove(self, product_name):
        if product_name not in self.catalogue.catalogue or product_name not in self.basket:
            raise ValueError("Product not found in catalogue or basket")
        del self.basket[product_name]


class BasketPricer:
    def __init__(self, catalogue, offers, basket):
        self.catalogue = catalogue.catalogue
        self.offers = offers
        self.basket = basket

        self.subtotal = self.calculate_subtotal()
        self.discount = 0
        self.total = self.calculate_total()
        self.currency = "£"

    def calculate_subtotal(self):
        subtotal = 0
        for key, value in self.basket.basket.items():
            subtotal += self.catalogue[key] * value
        return round(subtotal, 2)

    def calculate_discount(self):
        pass

    def calculate_total(self):
        if self.subtotal >= self.discount:
            return round(self.subtotal - self.discount, 2)
        else:
            return 0

    def __del__(self):
        print("subtotal:", self.currency + str(self.subtotal))
        print("discount:", self.currency + str(self.discount))
        print("total:", self.currency + str(self.total))
