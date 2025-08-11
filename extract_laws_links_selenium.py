import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from string import Template

TOTAL=163434
PAGE_SIZE=1000

BASE_URL= Template("https://qavanin.ir/?page=$page&size=$page_size")
FILE = 'links.txt'

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

try:
    with open(FILE, 'a') as f:
        # for i in range(1, TOTAL//PAGE_SIZE + 1):
        i = 1
        while i <= TOTAL//PAGE_SIZE + 1:
            driver.get(BASE_URL.substitute({'page': i, 'page_size': PAGE_SIZE}))
            time.sleep(1)
            print(f'getting {BASE_URL.substitute({'page': i, 'page_size': PAGE_SIZE})}')
            WebDriverWait(driver, 8).until(
                EC.presence_of_element_located((By.CLASS_NAME, "text-justify")))
            td_elements = driver.find_elements(By.CSS_SELECTOR, "td.text-justify")
            print(f'{len(td_elements) = }')
            if len(td_elements) < PAGE_SIZE:
                time.sleep(1)
                driver.refresh()
                continue
            for td in td_elements:
                f.writelines(str(td.find_element(By.TAG_NAME, 'a').get_attribute('href'))+'\n')
            i+=1
finally:
    # Close the browser when finished
    driver.quit()
    