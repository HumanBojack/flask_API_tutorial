from selenium import webdriver

base_url = "http://127.0.0.1:5000/"

driver = webdriver.Firefox()
driver.get(base_url)

print(driver.title)