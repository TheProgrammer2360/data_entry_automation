from bs4 import BeautifulSoup
from selenium import webdriver
from helpers import get_elements
from selenium.webdriver.common.by import By
import time

# using selenium and Beautiful soup
URL = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination" \
      "%22%3A%7B%7D%2C%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122" \
      ".56276167822266%2C%22east%22%3A-122.30389632177734%2C%22south%22%3A37.69261345230467%2C" \
      "%22north%22%3A37.857877098316834%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A" \
      "%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%" \
      "22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%2" \
      "2value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%" \
      "3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2" \
      "C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%" \
      "7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D"
driver = webdriver.Chrome(executable_path="/chromedriver.exe")
driver.get(url=URL)
driver.maximize_window()
# create  soup and then close the driver
soup = BeautifulSoup(driver.page_source, "html.parser")
prices = get_elements(soup, "span", "data-test", "property-card-price")
addresses = get_elements(soup, "address", "data-test", "property-card-addr")
# after every link there empty string, get rid of all empty strings
links_incorrect = get_elements(soup, "a", "class", "property-card-link")
# the links repeat themselfs twice, next to each other
# created a second list that does not have repeated elements
uncleaned_links = [links_incorrect[i] for i in range(0, len(links_incorrect)) if i % 2 == 0]
links = list()
# putting https on links that does not have it
https = "https://www.zillow.com"
for link in uncleaned_links:
    # when the link does not contain https
    if link[0:len(https)] != https:
        link = https + link
    links.append(link)

form_url = "https://docs.google.com/forms/d/e/1FAIpQLSeIg1Mac9uMOdxPmaq4FWIvrlwayiWDKNFXZ30RSxFu71Nc6Q/viewform?usp=sf_link"
driver.get(url=form_url)
# fill the form for all the data
for i in range(0, len(links)):
    # wait 2 seconds and start inputting data, to make the program behave like a human
    time.sleep(2)
    # fill in the first question
    q_xpath = "/html/body/div/div[2]/form/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input"
    a_input = driver.find_element(By.XPATH, q_xpath)
    a_input.send_keys(addresses[i])
    # wait 2 seconds and then fill in the second question
    time.sleep(2)
    q_xpath = "/html/body/div/div[2]/form/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input"
    a_input = driver.find_element(By.XPATH, q_xpath)
    a_input.send_keys(prices[i])
    # wait answer 2 seconds and start filling in the 3rd and last question
    time.sleep(2)
    q_xpath = "/html/body/div/div[2]/form/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input"
    a_input = driver.find_element(By.XPATH, q_xpath)
    a_input.send_keys(links[i])
    # wait one second and then start clicking the submit button
    time.sleep(1)
    q_xpath = "/html/body/div/div[2]/form/div[2]/div/div[3]/div[1]/div[1]/div"
    submit_button = driver.find_element(By.XPATH, q_xpath)
    submit_button.click()
    # wait 2 seconds and then go back to the form
    time.sleep(2)
    q_xpath = "/html/body/div[1]/div[2]/div[1]/div/div[4]/a"
    a_input = driver.find_element(By.XPATH, q_xpath)
    a_input.click()
print("Done with filling all the enteries")

driver.close()
