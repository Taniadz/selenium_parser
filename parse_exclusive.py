from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from parsing_helpers import *
import json


options = Options()

options.add_argument('--headless')
options.add_argument('--no-sandbox')
driver = webdriver.Chrome(chrome_options=options)


# get page with selected WEB EXCLUSIVES category
driver.get("https://suzyshier.com/collections/sz_trend_online-exclusives")


# get all links from products' grid
products_li = driver.find_elements_by_css_selector("li.grid__item.one-fifth.medium--one-quarter.small--one-half.product-list__item")
links = []
for a in products_li:
    link = a.find_element_by_xpath("./div/a")
    href = link.get_attribute("href")
    links.append(href)


exclusive_category = {}

for link in links:
    driver.get(link)
    driver.implicitly_wait(3)
    title = parse_title(driver)
    exclusive_category[title] = {}

    # check if discount price is present
    try:
        discount = driver.find_element_by_css_selector("span.product__price.product__discount").get_attribute(
            "innerText")
        exclusive_category[title]["discount_price"] = float(discount[1:])    # only integer
        compare_price = driver.find_element_by_css_selector("span.product__compare-at").get_attribute(
            "innerText")
        exclusive_category[title]["price"] = float(compare_price[1:])

    except(NoSuchElementException):
        exclusive_category[title]["discount_price"] = None
        exclusive_category[title]["price"] = parse_price(driver)


driver.close()


with open('parsed_exclusive.json', 'w') as the_file:
    data = json.dumps(exclusive_category, indent=4, sort_keys=True)
    the_file.write(data)




