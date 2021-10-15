import argparse
import unittest
from basket_pricer import Catalogue
from shopping_basket_tests import CatalogueTests, OffersTests, BasketTests, BasketPricerTests


def main():
    catalogue = Catalogue()


ap = argparse.ArgumentParser()

ap.add_argument("-t", "--test", required=False, default=False, help="Execute all unit tests")

args = vars(ap.parse_args())


if __name__ == '__main__':
    if args["test"]:
        unittest.main()
    else:
        main()
