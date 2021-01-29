import datetime
import time

import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import settings

GOOGLE_API_JSON = settings.GOOGLE_API_JSON
SPREAD_SHEET_KEY = settings.SPREAD_SHEET_KEY

LOGGER = open('log.txt', 'a')
LOGGER.write('Start\n')


def scraping(keyword):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)
     
    driver.get('https://www.google.co.jp/')
    search = driver.find_element_by_name('q')
    search.send_keys(keyword)
     
    time.sleep(3)
    
    suggest_list = driver.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[2]/div[2]/ul')
    items = suggest_list.find_elements_by_tag_name("li")
    
    results = list()
    
    for item in items:
        results.append(item.text)
    
    LOGGER.writelines(results)
    LOGGER.write('\n')
    
    #driver.save_screenshot('search_results.png')
    driver.quit()
    return results


scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_API_JSON, scope)
gc = gspread.authorize(credentials)

book = gc.open_by_key(SPREAD_SHEET_KEY)

master = book.worksheet('マスター')
result = book.worksheet('結果')

scraping_keyword = ''
scraping_results = []
for index, keyword in enumerate(master.col_values(1)):
    flag = master.acell(f'B{index+1}').value
    if flag == "":
        try:
            scraping_keyword = keyword
            scraping_results = scraping(scraping_keyword)
            master.update_acell(f'B{index+1}', datetime.datetime.now().strftime('%Y/%m/%d/ %H:%M:%S'))
            break
        except:
            master.update_acell(f'B{index+1}', 'xpath Error')
            exit()

for scraping_result in scraping_results:
    result.append_row([scraping_keyword, scraping_result])

LOGGER.write('Finish\n')
LOGGER.close()
