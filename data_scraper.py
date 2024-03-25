from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import csv 


#create CSV and write headers into the file


header = ['Title', 'Dimension (mm)', 'Weight (cts)', 'Certified Gemstones', 'Treatment', 'Clarity', 'Type',
          'Shape', 'Price', 'Estimated RRP']

#make sure to comment this...
with open('Gemstone_raw_data.csv', 'w', newline='', encoding='UTF8') as f:
    writer = csv.writer(f)
    writer.writerow(header)

#...out before running again so it will not overwrite the existing scraped data


url = 'https://www.gemrockauctions.com/stores/gemex'

driver = webdriver.Chrome()

driver.get(url)
driver.maximize_window()
gem = 1
while(True):
    time.sleep(3)    
    i = 1
    links = []
    links = driver.find_elements(By.PARTIAL_LINK_TEXT, 'Ct')
    for link in links:
        if(i == 1):
            ActionChains(driver) \
                .key_down(Keys.DOWN) \
                .key_up(Keys.DOWN) \
                .key_down(Keys.DOWN) \
                .key_up(Keys.DOWN) \
                .key_down(Keys.DOWN) \
                .key_up(Keys.DOWN) \
                .key_down(Keys.DOWN) \
                .key_up(Keys.DOWN) \
                .key_down(Keys.DOWN) \
                .key_up(Keys.DOWN) \
                .key_down(Keys.DOWN) \
                .key_up(Keys.DOWN) \
                .key_down(Keys.DOWN) \
                .key_up(Keys.DOWN) \
                .key_down(Keys.DOWN) \
                .key_up(Keys.DOWN) \
                .key_down(Keys.DOWN) \
                .key_up(Keys.DOWN) \
                .perform()
        if(i % 9 == 0):
            ActionChains(driver) \
                .key_down(Keys.SPACE) \
                .key_up(Keys.SPACE) \
                .perform()
        time.sleep(2)
        ActionChains(driver) \
            .key_down(Keys.CONTROL) \
            .move_to_element(link) \
            .click() \
            .key_up(Keys.CONTROL) \
            .perform()
        try:
            driver.switch_to.window(driver.window_handles[1])
        except:
            ActionChains(driver) \
                .key_down(Keys.SPACE) \
                .key_up(Keys.SPACE) \
                .key_down(Keys.CONTROL) \
                .move_to_element(link) \
                .click() \
                .click() \
                .click() \
                .key_up(Keys.CONTROL) \
                .perform()
            time.sleep(2)
            try:
                driver.switch_to.window(driver.window_handles[1])
            except:
                ActionChains(driver) \
                    .key_down(Keys.SPACE) \
                    .key_up(Keys.SPACE) \
                    .key_down(Keys.CONTROL) \
                    .move_to_element(link) \
                    .click() \
                    .click() \
                    .click() \
                    .key_up(Keys.CONTROL) \
                    .perform()
                time.sleep(2)
                driver.switch_to.window(driver.window_handles[1])
    
        
        time.sleep(3)
        #start the script for scraping
        html = driver.page_source
        soup1 = BeautifulSoup(html, "html.parser")
        soup2 = BeautifulSoup(soup1.prettify(), "html.parser")
        #getting title
        title = soup2.find(class_ = 'text-2xl font-bold text-gray-900 whitespace-normal').text
        #initialize dd string
        dimm = "" 
        weig = ""
        cergem = ""
        trea = ""
        clar = ""
        type1 = ""
        shape = ""
        # getting 'dd' data
        dt_tags = soup2.find_all('dt')

        # Iterate through each <dt> tag and get the corresponding <dd> text
        for dt in dt_tags:
            # Get the next sibling which should be <dd> tag
            dd = dt.find_next_sibling('dd')
            if dd:
                txt = dt.get_text()
                txt = txt.strip()
                if  txt == "Dimensions (mm)":
                    dimm = dd.get_text()
                if txt == "Weight (cts)":
                    weig = dd.get_text()
                if txt == "Certified Gemstones":
                    cergem = dd.get_text()
                if txt == "Treatment":
                    trea = dd.get_text()
                if txt == "Clarity" :
                    clar = dd.get_text()
                if txt == "Type" :
                    type1 = dd.get_text()
                if txt == "Shape" :
                    shape = dd.get_text()
        #getting price and est rrp
        try:
            price = soup2.find(class_ = 'text-xl font-bold flex items-center text-gray-800').text
            price = price.strip()[1:]
            price = price.strip()[:-3]
        except:
            price = ""
            
        try:
            rrp = soup2.find(class_ = 'text-gray-500 text-sm').text
            rrp = rrp.strip()[15:]
        except:
            rrp = ""
        
        #cleaning
        title = title.strip()
        dimm = dimm.strip()[:-2]
        dimm = dimm.strip()
        weig = weig.strip()
        cergem = cergem.strip()
        trea = trea.strip()
        clar = clar.strip()
        type1 = type1.strip()
        shape = shape.strip()
        time.sleep(2)
        #load our data to the csv
        print(f"gem data number {gem}:")
        print(title)
        print(dimm)
        print(weig)
        print(cergem)
        print(trea)
        print(clar)
        print(type1)
        print(shape)
        print(price)
        print(rrp)
        data = [title, dimm, weig, cergem, trea, clar, type1, shape, price, rrp]
        time.sleep(3)
        with open('Gemstone_raw_data.csv', 'a+', newline='', encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerow(data)
        #close the tab
        time.sleep(3)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        i +=1
        gem += 1
    try:
        time.sleep(5)   
        driver.find_element(By.XPATH,
                            "//li[@class='ais-Pagination-item bg-white text-sm ais-Pagination-item--nextPage border-r border-gray-300']"
                            ).click()
    except:
        print("You already scraped everything!") 
        break;


