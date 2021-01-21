from django.test import LiveServerTestCase
from django.urls import reverse
from selenium.webdriver.chrome.webdriver import WebDriver

from objectives.models import Objective, Goal


class SeleniumTests(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_goal_value_send_non_digit_keys(self):
        """Sending letters to the value input should have no effect"""
        self.selenium.get(self.live_server_url + reverse('objective-add'))

        # Get Value input field
        value_input = self.selenium.find_element_by_name("goal_set-0-value")
        previous_value = value_input.get_attribute("value")

        # Send letter keys
        value_input.send_keys("asdf")

        # Field should be unchanged
        new_value = value_input.get_attribute("value")
        self.assertEqual(new_value, previous_value)

    def test_goal_value_send_digit_keys(self):
        """Sending numbers to the value input should reflect changes"""
        self.selenium.get(self.live_server_url + reverse('objective-add'))

        # Get Value input field
        value_input = self.selenium.find_element_by_name("goal_set-0-value")
        previous_value = value_input.get_attribute("value")

        # Send number keys
        value_input.send_keys("123")

        # Field should reflect changes
        new_value = value_input.get_attribute("value")
        self.assertEqual(new_value, "123" + previous_value)

    def test_goal_percentage_send_non_digit_keys(self):
        """Sending letters to the percentage input should have no effect"""
        self.selenium.get(self.live_server_url + reverse('objective-add'))

        # Get percentage input field
        percentage_input = self.selenium.find_element_by_name(
            "goal_set-0-percentage")
        previous_percentage = percentage_input.get_attribute("value")

        # Send letter keys
        percentage_input.send_keys("asdf")

        # Field should be unchanged
        new_percentage = percentage_input.get_attribute("value")
        self.assertEqual(new_percentage, previous_percentage)

    def test_goal_percentage_send_digit_keys(self):
        """Sending numbers to the percentage input should reflect changes"""
        self.selenium.get(self.live_server_url + reverse('objective-add'))

        # Get percentage input field
        percentage_input = self.selenium.find_element_by_name(
            "goal_set-0-percentage")
        previous_percentage = percentage_input.get_attribute("value")

        # Send number keys
        percentage_input.send_keys("123")

        # Field should reflect changes
        new_percentage = percentage_input.get_attribute("value")
        self.assertEqual(new_percentage, "123" + previous_percentage)
