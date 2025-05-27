from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import data
import helpers
from data import MESSAGE_FOR_DRIVER


class UrbanRoutesPage:


    # Locators (example, adjust according to actual site)
    ADDRESS_FROM_INPUT = (By.ID, "from")
    ADDRESS_TO_INPUT = (By.ID, "to")
    ROUTE_SET_BUTTON = (By.ID, "set-route-btn")  # example, adjust as needed
    SUPPORTIVE_OPTION = (By.XPATH, "//div[text()='Supportive']")
    ACTIVE_OPTION = (By.CSS_SELECTOR, ".tcard.active .tcard-title")
    PHONE_INPUT = (By.ID, "phone")
    SMS_INPUT = (By.ID, "code")
    PHONE_BUTTON = (By.XPATH, "//div[@class='np-text' and text()='Phone number']")
    PAYMENT_BUTTON = (By. CLASS_NAME, "pp-value-text")
    ADD_CARD_BUTTON = (By.CLASS_NAME, "pp-plus")
    CARD_NUMBER_INPUT = (By.ID, "number")
    CARD_CODE_INPUT = (By.CSS_SELECTOR, "#code.card-input")
    LINK_BUTTON = (By.XPATH, "//button[text()='Link']")
    DRIVER_COMMENT_INPUT = (By.CSS_SELECTOR, "#comment.input")
    BLANKET_HANDKERCHIEF_SLIDER = (By.XPATH, "//span[@class='slider round']")
    BLANKET_HANDKERCHIEF_CHECKBOX = (By.CSS_SELECTOR, "#root > div > div.workflow > div.workflow-subcontainer > div.tariff-picker.shown > div.form > div.reqs.open > div.reqs-body > div:nth-child(1) > div > div.r-sw > div > input")
    ADD_ICE_CREAM_BUTTON = (By.XPATH, "//div[@class='counter-plus' and text()='+']")
    ICE_CREAM_COUNTER_VALUE = (By.CSS_SELECTOR, "#root > div > div.workflow > div.workflow-subcontainer > div.tariff-picker.shown > div.form > div.reqs.open > div.reqs-body > div.r.r-type-group > div > div.r-group-items > div:nth-child(1) > div > div.r-counter > div > div.counter-value")
    ORDER_BUTTON = (By.CSS_SELECTOR, "#root > div > div.workflow > div.smart-button-wrapper > button > span.smart-button-main")
    CAR_MODAL_DISPLAY = (By.CSS_SELECTOR, "#root > div > div.order.shown > div.order-body > div.order-header > div > div.order-header-title")

    def __init__(self, driver):
        self.driver = driver

    def set_address(self, address_from, address_to):
        from_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.ADDRESS_FROM_INPUT)
        )
        from_input.clear()
        from_input.send_keys(address_from)

        to_input = self.driver.find_element(*self.ADDRESS_TO_INPUT)
        to_input.clear()
        to_input.send_keys(address_to)

    def get_from(self):
        return self.driver.find_element(*self.ADDRESS_FROM_INPUT).get_attribute("value")

    def get_to(self):
        return self.driver.find_element(*self.ADDRESS_TO_INPUT).get_attribute("value")

    def select_mode(self):
        if self.get_active_plan()!="Supportive":
            self.driver.find_element(*self.SUPPORTIVE_OPTION).click()

    def get_active_plan(self):
       return self.driver.find_element(*self.ACTIVE_OPTION).text

    def click_call_taxi_button(self):
        call_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Call a taxi')]"))
        )
        call_button.click()
        print("Clicked the Call a taxi button.")

    def open_phone_modal_and_fill(self, phone_number):
        # Click the "Phone number" button to open modal
        # Wait until phone input is visible in modal
        phone_button = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.PHONE_BUTTON)
        )
        phone_button.click()

        # Wait until phone input is visible in modal
        phone_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.PHONE_INPUT)
        )

        # Clear and fill the phone input
        phone_input.clear()
        phone_input.send_keys(phone_number)
        phone_input.send_keys(Keys.RETURN)

    def input_sms_code(self, code):
        # Wait until phone input is visible in modal
        sms_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.SMS_INPUT)
        )
        #code = helpers.retrieve_phone_code(self.driver)
        # Clear and fill the sms input
        sms_input.clear()
        sms_input.send_keys(code)
        sms_input.send_keys(Keys.RETURN)

    def get_saved_phone(self):
        return self.driver.find_element(*self.PHONE_INPUT).get_attribute('value')

    def open_payment_modal_and_fill(self, card_number, card_code):
        payment_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable (self.PAYMENT_BUTTON))
        payment_button.click()

        add_card_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.ADD_CARD_BUTTON))
        add_card_button.click()

        card_number_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.CARD_NUMBER_INPUT))


        card_number_input.clear()
        card_number_input.send_keys(card_number)

        card_code_input = self.driver.find_element(*self.CARD_CODE_INPUT)
        card_code_input.clear()
        card_code_input.send_keys(card_code)
        card_code_input.send_keys(Keys.TAB)

        link_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.LINK_BUTTON))
        link_button.click()

    def get_payment_method(self):
        return self.driver.find_element(*self.PAYMENT_BUTTON).text

    def comment_for_driver(self, message):
        comment_input = self.driver.find_element(*self.DRIVER_COMMENT_INPUT)
        comment_input.clear()
        comment_input.send_keys(message)

    def get_message(self):
        return self.driver.find_element(*self.DRIVER_COMMENT_INPUT).get_attribute('value')

    def order_blanket_and_handkerchiefs(self):
        self.driver.find_element(*self.BLANKET_HANDKERCHIEF_SLIDER).click()

    def blankets_and_handkerchiefs_selected(self):
        return self.driver.find_element(*self.BLANKET_HANDKERCHIEF_CHECKBOX).get_attribute('checked')

    def order_ice_cream(self, count=2):
        for _ in range(count):
            self.driver.find_element(*self.ADD_ICE_CREAM_BUTTON).click()

    def ice_creams_ordered(self):
        return self.driver.find_element(*self.ICE_CREAM_COUNTER_VALUE).text

    def click_order_button(self):
        self.driver.find_element(*self.ORDER_BUTTON).click()

    def car_search_modal_display(self):
        return self.driver.find_element(*self.CAR_MODAL_DISPLAY).text


