from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
options = Options()
options.set_capability("acceptInsecureCerts", True)
# options.add_argument("--headless")

browser = webdriver.Chrome("C:\\Users\\kbasavarajap\\Downloads\\maria_10.3.11\\chromedriver_win32\\chromedriver.exe", options=options)
browser.implicitly_wait(10)
browser.maximize_window()
browser.get("https://10.220.4.207/")
time.sleep(3)
# browser.find_element_by_id("mat-input-0").send_keys("sunadmin")
browser.find_element(By.ID,"mat-input-0").send_keys("sunadmin")
browser.find_element_by_id("mat-input-1").send_keys("Infinera9")
time.sleep(3)

# browser.find_element_by_class_name("mat-icon material-icons mat-icon-no-color").click()
browser.find_element_by_xpath("//button[@class='mat-raised-button mat-primary']").click()
time.sleep(3)
browser.save_screenshot("test.png")
# browser.find_element_by_css_selector("inf-main-layout.ng-star-inserted:nth-child(2) div.main-container mat-toolbar.mat-toolbar.mat-primary.mat-toolbar-single-row inf-nested-menu:nth-child(2) > button.mat-button.ng-star-inserted:nth-child(6)").click()
# time.sleep(2)
browser.find_element_by_xpath("/html[1]/body[1]/inf-root[1]/inf-main-layout[1]/div[1]/mat-toolbar[1]/span[1]/button[1]").click()
time.sleep(3)
browser.find_element_by_xpath("/html[1]/body[1]/div[1]/div[2]/div[1]/div[1]/div[1]/button[1]/span[1]").click()
time.sleep(2)
browser.close()

# browser.get("https://bandcamp.com/")
# # browser.find_element_by_class_name('playbutton').click()
# tracks = browser.find_elements_by_class_name('discover-item')
# # tracks[3].click()
# for tracko in tracks:
#     print(tracko.text.split('\n')[0])
# next_button = [e for e in browser.find_elements_by_class_name('item-page')
#                    if e.text.lower().find('next') > -1]
#
# print("h")
# next_button[0].click()
# tracks = browser.find_elements_by_class_name('discover-item')
# for tracko in tracks:
#     print(tracko.text.split('\n')[0])
