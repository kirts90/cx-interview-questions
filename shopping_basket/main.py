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

    basket = Basket(catalogue)
    basket.add("Baked Beans", 4)
    basket.add("Biscuits", 1)

    BasketPricer(catalogue, offers, basket)


ap = argparse.ArgumentParser()

ap.add_argument("-t", "--test", required=False, default=True, help="Execute all unit tests")

args = vars(ap.parse_args())


if __name__ == '__main__':
    if args["test"]:
        unittest.main()
    else:
        main()
