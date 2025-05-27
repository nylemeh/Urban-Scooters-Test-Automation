from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

import data
import helpers
from pages import UrbanRoutesPage


class TestUrbanRoutes:

    @classmethod
    def setup_class(cls):
        # do not modify - we need additional logging enabled in order to retrieve phone confirmation code
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome()
        if helpers.is_url_reachable(data.URBAN_ROUTES_URL):
            print("Connected to the Urban Routes server.")
        else:
            raise Exception("Cannot connect to Urban Routes. Check the server is on and still running.")

    def test_set_route(self):
        self.driver.get(data.URBAN_ROUTES_URL)

        # Initialize the Page Object
        page = UrbanRoutesPage(self.driver)
        page.set_address(data.ADDRESS_FROM, data.ADDRESS_TO)

        assert page.get_from() == data.ADDRESS_FROM
        assert page.get_to() == data.ADDRESS_TO

    def test_select_mode(self):
        self.driver.get(data.URBAN_ROUTES_URL)

        # Initialize the Page Object
        page = UrbanRoutesPage(self.driver)
        page.set_address(data.ADDRESS_FROM, data.ADDRESS_TO)
        page.click_call_taxi_button()
        page.select_mode()
        assert page.get_active_plan() == "Supportive"

    def test_fill_phone_number(self):
        self.driver.get(data.URBAN_ROUTES_URL)

        # Initialize the Page Object
        page = UrbanRoutesPage(self.driver)
        page.set_address(data.ADDRESS_FROM, data.ADDRESS_TO)
        page.click_call_taxi_button()
        page.open_phone_modal_and_fill(data.PHONE_NUMBER)
        code = helpers.retrieve_phone_code(self.driver)
        page.input_sms_code(code)

        assert page.get_saved_phone() == data.PHONE_NUMBER

    def test_fill_card(self):
        self.driver.get(data.URBAN_ROUTES_URL)

        # Initialize the Page Object
        page = UrbanRoutesPage(self.driver)
        page.set_address(data.ADDRESS_FROM, data.ADDRESS_TO)
        page.click_call_taxi_button()
        page.open_payment_modal_and_fill(data.CARD_NUMBER, data.CARD_CODE)
        assert page.get_payment_method() == "Card"

    def test_comment_for_driver(self):
        self.driver.get(data.URBAN_ROUTES_URL)

        # Initialize the Page Object
        page = UrbanRoutesPage(self.driver)
        page.set_address(data.ADDRESS_FROM, data.ADDRESS_TO)
        page.click_call_taxi_button()
        page.comment_for_driver(data.MESSAGE_FOR_DRIVER)
        assert page.get_message() == data.MESSAGE_FOR_DRIVER

    def test_order_blanket_and_handkerchiefs(self):
        self.driver.get(data.URBAN_ROUTES_URL)

        # Initialize the Page Object
        page = UrbanRoutesPage(self.driver)
        page.set_address(data.ADDRESS_FROM, data.ADDRESS_TO)
        page.click_call_taxi_button()
        page.select_mode()
        page.order_blanket_and_handkerchiefs()
        assert page.blankets_and_handkerchiefs_selected() == 'true'


    def test_order_2_ice_creams(self):
        self.driver.get(data.URBAN_ROUTES_URL)

        # Initialize the Page Object
        page = UrbanRoutesPage(self.driver)
        page.set_address(data.ADDRESS_FROM, data.ADDRESS_TO)
        page.click_call_taxi_button()
        page.select_mode()
        page.order_ice_cream()
        assert page.ice_creams_ordered() == "2"

    def test_car_search_model_appears(self):
        self.driver.get(data.URBAN_ROUTES_URL)

        # Initialize the Page Object
        page = UrbanRoutesPage(self.driver)
        page.set_address(data.ADDRESS_FROM, data.ADDRESS_TO)
        page.click_call_taxi_button()
        page.select_mode()
        page.comment_for_driver(data.MESSAGE_FOR_DRIVER)
        page.click_order_button()
        assert page.car_search_modal_display() == "Car search"

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()