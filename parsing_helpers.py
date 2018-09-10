from selenium.common.exceptions import NoSuchElementException


def get_sizes(driver):
    available_sizes = []
    sizes_labels = driver.find_elements_by_css_selector("label.product__radio[data-analytics-title='product_size']")
    for label in sizes_labels:
        size_input= label.find_elements_by_xpath("./input")
        for i in size_input:
            if not i.get_attribute("disabled"):
                available_sizes.append(i.get_attribute("value"))
    return available_sizes


def parse_title(driver):
    title = driver.find_element_by_css_selector("h1.header.product__header")
    return title.get_attribute("innerText")

def parse_price(driver):
    pricce_div = driver.find_element_by_css_selector("div.product__price-wrapper")
    price = int(pricce_div.get_attribute("data-product-price")) / 100
    return price


def parse_description(driver):
    description_div = driver.find_element_by_css_selector("#toggle-product__description")
    description = description_div.get_attribute("innerText")
    return description


def parse_spec(driver):
    spec_ul = driver.find_elements_by_css_selector("#toggle-product__specs ul li")
    spec = []
    for li in spec_ul:
        text = li.get_attribute("innerHTML")
        spec.append(text)
    return spec


def parse_color_size(driver):
    color_dict = {}
    colour_buttons = driver.find_elements_by_css_selector("label.product__radio.radio-color")
    for button in colour_buttons:
        colour = button.get_attribute("data-value")
        driver.execute_script("arguments[0].click();", button)
        color_dict[colour] = get_sizes(driver)
    return color_dict



