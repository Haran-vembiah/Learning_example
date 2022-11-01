"""
A complete end-to-end test for an e-commerce website.
"""
from seleniumbase import BaseCase


class MyTestClass(BaseCase):
    def test_swag_labs(self):
        self.open("https://www.saucedemo.com")
        self.type("#user-name", "standard_user")
        self.type("#password", "secret_sauce\n")
        self.assert_element("div.inventory_list")

    def test_swag_labs1(self):
        self.open("https://www.saucedemo.com")
