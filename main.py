from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import ChromiumOptions
import os
import pandas as pd
import json

class Zoro:
    def launch_chrome(self):
        options = ChromiumOptions()
        # options.add_argument('---headless')
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(2)

    def get_url(self,url):
        print(f"GETTING URL: {url}")
        self.driver.get(url)
    def generate_urls(self):
        file = open("keywords.json")
        load = json.load(file)
        urls = []
        for value in load['keywords']:
            urls.append(f"https://www.zoro.com/search?q={value}")
        return urls
    def scrape_urls(self):
        total_pages_element = self.driver.find_element(By.XPATH,'//span[@data-za="pagination-label"]').text
        split_total_pages = total_pages_element.split(" ")
        total_pages = int(split_total_pages[1])
        print(f"TOTAL PAGES ARE {total_pages}")
        urls = []
        for i in range(1, total_pages + 1):
            current_url = self.driver.current_url
            urls.append(current_url+f"&page={i}")
        urls_2 = []
        for i in urls:
            self.get_url(i)
            try:
                url = WebDriverWait(self.driver,60).until(EC.presence_of_all_elements_located((By.XPATH,'//a[@class="product-image-link"]')))
            except:
                pass
            for u in url:
                urls_2.append(u.get_attribute("href"))
        print(f"TOTAL PRODUCTS ARE {len(urls_2)}")
        return urls_2
    def scrape(self):
        print("SCRAPING DATA")
        data = {'url':[],'brand':[],'title':[],'model':[],'upc':[],'price':[],'stock':[],'min_order_qty':[],'pack_size':[]}
        try:
            brand = self.driver.find_element(By.XPATH,'//a[@data-za="product-brand-name"]').text
            data['brand'].append(brand)
        except:
            data['brand'].append("None")
        try:
            url = self.driver.current_url
            data['url'].append(url)
        except:
            data['url'].append("None")
        try:
            title = self.driver.find_element(By.XPATH,'//h1[@data-za="product-name"]').text
            data['title'].append(title)
        except:
            data['title'].append('None')
        try:
            model = self.driver.find_element(By.XPATH,'//span[@data-za="PDPZoroNo"]').text
            data['model'].append(model)
        except:
            data['model'].append("None")
        try:
            upc = self.driver.find_element(By.XPATH,'//li[@class="product-identifiers__upc-no"]/span').text
            data['upc'].append(upc)
        except:
            data['upc'].append("None")

        try:
            price = self.driver.find_element(By.XPATH,'(//div[@data-za="product-price"])[1]').text
            data['price'].append(price)
        except:
            data['price'].append('None')
        try:
            in_stock = self.driver.find_element(By.XPATH,'//button[@aria-label="Add to Cart, Main Product"]')
            data['stock'].append("in-stock")
        except:
            data['stock'].append("out-of-stock")
        try:
            min_order_qty = self.driver.find_element(By.XPATH,'//div[@class="multiples text-body-1 mb-2"]').text
            data['min_order_qty'].append(min_order_qty)
        except:
            data['min_order_qty'].append('None')
        try:
            pack_size = self.driver.find_element(By.XPATH,'//div[@class="per-unit-price flex text-body-2 inline ml-2"]').text
            data['pack_size'].append(pack_size)
        except:
            data['pack_size'].append("None")
        path = os.listdir()
        if 'data.csv' in path:
            df = pd.DataFrame(data,columns=list(data.keys()))
            df.to_csv(f'data.csv', mode='a',index=False,header=False)
        else:
            df = pd.DataFrame(data, columns=list(data.keys()))
            df.to_csv(f'data.csv', mode='a', index=False, header=True)

if __name__ == '__main__':
    scraper = Zoro()
    scraper.launch_chrome()
    keyword_urls = scraper.generate_urls()
    for keyword_url in keyword_urls:
        scraper.get_url(keyword_url)
        urls = scraper.scrape_urls()
        for u in urls:
            try:
                scraper.get_url(u)
                scraper.scrape()
            except:
                pass
