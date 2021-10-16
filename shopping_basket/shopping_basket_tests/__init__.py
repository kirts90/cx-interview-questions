import unittest
from shopping_basket.basket_pricer import Catalogue


class CatalogueTests(unittest.TestCase):
    def test_catalogue_add(self):
        # Assumptions:
        # We assume negative prices are accepted
        # Rounding up/down is being done to the closest
        # Add can behave like an update function
        # Invalid values will raise ValueError and thus, not accepted
        catalogue = Catalogue()

        catalogue.add("test", 5)
        self.assertEqual(catalogue.catalogue["test"], 5)

        catalogue.add("test", 6)
        self.assertEqual(catalogue.catalogue["test"], 6)

        catalogue.add("test", 6.5566778899)
        self.assertEqual(catalogue.catalogue["test"], 6.56)

        catalogue.add("test", 6.5546778899)
        self.assertEqual(catalogue.catalogue["test"], 6.55)

        catalogue.add("test", 6.5555555)
        self.assertEqual(catalogue.catalogue["test"], 6.56)

        catalogue.add("test", 6.5)
        self.assertEqual(catalogue.catalogue["test"], 6.5)

        catalogue.add("test", -5)
        self.assertEqual(catalogue.catalogue["test"], -5)

        self.assertRaises(ValueError, catalogue.add, "test", "asdf")
        self.assertRaises(ValueError, catalogue.add, "test", "£7")
        self.assertRaises(ValueError, catalogue.add, "test", "8")

    @staticmethod
    def test_catalogue_remove():
        # Assumptions:
        # If key is wrong then do nothing (we could've raised an exception instead)
        catalogue = Catalogue()
        catalogue.add("test", 5)
        catalogue.remove("test")
        catalogue.remove("test")
        catalogue.remove("asdf")
        catalogue.add("test", 5)
        catalogue.remove(0)

    def test_catalogue_generic(self):
        # Assumptions:
        # Invalid usage/access, will default to KeyError exception
        # We want to limit unexpected behaviour/usage but there is a diminishing returns to the value added vs dev time
        catalogue = Catalogue()
        self.assertRaises(KeyError, lambda: catalogue.catalogue["test"])


class OffersTests(unittest.TestCase):
    pass


class BasketTests(unittest.TestCase):
    pass


class BasketPricerTests(unittest.TestCase):
    pass
