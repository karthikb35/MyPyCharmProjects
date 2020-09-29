from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

options = Options ( )
options.set_capability ( "acceptInsecureCerts", True )
# options.add_argument("--headless")

browser = webdriver.Chrome (
    "C:\\Users\\kbasavarajap\\Downloads\\maria_10.3.11\\chromedriver_win32\\chromedriver.exe", options=options )
browser.implicitly_wait ( 10 )
browser.maximize_window ( )
browser.get ( "https://10.220.4.207/#/auth/login" )
time.sleep ( 3 )
browser.find_element_by_css_selector('input[formcontrolname="username"]').send_keys('sunadmin')
browser.find_element_by_css_selector('input[formcontrolname="password"]').send_keys('Infinera9')
browser.find_element_by_css_selector('input[formcontrolname="password"]').send_keys(Keys.ENTER)
# browser.find_element_by_css_selector('span[text()="Sign In"]').click()
time.sleep(3)
browser.find_element_by_css_selector('inf-main-layout.ng-star-inserted:nth-child(2) div.main-container mat-toolbar.mat-toolbar.mat-primary.mat-toolbar-single-row inf-nested-menu:nth-child(2) button.mat-button.ng-star-inserted:nth-child(3) span.mat-button-wrapper > span:nth-child(2)').click()

time.sleep(2)
entries=[]
while(True):
    browser.find_element_by_css_selector('inf-main-layout.ng-star-inserted:nth-child(2) div.main-container div.main-layout-content inf-events-table.ng-star-inserted:nth-child(2) div.tblEvents div.ui-table.ui-widget.ui-table-responsive.ui-table-hoverable-rows.ui-table-auto-layout div.ui-table-caption.ui-widget-header.ng-star-inserted div.ng-star-inserted div.ui-inputgroup:nth-child(1) > input.ng-valid.ui-inputtext.ui-corner-all.ui-state-default.ui-widget.ng-dirty.ng-touched').send_keys('fail')
    entries=browser.find_elements_by_css_selector('tr.ui-selectable-row ng-star-inserted')
    if(len(entries)>=1):
        break
    browser.find_element_by_css_selector('span.ui-paginator-icon pi pi-caret-right')


