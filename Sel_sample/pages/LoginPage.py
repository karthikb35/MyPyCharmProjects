from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from base.MySeleniumDriver import MySeleniumDriver
from base.Element import Element


class LoginPage(MySeleniumDriver):
    def __init__(self,driver):
        super().__init__(driver)
        self.driver = driver

    #Locators are defined here
    username = Element(locatorType= "css", locator ="input#web-username")

    password = Element(locatorType= "css", locator ="input#web-password")

    loginButton = Element(locatorType= "css", locator ="input#react-login-submit")

    rememberme=Element(locatorType="css", locator="input#isRemberPwdId")

    #Page Operations are defined here
    def login( self,user_name,pass_word ):
        self.sendKeys(self.username,user_name)
        self.sendKeys(self.password,pass_word)
        time.sleep(2)
        self.click ( self.rememberme )
        time.sleep(2)
        self.click(self.loginButton)


