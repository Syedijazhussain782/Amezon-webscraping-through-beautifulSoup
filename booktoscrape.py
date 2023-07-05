import requests 
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


import pymongo
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["Bookscrape"]
mycol = mydb["BOOKSCRAPE"]



url="https://books.toscrape.com/"
driver=webdriver.Chrome()
resp=driver.get(url)



for page in range(1, 51):
    data=[]
    print("Page:", page)
    products = driver.find_elements_by_xpath('//article[@class="product_pod"]')

    for product in products:
        Name=product.find_element_by_tag_name('h3')
        link = Name.find_element_by_css_selector("a").get_attribute("href")
        print("BOOK LINK :", link)
        Book_Name = Name.find_element_by_css_selector("a").get_attribute("title")
        print("BOOK_NAME :",Book_Name)
        price=product.find_element_by_xpath('//p[@class="price_color"]').text
        print("PRICE :", price)
        data={
                "Book_Name": Book_Name,
                "Book_link":link,
                "price": price
                
            }
      
        
        X = mycol.insert_one(data)

    # Go to the next page if available
    try:
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "li.next a"))
        )
        next_button.click()
    except:
        break








# # Extract href attributes and their attributes
#     for element in Book_Name:
#         href = element.get_attribute("href")
#         attributes = element.get_attribute("title")
#         print(href, attributes)