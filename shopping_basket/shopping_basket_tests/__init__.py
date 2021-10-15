import unittest
from shopping_basket.basket_pricer import Catalogue


class CatalogueTests(unittest.TestCase):
    def test_catalogue_add(self):
        catalogue = Catalogue()

        catalogue.add("test", 5)
        self.assertEqual(catalogue.catalogue["test"], 5)

        catalogue.add("test", 6)
        self.assertEqual(catalogue.catalogue["test"], 6)

        catalogue.add("test", 6.5566778899)
        self.assertEqual(catalogue.catalogue["test"], 6.55)

        self.assertRaises(ValueError, catalogue.add("test", "asdf"))
        self.assertRaises(ValueError, catalogue.add("test", "£7"))
        self.assertRaises(ValueError, catalogue.add("test", "8"))

    @staticmethod
    def test_catalogue_remove():
        catalogue = Catalogue()
        catalogue.add("test", 5)
        catalogue.remove("test")
        catalogue.remove("test")
        catalogue.remove("asdf")
        catalogue.add("test", 5)
        catalogue.remove(0)

    def test_catalogue_generic(self):
        catalogue = Catalogue()
        self.assertRaises(KeyError, lambda: catalogue.catalogue["test"])


class OffersTests(unittest.TestCase):
    pass


class BasketTests(unittest.TestCase):
    pass


class BasketPricerTests(unittest.TestCase):
    pass
