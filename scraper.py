from math import ceil
import time
import json
import re
import Review
import click
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
# from selenium.webdriver.common.keys import Keys

from config import COMPANY_NAME_TO_BASE_URL, USER_SECRETS, number_of_interviews, start_page


# Manual options for the company, num pages to scrape, and URL
pages = 200


def obj_dict(obj):
    return vars(obj)
# return obj.__dict__
# enddef


def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--test-type")
    # options.binary_location = "./chromedriver"
    driver = webdriver.Chrome(
        executable_path="./chromedriver.exe", chrome_options=options)
    # driver.get('https://python.org')

    # driver = webdriver.Chrome(executable_path = "./chromedriver")
    driver.wait = WebDriverWait(driver, 10)
    return driver
# enddef


def login(driver, username, password):
    driver.get("http://www.glassdoor.com/profile/login_input.htm")
    try:
        user_field = driver.wait.until(EC.presence_of_element_located(
            (By.NAME, "username")))

        # pw_field = driver.find_element_by_class_name("signin-password")
        login_button = driver.find_element(
            By.XPATH, '//button[@type="submit"]')

        # login_button = driver.find_element_by_id("signInBtn")
        user_field.send_keys(username)
        # user_field.send_keys(Keys.TAB)
        time.sleep(1)

        login_button.click()
        time.sleep(1)

        pw_field = driver.find_element(By.NAME, 'password')
        pw_field.send_keys(password)
        login_button = driver.find_element(
            By.XPATH, '//button[@type="submit"]')
        login_button.click()
    except TimeoutException:
        print("TimeoutException! Username/password field or login button not found on glassdoor.com")
# enddef


def _get_pagenated_url(base_url, pagestr, idx):
    base = base_url[:idx] + pagestr + base_url[idx+1:]

    print(base)
    pagenated_url = base
    return pagenated_url


def get_data(driver, URL, startPage, endPage, data, refresh, idx):
    print(endPage)
    if (startPage > endPage):
        return data
    # endif
    print("\nPage " + str(startPage) + " of " + str(endPage))
    # currentURL = URL + "_IP" + str(startPage) + ".htm"
    currentURL = _get_pagenated_url(URL, str(startPage), idx)
    time.sleep(5)
    # endif
    if (refresh):
        driver.get(currentURL)
        print("Getting " + currentURL)

    # endif
    time.sleep(5)
    HTML = driver.page_source
    soup = BeautifulSoup(HTML, "html.parser")
    nextpage_node = soup.find('button', attrs={'data-test': 'pagination-next'})
    if nextpage_node is not None and nextpage_node.get('disabled'):
        nextpage_node = None

    reviews_container = soup.find('div', attrs={'data-test': 'InterviewList'})
    reviews = HTML
    if (reviews):
        # print (reviews)

        data.append(reviews)
        print(len(data))
        print("Page " + str(startPage) + " scraped.")

        if nextpage_node is None:
            print('Reached last page: {}'.format(currentURL))
            return data

        if (startPage % 10 == 0):
            print("\nTaking a breather for a few seconds ...")
            time.sleep(12)
        # endif
        get_data(driver, URL, startPage + 1, endPage, data, True, idx)
    else:
        print("Waiting ... page still loading or CAPTCHA input required")
        time.sleep(3)
        get_data(driver, URL, startPage, endPage, data, False, idx)
    # endif
    return data
# enddef


def get_data_for_job_search(driver, URL, startPage, endPage, data, refresh, idx):
    print(endPage)
    if (startPage > endPage):
        return data
    # endif
    print("\nPage " + str(startPage) + " of " + str(endPage))
    # currentURL = URL + "_IP" + str(startPage) + ".htm"
    currentURL = _get_pagenated_url(URL, str(startPage), idx)
    time.sleep(5)
    # endif
    if (refresh):
        driver.get(currentURL)
        print("Getting " + currentURL)

    # endif
    time.sleep(5)
    HTML = driver.page_source
    soup = BeautifulSoup(HTML, "html.parser")
    nextpage_node = soup.find('button', attrs={'data-test': 'pagination-next'})
    if nextpage_node is not None and nextpage_node.get('disabled'):
        nextpage_node = None

    reviews_container = soup.find(
        'div', attrs={'data-test': 'results-container'})
    reviews = str(reviews_container)
    if (reviews):
        # print (reviews)

        data.append(reviews)
        print(len(data))
        print("Page " + str(startPage) + " scraped.")

        if nextpage_node is None:
            print('Reached last page: {}'.format(currentURL))
            return data

        if (startPage % 10 == 0):
            print("\nTaking a breather for a few seconds ...")
            time.sleep(12)
        # endif
        get_data(driver, URL, startPage + 1, endPage, data, True, idx)
    else:
        print("Waiting ... page still loading or CAPTCHA input required")
        time.sleep(3)
        get_data(driver, URL, startPage, endPage, data, False, idx)
    # endif
    return data


def _extract_company_name_map_for_alias(company_alias):
    if company_alias == 'all':
        name_map = COMPANY_NAME_TO_BASE_URL
    else:
        name_map = {}
        name_map[company_alias] = COMPANY_NAME_TO_BASE_URL[company_alias]
    return name_map


def find_idx(company_url: str) -> int:
    match = re.search(r'IP(\d+)', company_url)

    if match:
        index = match.start(1)
        return index
    else:
        return -1


@click.command()
@click.option('--company_names', default='all')
def main(company_names):
    driver = init_driver()
    time.sleep(5)
    print("Logging into Glassdoor account ...")
    login(driver, USER_SECRETS['username'], USER_SECRETS['password'])
    time.sleep(5)
    print("\nStarting data scraping ...")

    company_name_map = _extract_company_name_map_for_alias(company_names)

    for company_name, company_url in company_name_map.items():
        end_page = ceil(number_of_interviews/10)
        idx = find_idx(company_url)
        print(company_url)
        data = get_data_for_job_search(driver, company_url, start_page,
                                       end_page, [], True, idx)
        # data = get_data(driver, companyURL[:-4], 1, pages, [], True)
        file_name = 'items_' + str(company_name)

        with open(file_name+'.json', 'w') as file:
            json.dump(data, file)

        print("\nExporting data to " + file_name + ".json")

    driver.quit()


if __name__ == "__main__":

    main()
# endif
