import math


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
        self.offers = []

    @staticmethod
    def round_up(n, decimals=0):
        multiplier = 10 ** decimals
        return math.ceil(n * multiplier) / multiplier

    def calculate_discount(self, basket):
        total_discount = 0
        for i in range(len(self.offers)):
            offer = self.offers[i]
            total_discount += offer(basket)
        return total_discount

    @staticmethod
    def buy_x_get_y_free(product, buy_x, free_product, free_y, basket):
        if not isinstance(buy_x, int) or not isinstance(free_y, int):
            raise ValueError("quantity or free_quantity are not integers")
        if buy_x <= 0 or free_y <= 0:
            raise ValueError("Unexpected x or y values")

        if product in basket.basket and free_product in basket.basket:
            free_product_price = basket.catalogue.catalogue[free_product]
            buy_x_quantity = basket.basket[product]
            free_y_quantity = basket.basket[free_product]

            if product == free_product:
                free_quantity = 0
                for i in range(buy_x_quantity):
                    buy_x_quantity -= (buy_x + free_y)
                    if buy_x_quantity >= 0:
                        free_quantity += 1
                    else:
                        return free_quantity * free_product_price
            else:
                free_quantity = int(buy_x_quantity / buy_x)
                if free_quantity == free_y_quantity:
                    return free_quantity * free_product_price
                elif free_quantity > free_y_quantity:
                    return free_y_quantity * free_product_price
                elif free_quantity < free_y_quantity and free_y <= free_y_quantity:
                    return (free_quantity * free_y) * free_product_price
                elif free_quantity < free_y_quantity < free_y:
                    return free_y_quantity * free_product_price
        return 0

    def percentage_discount(self, product, percentage_discount, basket):
        if not isinstance(percentage_discount, int) or percentage_discount <= 0:
            raise ValueError("percentage_discount value is equal or less to 0 or not an integer")
        if product in basket.basket:
            price = basket.catalogue.catalogue[product]
            quantity = basket.basket[product]
            total = price * quantity
            return self.round_up((total * percentage_discount) / 100, 2)
        return 0

    def add_offer(self, offer_lambda):
        self.offers.append(offer_lambda)


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
        self.discount = self.calculate_discount()
        self.total = self.calculate_total()
        self.currency = "£"

    def calculate_subtotal(self):
        subtotal = 0
        for key, value in self.basket.basket.items():
            subtotal += self.catalogue[key] * value
        return round(subtotal, 2)

    def calculate_discount(self):
        return self.offers.calculate_discount(self.basket)

    def calculate_total(self):
        if self.subtotal >= self.discount:
            return round(self.subtotal - self.discount, 2)
        else:
            return 0

    def __del__(self):
        print("---")
        print("subtotal:", self.currency + str(self.subtotal))
        print("discount:", self.currency + str(self.discount))
        print("total:", self.currency + str(self.total))
