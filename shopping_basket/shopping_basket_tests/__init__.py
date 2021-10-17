import unittest
from basket_pricer import Catalogue, Offers, Basket, BasketPricer


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
    def test_round_up(self):
        # Assumptions:
        # Discount is rounded up as per the assignment example for the 2 Sardines which got rounded up
        # instead of the default round down (£0.94 vs £0.95).
        offers = Offers()
        for i in range(101):
            self.assertEqual(offers.round_up(i, 2), i)

        self.assertEqual(offers.round_up(0.940, 2), 0.94)
        self.assertEqual(offers.round_up(0.941, 2), 0.95)
        self.assertEqual(offers.round_up(0.942, 2), 0.95)
        self.assertEqual(offers.round_up(0.943, 2), 0.95)
        self.assertEqual(offers.round_up(0.944, 2), 0.95)
        self.assertEqual(offers.round_up(0.945, 2), 0.95)
        self.assertEqual(offers.round_up(0.946, 2), 0.95)
        self.assertEqual(offers.round_up(0.947, 2), 0.95)
        self.assertEqual(offers.round_up(0.948, 2), 0.95)
        self.assertEqual(offers.round_up(0.949, 2), 0.95)
        self.assertEqual(offers.round_up(0.95, 2), 0.95)
        self.assertEqual(offers.round_up(0.951, 2), 0.96)
        self.assertEqual(offers.round_up(0.951000, 2), 0.96)
        self.assertEqual(offers.round_up(0.951999, 2), 0.96)

    def test_calculate_discount(self):
        catalogue = Catalogue()
        catalogue.add("test", 100)
        catalogue.add("Lorem ipsum", 1)
        basket = Basket(catalogue)
        basket.add("test", 3)
        basket.add("Lorem ipsum", 3)
        offers = Offers()

        offers.add_offer(lambda user_basket: offers.percentage_discount("test", 25, user_basket))
        self.assertEqual(offers.calculate_discount(basket), 75)

        offers.add_offer(lambda user_basket: offers.buy_x_get_y_free("Lorem ipsum", 2, "Lorem ipsum", 1, user_basket))
        self.assertEqual(offers.calculate_discount(basket), 76)

    def test_buy_x_get_y_free(self):
        catalogue = Catalogue()
        catalogue.add("test", 100)
        catalogue.add("Lorem ipsum", 1)
        basket = Basket(catalogue)
        basket.add("test", 3)
        basket.add("Lorem ipsum", 1)
        offers = Offers()
        self.assertEqual(offers.buy_x_get_y_free("test", 2, "test", 1, basket), 100)
        self.assertEqual(offers.buy_x_get_y_free("Lorem ipsum", 2, "Lorem ipsum", 1, basket), 0)
        basket.add("Lorem ipsum", 2)
        self.assertEqual(offers.buy_x_get_y_free("Lorem ipsum", 2, "Lorem ipsum", 1, basket), 0)
        basket.add("Lorem ipsum", 3)
        self.assertEqual(offers.buy_x_get_y_free("Lorem ipsum", 2, "Lorem ipsum", 1, basket), 1)
        basket.add("Lorem ipsum", 4)
        self.assertEqual(offers.buy_x_get_y_free("Lorem ipsum", 2, "Lorem ipsum", 1, basket), 1)
        self.assertEqual(offers.buy_x_get_y_free("Lorem ipsum", 1, "test", 1, basket), 300)
        self.assertEqual(offers.buy_x_get_y_free("Lorem ipsum", 2, "test", 1, basket), 200)
        self.assertEqual(offers.buy_x_get_y_free("Lorem ipsum", 3, "test", 1, basket), 100)
        self.assertEqual(offers.buy_x_get_y_free("Lorem ipsum", 4, "test", 1, basket), 100)
        self.assertEqual(offers.buy_x_get_y_free("Lorem ipsum", 4, "test", 2, basket), 200)
        self.assertEqual(offers.buy_x_get_y_free("Lorem ipsum", 4, "test", 3, basket), 300)
        self.assertEqual(offers.buy_x_get_y_free("Lorem ipsum", 4, "test", 4, basket), 300)

    def test_percentage_discount(self):
        # Assumptions:
        # We assume the percentage discount is always a deduction
        # We assume the percentage discount is int instead of float as it's rare to find discount percentages as floats
        # Negative or 0 percentage discounts will throw an exception
        # X value cannot be 0 or less than 0
        # Y value cannot be 0 or less than 0
        # Discount is rounded up as per the assignment example for the 2 Sardines which got rounded up
        # instead of the default round down (£0.94 vs £0.95).
        # We assume 100% discount is possible although questionable. Similarly, 99% or 98% would also be questionable.
        catalogue = Catalogue()
        catalogue.add("test", 100)
        basket = Basket(catalogue)
        basket.add("test", 1)
        offers = Offers()
        self.assertRaises(ValueError, offers.percentage_discount, "test", "£10", basket)
        self.assertRaises(ValueError, offers.percentage_discount, "test", -10, basket)
        self.assertRaises(ValueError, offers.percentage_discount, "test", 0, basket)
        for i in range(1, 101):
            self.assertEqual(offers.percentage_discount("test", i, basket), i)

        catalogue = Catalogue()
        catalogue.add("test", 1)
        basket = Basket(catalogue)
        basket.add("test", 1)
        offers = Offers()
        self.assertRaises(ValueError, offers.percentage_discount, "test", "10", basket)
        self.assertRaises(ValueError, offers.percentage_discount, "test", -10, basket)
        self.assertRaises(ValueError, offers.percentage_discount, "test", 0, basket)
        for i in range(1, 101):
            self.assertEqual(offers.percentage_discount("test", i, basket), offers.round_up((1 * i) / 100, 2))


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

    def test_calculate_discount(self):
        catalogue = Catalogue()
        catalogue.add("test", 50)
        catalogue.add("Lorem ipsum", 25)
        basket = Basket(catalogue)
        basket.add("test", 10)
        basket.add("Lorem ipsum", 10)
        offers = Offers()

        offers.add_offer(lambda user_basket: offers.percentage_discount("test", 25, user_basket))
        self.assertEqual(offers.calculate_discount(basket), 125)

        offers.add_offer(lambda user_basket: offers.buy_x_get_y_free("Lorem ipsum", 2, "Lorem ipsum", 1, user_basket))
        self.assertEqual(offers.calculate_discount(basket), 200)

    def test_calculate_total(self):
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
        basket_pricer = BasketPricer(catalogue, offers, basket)
        self.assertEqual(basket_pricer.total, 4.17)

        basket = Basket(catalogue)
        basket.add("Baked Beans", 2)
        basket.add("Biscuits", 1)
        basket.add("Sardines", 2)
        basket_pricer = BasketPricer(catalogue, offers, basket)
        self.assertEqual(basket_pricer.total, 6.01)

        basket = Basket(catalogue)
        basket.add("Baked Beans", 51)
        basket.add("Biscuits", 100)
        basket.add("Sardines", 150)
        basket_pricer = BasketPricer(catalogue, offers, basket)
        self.assertEqual(basket_pricer.total, 366.28)

    def test_init(self):
        catalogue = Catalogue()
        offers = Offers()
        basket = Basket(catalogue)
        basket_pricer = BasketPricer(catalogue, offers, basket)

        self.assertEqual(basket_pricer.subtotal, 0)
        self.assertEqual(basket_pricer.discount, 0)
        self.assertEqual(basket_pricer.total, 0)
        self.assertEqual(basket_pricer.currency, "£")
