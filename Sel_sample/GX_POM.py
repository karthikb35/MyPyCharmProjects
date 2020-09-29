from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.LoginPage import LoginPage

options = Options ( )
options.set_capability ( "acceptInsecureCerts", True )
browser = webdriver.Chrome (
    "C:\\Users\\kbasavarajap\\Downloads\\maria_10.3.11\\chromedriver_win32\\chromedriver.exe", options=options )
browser.implicitly_wait ( 10 )
browser.maximize_window ( )
browser.get ( "https://localhost/login.html" )
time.sleep (3)
login=LoginPage(browser)
login.login("root", "onl")

