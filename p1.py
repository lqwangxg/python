from selenium import webdriver

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

driver = webdriver.Chrome()
url="https://www.m-mart.co.jp/"
driver.get(url)

driver.find_element_by_link_text('買い手MYページ').click()
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'id')))

txtId = driver.find_element_by_name("id")
txtId.send_keys("annywf")

txtPwd = driver.find_element_by_name("password")
txtPwd.send_keys("1818918wf")

btnSubmit=driver.find_element_by_class_name('button-primary')
btnSubmit.submit()
driver.find_element_by_name("order_list").click()
