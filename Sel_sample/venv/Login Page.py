from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.by import By
from PageFactory import *
driver = webdriver.Chrome()

class LoginPage(object):
    def __init__(self, driver):
        self.driver = driver
        self.driver =  webdriver.Chrome()

        self.username = self.driver.find_element(By.NAME, )
