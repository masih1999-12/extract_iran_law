from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from string import Template

BASE_URL= Template("https://qavanin.ir/?page=$page&size=1000")
FILE = 'links.txt'

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

try:
    for i in range(1, 165):
        driver.get(BASE_URL.substitute({'page': i}))
        print(f'getting {BASE_URL.substitute({'page': i})}')
        
        WebDriverWait(driver, 9).until(
            EC.presence_of_element_located((By.CLASS_NAME, "text-justify")))
        
        td_elements = driver.find_elements(By.CSS_SELECTOR, "td.text-justify")
        
        with open(FILE, 'a') as f:
            for td in td_elements:
                f.writelines(str(td.find_element(By.TAG_NAME, 'a').get_attribute('href'))+'\n')
finally:
    # Close the browser when finished
    driver.quit()