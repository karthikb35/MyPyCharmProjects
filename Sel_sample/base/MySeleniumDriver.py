from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

class MySeleniumDriver:
    def __init__(self, driver):
        self.driver = driver

    def element_finder( self, element ):
        try:
            if element.locatorType.lower()=='css':
                element=self.driver.find_element(By.CSS_SELECTOR,element.locator)
            elif element.locatorType.lower()=='id':
                element=self.driver.find_element(By.ID,element.locator)
        except:
            print("Element not found")
        return element

    def sendKeys( self, element, keys ):
        self.element_finder(element).send_keys(keys)

    def click( self, element):
        self.element_finder (element).click()
