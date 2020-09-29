from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import time
from selenium.webdriver.support.ui import Select

def setup ( ):
    options = Options ( )
    options.add_argument ( '--allow-running-insecure-content' )
    options.add_argument ( '--ignore-certificate-errors' )
    browser = webdriver.Chrome (
        "C:\\Users\\kbasavarajap\\Downloads\\maria_10.3.11\\chromedriver.exe", options=options )
    browser.get ( "https://172.16.11.194" )
    time.sleep ( 5 )
    browser.maximize_window ( )

    return browser


def login_ne ( browser, username='root', password='onl' ):
    print ( "Trying to login to NE" )
    search_field = browser.find_element_by_id ( "web-username" )
    search_field.clear ( )
    search_field.send_keys ( username )
    search_field = browser.find_element_by_id ( "web-password" )
    search_field.send_keys ( password )
    a= browser.find_element_by_id ( "react-login-submit" )


    print(a.text, a.parent, a.rect, a.id, a.tag_name)
    a.click()

def createXcon( source, destination, name="autocreated", label='autocreatedXCON' ):
    driver.find_element_by_css_selector('input[value="Create XCON Manual"]').click()
    time.sleep ( 2 )
    driver.find_element_by_css_selector('input#name').send_keys(name)
    # self.sendKeys ( locator='input#name', locatorType='css', data=name )
    time.sleep ( 2 )
    driver.find_element_by_css_selector('input#label').send_keys(label)
    # self.sendKeys ( locator='input#label', locatorType='css', data=label )
    time.sleep ( 2 )
    select = Select(driver.find_element_by_css_selector('select#source'))
    select.select_by_visible_text(source)
    # self.dropdownSelectElement ( locator='select#source', locatorType="css", selector=source, selectorType="text" )
    time.sleep ( 2 )
    select = Select ( driver.find_element_by_css_selector ( 'select#destination' ) )
    select.select_by_visible_text ( destination )
    # self.dropdownSelectElement ( locator='select#destination', locatorType="css", selector=destination,selectorType="text" )
    time.sleep ( 2 )
    driver.find_element_by_css_selector('a.button.okBtn').click()


    # self.elementClick ( locatorType='css', locator='a.button.okBtn' )
    time.sleep ( 5 )
    self.elementClick ( locator=self.refreshButton.locator, locatorType=self.refreshButton.locatorType )
    time.sleep ( 2 )
    row = self.findXcon ( searchBy="name", searchText=name )



driver = setup ( )

login_ne ( driver )

time.sleep ( 5 )
driver.find_element_by_link_text ( 'L1 Service' ).click ( )
time.sleep(3)
a=driver.find_element_by_xpath ( '//tr[contains(@class,"oddTrClass")]')
b=a.find_element_by_xpath('./td[18]/a[1]')
b.click()

time.sleep ( 5 )


# listCheck = ['10']
# element = driver.find_element_by_xpath (
#     '//*[@id="react_collapse_table_body_table_id_1387998041"]/div/div[1]/table/tbody/tr[1]/td[5]' )  ## empty attribute
# print ( "Empty attribute should be printed  below" )
# print ( element.get_attribute ( 'data-value' ) )
# listCheck.append ( element.get_attribute ( 'data-value' ) )
# time.sleep ( 5 )
# listCheck.append ( element.find_element_by_xpath (
#     '//*[@id="react_collapse_table_body_table_id_1387998041"]/div/div[1]/table/tbody/tr[1]/td[3]' ).get_attribute (
#     'data-value' ) )
#
# time.sleep ( 5 )
#
# print ( listCheck )
# '''
# print(driver.find_element_by_id('name').is_enabled())
#
# print(driver.find_element_by_id('label').is_enabled())
#
# print(driver.find_element_by_id('rack-name').get_attribute("innerText"))
# '''

driver.quit ( )

