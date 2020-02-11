from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
driver = webdriver.Chrome()

driver.get(url='http://dwlc.pl')
assert "DWLC" in driver.title, 'rzić! ni ma!'
driver.set_page_load_timeout(10)
# driver.find_element_by_xpath('//*[@id="searchform"]/div/label').send_keys('star realms') # nie działa :(
driver.find_element_by_xpath('//*[@id="s"]').send_keys('star realms') # działa
# driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/aside[1]/form/div/input[1]').send_keys('star realms') # działa, Copy full xpath
# driver.find_element_by_name(name='s').send_keys('star realms') # działa
# driver.find_element_by_id(id_='searchsubmit').send_keys('star realms') # nie działa :(

# driver.find_element_by_css_selector(css_selector='#s') # nie działa
driver.find_element_by_xpath(('//*[@id="searchsubmit"]')).click()
sleep(3)
driver.back()
sleep(2)
driver.forward()
WebDriverWait(driver=driver, timeout=10)
print('Page title: ', driver.title)
print('Current url: ', driver.current_url)
sleep(10)


driver.close()
