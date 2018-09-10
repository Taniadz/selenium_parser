from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

from parsing_helpers import *
import json


options = Options()

options.add_argument('--headless')
options.add_argument('--no-sandbox')
driver = webdriver.Chrome(chrome_options=options)

# get page with selected BOTTOMS category
driver.get("https://suzyshier.com/collections/sz_bottoms_shop-all-bottoms")

# get all links from products' grid
products_li = driver.find_elements_by_css_selector("li.grid__item.one-fifth.medium--one-quarter.small--one-half.product-list__item")
links = []
for a in products_li:
    link = a.find_element_by_xpath("./div/a")
    href = link.get_attribute("href")
    links.append(href)



# click for load second page
next_page_button = driver.find_element_by_css_selector("a.pagination-button.pagination-button-next")
driver.execute_script("arguments[0].click();", next_page_button)

# wait for loading product list
element = WebDriverWait(driver, 10).until(
    EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".product-list__item a"))
)
# get all links from products' grid on the second page
li = driver.find_elements_by_css_selector("li.grid__item.one-fifth.medium--one-quarter.small--one-half.product-list__item")
for a in li:
    link = a.find_element_by_xpath("./div/a")
    href = link.get_attribute("href")
    links.append(href)



bottoms_category = {}

for link in links:
    driver.get(link)
    driver.implicitly_wait(3)
    title = parse_title(driver)
    bottoms_category[title] = {}

    bottoms_category[title]["price"] = parse_prize(driver)
    bottoms_category[title]["description"] = parse_description(driver)
    bottoms_category[title]["spec"] = parse_spec(driver)
    bottoms_category[title]["color"] = parse_color_size(driver)


with open('parsed_bottoms.json', 'w') as the_file:
    data = json.dumps(bottoms_category, indent=4, sort_keys=True)
    the_file.write(data)

driver.close()

