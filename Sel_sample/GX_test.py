from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select



def Launch():
    options = Options ( )
    options.set_capability ( "acceptInsecureCerts", True )
    # options.add_argument("--headless")

    browser = webdriver.Chrome (
        "C:\\Users\\kbasavarajap\\Downloads\\maria_10.3.11\\chromedriver_win32\\chromedriver.exe", options=options )
    browser.implicitly_wait ( 10 )
    browser.maximize_window ( )
    browser.get ( "https://localhost/login.html" )
    time.sleep ( 3 )
    return browser

def Login(browser):
    browser.find_element_by_css_selector ( "input#web-username" ).send_keys ( "root" )
    browser.find_element_by_css_selector ( "input#web-password" ).send_keys ( "onl" )
    browser.find_element_by_css_selector ( "input#react-login-submit" ).click ( )
    print(browser.find_element_by_css_selector("#sidebar").get_attribute('class'))
    time.sleep(4)
    return browser

def HideSidebar(browser):
    if browser.find_element_by_css_selector("#sidebar").get_attribute('class')=='sidebar-width':
        browser.find_element_by_css_selector ( "#react-navbar-btn" ).click()
        time.sleep(2)
    return browser

def ShowSideBar(browser):
    if browser.find_element_by_css_selector("#sidebar").get_attribute('class')=='sidebar-width-wrap':
        browser.find_element_by_css_selector ( "#react-navbar-btn" ).click()
        time.sleep(2)
    element=browser.find_element_by_css_selector('canvas#chassisView1')
    # element.location['x']
    action = webdriver.common.action_chains.ActionChains ( browser )
    action.move_to_element_with_offset ( element, 5, 15 )
    time.sleep(3)
    action.move_by_offset(3,2).perform()
    action.context_click(element).perform()
    time.sleep(2)
    action.move_by_offset(0,-6).perform()
    action.context_click ( element ).perform ( )
    time.sleep ( 2 )
    action.move_by_offset(3,-4 ).perform()
    time.sleep ( 3 )
    action.context_click ( element).perform()

    time.sleep ( 3 )
    action.click().perform()
    return browser


def EquipmentTable(browser):
    browser.find_element_by_link_text('Equipment & Facility').click()
    browser.find_element_by_link_text('Equipment').click()
    columns=browser.find_elements_by_css_selector('tr.react-treetable-header-row')
    col_text=[]
    for col in columns:
        col_text.append(col.text)
    print(col_text)
    return browser


def Logout(browser):
    browser.find_element_by_css_selector("a#react-user-sys-dropdown-btn").click()
    time.sleep(2)
    browser.find_element_by_css_selector("a#react-menu-logout-btn").click()
    time.sleep(2)
    # browser.find_element_by_class_name("a.sgBtn.ok").click()
    browser.find_element_by_link_text("Yes").click()
    time.sleep(2)
    return browser



def Close(browser):
    browser.close ( )


Login_page=Launch()
Home_page=Login(Login_page)
Hidden=HideSidebar(Home_page)
time.sleep(3)
Shown=ShowSideBar(Hidden)
time.sleep(2)
Eq=EquipmentTable(Shown)
browser=Logout(Eq)
Close(browser)
