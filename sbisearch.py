from selenium import webdriver

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

driver = webdriver.Chrome()


url="https://kabuoji3.com/stock/"
driver.get(url)


#WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'top_stock_sec')))
id="6506"
txtId = driver.find_element_by_name("word")
txtId.send_keys(id)
txtId.submit()
a = driver.find_element_by_css_selector("a[href*="+ id +"]")
a.click()


#read config.txt
#get info and export to excel.
