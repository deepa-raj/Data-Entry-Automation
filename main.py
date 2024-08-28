
from selenium.common import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import requests
import lxml
from dotenv import load_dotenv
import os
load_dotenv()

google_form_link = os.getenv("GOOGLE_FORM")

GOOGLE_FORM = google_form_link

PRICE = "PropertyCardWrapper__StyledPriceLine" #class
ADDRESS = "property-card-addr" #class
LINK = "property-card-link" #class

URL = "https://appbrewery.github.io/Zillow-Clone/"



# Part 1 - Scrape the links, addresses, and prices of the rental properties

header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}

response = requests.get(url=URL, headers=header)
data = response.text

soup = BeautifulSoup(data, parser="html", features="lxml")
print(soup.prettify())


print("-----------------------------------------------------------------------\n")
print("-----------------------------------------------------------------------\n")
print("-----------------------------------------------------------------------\n")
print("-----------------------------------------------------------------------\n")
print("-----------------------------------------------------------------------\n")
print("-----------------------------------------------------------------------\n")
print("-----------------------------------------------------------------------\n")
print("-----------------------------------------------------------------------\n")
print("-----------------------------------------------------------------------\n")

all_link_elements = soup.select(".StyledPropertyCardDataWrapper a")
all_links = [link["href"] for link in all_link_elements]
print(f"There are {len(all_links)} links to individual listings in total: \n")
print(all_links)

all_address_element = soup.select(".StyledPropertyCardDataWrapper address")
all_addresses = [address.get_text().replace("|", " ").strip() for address in all_address_element]
print(f"\n After having been cleaned up, the {len(all_addresses)} addresses now look like this: \n")
print(all_addresses)

all_price_elements = soup.select(".PropertyCardWrapper span")
all_prices = [price.getText().replace("/mo", "").split("+")[0] for price in all_price_elements if "$" in price.text]
print(f"\n After having been cleaned up, the {len(all_prices)} prices now look like this: \n")
print(all_prices)




# Optional - Keep the browser open (helps diagnose issues if the script crashes)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)


for n in range(len(all_links)):
    driver.get(GOOGLE_FORM)
    time.sleep(2)

    address = driver.find_element(by=By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price = driver.find_element(by=By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link = driver.find_element(by=By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit = driver.find_element(by=By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')

    address.send_keys(all_addresses[n])
    time.sleep(1)
    price.send_keys(all_prices[n])
    time.sleep(1)
    link.send_keys(all_links[n])
    time.sleep(1)
    submit.click()
