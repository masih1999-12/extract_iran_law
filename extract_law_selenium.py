from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import mysql.connector
import os
import time
from collections import OrderedDict

load_dotenv()

FILE = 'links5.txt'
LINKS=None

with open(FILE, 'r')as f:
    LINKS=tuple(f.readlines())

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

query = """
            INSERT IGNORE INTO iran_laws
                (id,title,text,type,approval_authority,date_of_approval_document,
                notice_number,notification_authority,official_newspaper_number,
                status,classification,approval_date,approval_document_number,
                notification_date,execution_date,official_newspaper_date,
                release_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

connection = mysql.connector.connect(
    host="localhost",
    port=3306,
    user=os.environ.get('DB_USER', 'root'), 
    password=os.environ.get('DB_PASS', ''), 
    database="iran_laws" 
)

cursor = connection.cursor()
counter = 1
try:
    for link in LINKS:
        print('*************************************')
        print(f'*********{counter = }***************')
        print('*************************************')
        data = OrderedDict()
        data['id'] = link.split('=')[1].strip()
        driver.get(link)
        print(f'getting {link}')
        
        # TEXT
        WebDriverWait(driver, 9).until(
            EC.presence_of_element_located((By.CLASS_NAME, "mytitle")))
        
        try:
            h1_element_text = driver.find_element(By.CSS_SELECTOR, "h1.mytitle").text
        except Exception as e:
            h1_element_text=''
            
        data['title'] = h1_element_text.strip()

        try:
            paragraph_text = driver.find_elements(By.CLASS_NAME, "SecTex ")[0].text
        except Exception as e:
            paragraph_text = ''
            
        data['text'] = paragraph_text.strip()
        
        # Attribute
        link_att = link.replace('TreeText','Attribute')
        driver.get(link_att)
        print(f'getting {link_att}')
        WebDriverWait(driver, 9).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h1.mytitle")))
        
        attributes = driver.find_elements(By.CSS_SELECTOR, "span.text-left")
        data['type'] = attributes[0].text.strip()
        data['approval_authority'] = attributes[1].text.strip()
        data['date_of_approval_document'] = attributes[2].text.strip() if attributes[2].text.strip() else None
        data['notice_number'] = attributes[3].text.strip()
        data['notification_authority'] = attributes[4].text.strip()
        data['official_newspaper_number'] = attributes[5].text.strip()
        data['status'] = attributes[6].text.strip()
        data['classification'] = attributes[7].text.strip()
        data['approval_date'] = attributes[8].text.strip() if attributes[8].text.strip() else None
        data['approval_document_number'] = attributes[9].text.strip()
        data['notification_date'] = attributes[10].text.strip() if attributes[10].text.strip() else None
        data['execution_date'] = attributes[11].text.strip() if attributes[11].text.strip() else None
        data['official_newspaper_date'] = attributes[12].text.strip() if attributes[12].text.strip() else None
        data['release_date'] = attributes[13].text.strip() if attributes[13].text.strip() else None
        
        cursor.execute(query, list(data.values()))
        connection.commit()
        time.sleep(1)
finally:
    # Close the browser when finished
    driver.quit()
    cursor.close()
    connection.close()
    