import argparse
import unittest
from basket_pricer import Catalogue, Offers, Basket, BasketPricer
from shopping_basket_tests import CatalogueTests, OffersTests, BasketTests, BasketPricerTests


def main():
    catalogue = Catalogue()
    catalogue.add("Baked Beans", 0.99)
    catalogue.add("Biscuits", 1.20)
    catalogue.add("Sardines", 1.89)
    catalogue.add("Shampoo (Small)", 2.00)
    catalogue.add("Shampoo (Medium)", 2.50)
    catalogue.add("Shampoo (Large)", 3.50)

    offers = Offers()
    offers.add_offer(lambda user_basket: offers.percentage_discount("Sardines", 25, user_basket))
    offers.add_offer(lambda user_basket: offers.buy_x_get_y_free("Baked Beans", 2, "Baked Beans", 1, user_basket))

    basket = Basket(catalogue)
    basket.add("Baked Beans", 4)
    basket.add("Biscuits", 1)
    BasketPricer(catalogue, offers, basket)

    basket = Basket(catalogue)
    basket.add("Baked Beans", 2)
    basket.add("Biscuits", 1)
    basket.add("Sardines", 2)
    BasketPricer(catalogue, offers, basket)


ap = argparse.ArgumentParser()

ap.add_argument("-t", "--test", required=False, dest='test', action='store_true', default=False,
                help="Execute all unit tests")
args = vars(ap.parse_args())

if __name__ == '__main__':
    if args["test"]:
        unittest.main(argv=[''])
    else:
        main()
