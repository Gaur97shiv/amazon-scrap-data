import csv
import os
import time
from selenium import webdriver
from bs4 import BeautifulSoup
#This imports the necessary modules for the web scraping process.
# csv is for writing to CSV files, os is for file path operations,
# time is for pausing the script, selenium is for automating web browser interactions, and BeautifulSoup is for parsing HTML.
driver = webdriver.Chrome()
#This creates an instance of the webdriver class for Chrome.

driver.get("https://www.amazon.in/s?rh=n%3A6612025031&fs=true&ref=lp_6612025031_sar")
#This instructs the driver to navigate to the given Amazon webpage.

time.sleep(5)
#This pauses the script for 5 seconds to wait for the webpage to load.

html = driver.page_source
#This gets the HTML content of the page using the page_source method of the driver object.

soup = BeautifulSoup(html, 'html.parser')
#This creates a BeautifulSoup object with the HTML content and uses the html.parser to parse it.

driver.quit()
#This quits the driver and closes the web browser.

products = []
#This initializes an empty list products to store product details.
for product in soup.findAll('div', attrs={'class': 's-result-item'}):
    #This iterates through all the div tags with class attribute equal to 's-result-item' in the soup object.
    product_name = product.find('h2', attrs={'class': 'a-size-mini'})
    if product_name:
        product_name = product_name.text.strip()
    else:
        product_name = ''
#This finds the first h2 tag with class attribute equal to 'a-size-mini' in the product object and stores its text content in product_name. If it is not found, then product_name is set to an empty string.
    try:
        price = product.find('span', attrs={'class': 'a-price-whole'}).text.strip()
    except AttributeError:
        price = ''
#This tries to find the first span tag with class attribute equal to 'a-price-whole' in the product object and stores its text content in price. If it is not found, then price is set to an empty string.
    try:
        rating = product.find('span', attrs={'class': 'a-icon-alt'})
        if rating:
            rating = rating.text.strip()
        else:
            rating = ''
    except AttributeError:
        rating = ''
#This tries to find the first span tag with no class attribute inside product and stores its text content in rating. If it is not found, then rating is set to an empty string
    try:
        seller_name = product.find('span', attrs={'class': 'a-color-secondary'})
        if seller_name:
            seller_name = seller_name.text.strip()
        else:
            seller_name = ''
    except AttributeError:
        seller_name = ''
#This tries to find the first span tag with class attribute equal to 'a-color-secondary' inside product and stores its text content in seller_name. If it is not found, then seller_name is set to an empty string.


    if 'Currently unavailable' not in product.text:
        products.append([product_name, price, rating, seller_name])


with open('amazon_products.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Product Name', 'Price', 'Rating', 'Seller Name'])
    writer.writerows(products)
#his line writes the extracted product details to a CSV file named 'amazon_products.csv'. The file is opened in write mode with the 'utf-8' encoding, and the writer object is used to write a header row with the column names and then write the product data.
# Print a message to confirm that the data has been written to the CSV file
print("Product details have been written to amazon_products.csv.")
#his line prints a message to the console to confirm that the product details have been successfully written to the CSV file.