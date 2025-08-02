from bs4 import BeautifulSoup
import requests
import mysql.connector
import time
from string import Template

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'authority': 'qavanin.ir','method': 'GET', 'path':'/', 'scheme': 'https',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-encoding': 'gzip, deflate, br, zstd', 'accept-language': 'en-US,en;q=0.9,pl;q=0.8,fa;q=0.7', 'cache-control': 'no-cache',
    'cookie': '__arcsjs=03348a90a847591004d853910499ce58; ASP.NET_SessionId=bcrbzyfzz22jmcw04rhlale1; cookiesession1=678B28830CDD45793269489F9E1E9643',
    'pragma':'no-cache', 'priority': 'u=0, i', 'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Microsoft Edge";v="138"',
    'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': "Linux", 'sec-fetch-dest': 'document', 'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none', 'sec-fetch-user': '?1', 'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0'
}
BASE_URL= Template("https://qavanin.ir/page=$page?size=25")
connection = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="", 
    password="", 
    database="iran_laws" 
)

cursor = connection.cursor()

counter = 1
for i in range(1,2):
    print('__________________')
    print(f'page = {i}')
    print('__________________')
    with requests.Session() as session:
        session.headers.update(headers)
        
        # The first request will get the necessary cookies
        response = session.get('https://qavanin.ir/')
        
        # You can then use the session for subsequent requests
        print(response.status_code)
        break
    page = requests.get(BASE_URL.substitute({'page': str(i)}),headers=headers)
    page = requests.get('https://qavanin.ir/Law/TreeText/?IDS=4061739163395626925')
    
    print(f'{page = }')
    print(f'{page.status_code = }')
    page.raise_for_status()
    if page.status_code == 200:
        
        content = page.content
        
    Data = {}
    DOMdocument = BeautifulSoup(content, 'html.parser')
    tds = DOMdocument.find_all('td', class_='text-justify')
    print(tds)
    break
    for td in tds:
        title = td[1].a.text.strip()
        link = cols[1].a['href'].strip()
        date = cols[2].text.strip()
        case_id = cols[3].text.strip()
        category = cols[4].text.strip()
        court = cols[5].text.strip()
        while True:
            try:
                page = requests.get("https://ara.jri.ac.ir"+link)
                break
            except Exception as e:
                time.sleep(0.5)
                pass
        text_page_document = BeautifulSoup(page.content, 'html.parser')
        text = text_page_document.find('div', id='treeText')
        for tag in text(['button', 'h2']):
            tag.decompose()
        text = text.get_text().replace('\n','').replace('\r', '').strip()
        # Prepare the INSERT query
        query = """
            INSERT INTO legal_cases (id, title, link, date, case_id, category, court, text)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        data = (index, title, link, date, case_id, category, court, text)
        # Execute the query
        cursor.execute(query, data)
        # Commit the changes
        connection.commit()
        print(f'{index = }')
        print(f'{link = }')
        
cursor.close()
connection.close()