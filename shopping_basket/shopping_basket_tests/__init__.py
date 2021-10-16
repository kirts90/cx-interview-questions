import unittest
from shopping_basket.basket_pricer import Catalogue, Offers, Basket, BasketPricer


class CatalogueTests(unittest.TestCase):
    def test_add(self):
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

        self.assertRaises(ValueError, catalogue.add, "test", "Lorem ipsum")
        self.assertRaises(ValueError, catalogue.add, "test", "£7")
        self.assertRaises(ValueError, catalogue.add, "test", "8")

    def test_remove(self):
        # Assumptions:
        # If key is wrong then raise ValueError exception
        # Invalid access, will default to KeyError exception
        catalogue = Catalogue()
        catalogue.add("test", 5)
        self.assertEqual(catalogue.catalogue["test"], 5)
        catalogue.remove("test")
        self.assertRaises(KeyError, lambda: catalogue.catalogue["test"])
        self.assertRaises(ValueError, catalogue.remove, "test")
        self.assertRaises(ValueError, catalogue.remove, "Lorem ipsum")
        catalogue.add("test", 5)
        self.assertEqual(catalogue.catalogue["test"], 5)
        self.assertRaises(ValueError, catalogue.remove, 0)
        self.assertEqual(catalogue.catalogue["test"], 5)


class OffersTests(unittest.TestCase):
    pass


class BasketTests(unittest.TestCase):
    def test_add(self):
        # Assumptions:
        # Add can add news elements
        # Add can update existing elements (like an update function) for simplicity reasons
        # Add will not increment the quantity, it will instead replace the previous value
        # Negative or 0 values in quantity will remove the element
        # Unexpected values will throw ValueError exception
        # We verify the product exists in the catalogue before adding it to the basket
        catalogue = Catalogue()
        catalogue.add("Baked Beans", 3.26)
        basket = Basket(catalogue)

        basket.add("Baked Beans", 4)

        self.assertRaises(ValueError, basket.add, "Biscuits", 1)

        basket.add("Baked Beans", 2)
        self.assertEqual(basket.basket["Baked Beans"], 2)

        basket.add("Baked Beans", 0)
        self.assertRaises(KeyError, lambda: basket.basket["Baked Beans"])

        self.assertRaises(ValueError, basket.add, "Baked Beans", -15)
        self.assertRaises(KeyError, lambda: basket.basket["Baked Beans"])

        self.assertRaises(ValueError, basket.add, "Baked Beans", "£1")
        self.assertRaises(ValueError, basket.add, "Baked Beans", "Lorem ipsum")
        self.assertRaises(ValueError, basket.add, "Lorem ipsum", 100)

    def test_remove(self):
        # Assumptions:
        # If key is wrong then raise ValueError exception
        # Invalid access, will default to KeyError exception
        catalogue = Catalogue()
        catalogue.add("test", 3.26)
        basket = Basket(catalogue)

        basket.add("test", 5)
        self.assertEqual(basket.basket["test"], 5)

        basket.remove("test")
        self.assertRaises(KeyError, lambda: basket.basket["test"])

        self.assertRaises(ValueError, basket.remove, "test")
        self.assertRaises(ValueError, basket.remove, "Lorem ipsum")
        self.assertRaises(ValueError, basket.remove, 0)

        basket.add("test", 5)
        self.assertEqual(basket.basket["test"], 5)
        self.assertEqual(basket.basket["test"], 5)


class BasketPricerTests(unittest.TestCase):
    def test_calculate_subtotal(self):
        # Assumptions:
        # Critical error handling is being done in the other classes.
        # We assume data integrity, however, in a production environment there should be well defined scenarios and
        # use cases for the unexpected with special exceptions accordingly.

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
        basket_pricer = BasketPricer(catalogue, offers, basket)
        self.assertEqual(basket_pricer.subtotal, 5.16)

        basket = Basket(catalogue)
        basket.add("Baked Beans", 2)
        basket.add("Biscuits", 1)
        basket.add("Sardines", 2)
        basket_pricer = BasketPricer(catalogue, offers, basket)
        self.assertEqual(basket_pricer.subtotal, 6.96)

        basket = Basket(catalogue)
        basket.add("Baked Beans", 51)
        basket.add("Biscuits", 100)
        basket.add("Sardines", 150)
        basket_pricer = BasketPricer(catalogue, offers, basket)
        self.assertEqual(basket_pricer.subtotal, 453.99)

    def test_calculate_discount(self):  # TODO: Need to implement Offers first
        pass

    def test_calculate_total(self):
        catalogue = Catalogue()
        catalogue.add("Baked Beans", 0.99)
        catalogue.add("Biscuits", 1.20)
        catalogue.add("Sardines", 1.89)
        catalogue.add("Shampoo (Small)", 2.00)
        catalogue.add("Shampoo (Medium)", 2.50)
        catalogue.add("Shampoo (Large)", 3.50)
        offers = Offers()
        # TODO: add offers and update total values in assertEqual

        basket = Basket(catalogue)
        basket.add("Baked Beans", 4)
        basket.add("Biscuits", 1)
        basket_pricer = BasketPricer(catalogue, offers, basket)
        self.assertEqual(basket_pricer.total, 5.16)

        basket = Basket(catalogue)
        basket.add("Baked Beans", 2)
        basket.add("Biscuits", 1)
        basket.add("Sardines", 2)
        basket_pricer = BasketPricer(catalogue, offers, basket)
        self.assertEqual(basket_pricer.total, 6.96)

        basket = Basket(catalogue)
        basket.add("Baked Beans", 51)
        basket.add("Biscuits", 100)
        basket.add("Sardines", 150)
        basket_pricer = BasketPricer(catalogue, offers, basket)
        self.assertEqual(basket_pricer.total, 453.99)

    def test_init(self):
        catalogue = Catalogue()
        offers = Offers()
        basket = Basket(catalogue)
        basket_pricer = BasketPricer(catalogue, offers, basket)

        self.assertEqual(basket_pricer.subtotal, 0)
        self.assertEqual(basket_pricer.discount, 0)
        self.assertEqual(basket_pricer.total, 0)
        self.assertEqual(basket_pricer.currency, "£")
