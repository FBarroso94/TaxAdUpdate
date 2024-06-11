import logging
import time
import traceback
from types import NoneType
from selenium import webdriver
from selenium.common import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
import keyring
import pandas as pd
from datetime import datetime
import os

now = datetime.now()
pd.reset_option('max_columns')
pd.set_option('display.max_columns', 10)
log_filename = 'session_log_' + now.strftime("%Y%m%d%H%M%S") + '.csv'
process_log_filename = 'process_log_' + now.strftime("%Y%m%d%H%M%S") + '.txt'
f = open(process_log_filename, 'a')

# Edge driver
# from selenium.webdriver.edge.service import Service
# service_obj = Service("/Users/YN557KV/AppData/Local/Programs/MSEdge Webdriver/msedgedriver")
# driver = webdriver.Edge(service=service_obj)
#

# Prompt User to Set Action
iptu_input = ''
while iptu_input != 'a' and iptu_input != 'd':
    os.system('cls')
    iptu_input = input('IPTU: aumenta ou diminui? (A/D)\n').lower()

# Chrome driver
service_obj = Service("C:/_Dev/chrome-webdriver/chromedriver.exe")
driver = webdriver.Chrome(service=service_obj)
# 5 seconds is max timeout
driver.implicitly_wait(7)
# explicit 10s wait
wait_10s = WebDriverWait(driver, 10)
driver.delete_all_cookies()

# Constants

DEFAULT_TEXT = "A Empresa tem convênio com os maiores Bancos do País para aprovação e condução do seu crédito " \
               "imobiliário, sem custo pelo serviço."
TODAY = datetime.strftime(datetime.today(), "%d/%m/%Y")

# Actions

# Credentials
servicename = "EmpresaLogin"
username = "empresa@Empresa.com"
password = keyring.get_password(servicename, username)


def login(web_driver, login_user, login_password):
    print("\t\tOpening Website...", file=f)
    web_driver.get("https://comercial.website.com/")
    web_driver.maximize_window()
    print("\t\tOpened!", file=f)
    web_driver.find_element(By.NAME, "email").send_keys(login_user)
    web_driver.find_element(By.NAME, "password").send_keys(login_password)
    web_driver.find_element(By.XPATH, "//button[@type='submit']").click()
    print("\t\tUsername and password sent. Logging in...", file=f)
    web_driver.find_element(By.CLASS_NAME, "app-header__logo-container")
    print("\t\tLogged!", file=f)
    try:
        if web_driver.find_element(By.XPATH, "//button[@type='button']"):
            element1 = web_driver.find_element(By.XPATH, "//button[@type='button']")
            print("\t\tFound Element1", file=f)
            web_driver.execute_script("arguments[0].click();", element1)
            print("\t\tElement1 Clicked", file=f)
    except NoSuchElementException:
        print("\t\tElement1 Not Found. Moving on...", file=f)
    try:
        if web_driver.find_element(By.XPATH, "//*[@id='privacy-term-alert']/div[2]/button"):
            print("\t\tFound Element2", file=f)
            element2 = web_driver.find_element(By.XPATH, "//*[@id='privacy-term-alert']/div[2]/button")
            web_driver.execute_script("arguments[0].click();", element2)
            print("\t\tElement2 Clicked", file=f)
    except NoSuchElementException:
        print("\t\tElement2 Not Found. Moving on...", file=f)
    try:
        if web_driver.find_element(By.XPATH, "//*[@id='cookie-notifier-cta']"):
            print("\t\tFound Element3", file=f)
            element3 = web_driver.find_element(By.XPATH, "//*[@id='cookie-notifier-cta']")
            web_driver.execute_script("arguments[0].click();", element3)
            print("\t\tElement3 Clicked", file=f)
    except NoSuchElementException:
        print("\t\tElement3 Not Found. Moving on...", file=f)


def navigate_menu_advertising(web_driver):
    # web_driver.find_element(By.ID, "Icons-/-Advertising").click()
    # ads_element_xpath = "//*[@id='app']/div[2]/div[1]/div[2]/div/div[1]/ul/li[3]/div/div/div/div/div/div/span"
    # my_ads_element_xpath = "//*[@id='app']/div[2]/div[1]/div[2]/div/div[1]/ul/li[3]/div/div/div[2]/div/nav/ul/li"

    burger_element_xpath = "//*[@id='burger']/button"
    # my_ads_element_xpath = "//*[@id='app']/div[2]/div[1]/div[1]/div[2]/div/ul/li[2]/a/div/button"
    my_ads_element_xpath = "//*[@id='app']/div[2]/div[1]/div[1]/div[2]/ul/li[2]/div/button"

    print("\t\tWaiting for burger_element...", file=f)
    wait_10s.until(
        expected_conditions.presence_of_element_located((By.XPATH, burger_element_xpath)))
    print("\t\tFound burger_element!", file=f)

    # burger_element = web_driver.find_element(By.XPATH, burger_element_xpath)
    # web_driver.execute_script("arguments[0].click();", burger_element)
    # print("\t\tClicked burger_element!")
    my_ads_element = web_driver.find_element(By.XPATH, my_ads_element_xpath)
    web_driver.execute_script("arguments[0].click();", my_ads_element)
    print("\t\tClicked my_ads_element!", file=f)
    print("\t\tMy Ads page accessed!", file=f)

    try:
        if web_driver.find_element(By.XPATH, "//*[@id='privacy-term-alert']/button"):
            print("\t\tFound New Privacy Term Alert", file=f)
            pta_element = web_driver.find_element(By.XPATH, "//*[@id='privacy-term-alert']/button")
            web_driver.execute_script("arguments[0].click();", pta_element)
            print("\t\tNew Privacy Term Alert Clicked", file=f)
    except NoSuchElementException:
        print("\t\tNew Privacy Term Alert Not Found. Moving on...", file=f)


def access_ad(web_driver, pos):
    position = str(pos)
    xpaths = [
        "//*[@id='top-page']/section/div[3]/div/div/section/div/div/div/div[" + position + "]/div/section/div[2]/section[1]/div/figure/picture/img",
        "//*[@id='app']/div[2]/div[2]/div[1]/section/div[3]/div/div/section/div/div/div/div[" + position + "]/div/section/div[2]/section[1]/div/figure/img",
        "//*[@id='app']/div[2]/div[2]/div[1]/section/div[2]/div/div/section/div/div/div/div[" + position + "]/div/section/div[2]/section[1]/div/figure/img",
        "//*[@id='app']/div[2]/div[2]/div[1]/section/div[2]/div/div/section/div/div/div/div[" + position + "]/section/section/section[2]/section[2]/ul/li[1]/div[1]/div"]

    # old_layout_xpath = "//*[@id='app']/div[2]/div[2]/div[1]/section/div[2]/div/div/section/div/div/div/div[" + position + "]/section/section/section[2]/section[2]/ul/li[1]/div[1]/div"
    # new_layout_xpath = "//*[@id='app']/div[2]/div[2]/div[1]/section/div[2]/div/div/section/div/div/div/div[" + position + "]/div/section/div[2]/section[1]/div/figure/img"

    for xpath in xpaths:
        try:
            wait_10s.until(
                expected_conditions.presence_of_element_located((By.XPATH, xpath)))
            ad_element = web_driver.find_element(By.XPATH, xpath)
            web_driver.execute_script("arguments[0].click();", ad_element)
            time.sleep(1)
            break
        except NoSuchElementException:
            print("\t\tAd Element does not exist - NoSuchElementException", file=f)
        except TimeoutException:
            print("\t\tAd Element timed out - TimeoutException", file=f)


def read_ad_description(web_driver):
    wait_10s.until(
        expected_conditions.presence_of_element_located((By.XPATH,
                                                         "//*[@id='category-3']/section[3]/div/div/div/div/div/textarea"
                                                         )))
    ad_desc = web_driver.find_element(By.XPATH,
                                      "//*[@id='category-3']/section[3]/div/div/div/div/div/textarea").get_attribute(
        "value")
    return ad_desc


def read_ad_iptu(web_driver):
    free_radio_xpath = "//*[@id='category-2']/section[2]/section[2]/section/label[2]/div[1]/input"
    try:
        radio_element = web_driver.find_element(By.XPATH, free_radio_xpath)
        radio_element_selected = radio_element.is_selected()
        if radio_element_selected:
            return radio_element
    except NoSuchElementException:
        print("\t\tIPTU Não Isento - NoSuchElementException", file=f)
    except TimeoutException:
        print("\t\tIPTU Não Isento - TimeoutException", file=f)

    xpaths = ["//*[@id='category-2']/section[2]/section[2]/section/div/div/div/div/div/input",
              "//*[@id='category-2']/section[3]/section[2]/section/div/div/div/div/div/input"]
    for xpath in xpaths:
        try:
            wait_10s.until(
                expected_conditions.presence_of_element_located((By.XPATH, xpath)))
            iptu_element = web_driver.find_element(By.XPATH, xpath)  # .get_attribute("value")
            return iptu_element  # .replace(".", "")
        except NoSuchElementException:
            print("\t\tIptu Element does not exist - NoSuchElementException", file=f)
        except TimeoutException:
            print("\t\tIptu Element timed out - TimeoutException", file=f)


def assess_ad_description(ad_desc):
    try:
        assert DEFAULT_TEXT in ad_desc
    except AssertionError:
        return "Default Text Not Found"
    else:
        return "Default Text Found"


def add_default_text(ad_desc):
    return ad_desc + "\n" + DEFAULT_TEXT


def remove_default_text(ad_desc):
    removed_text = ad_desc.replace(DEFAULT_TEXT, "")
    return removed_text


def get_ad_code(web_driver, pos):
    position = str(pos)
    # Layout antigo, alterado em 03/11/2022
    xpaths = [
        "//*[@id='app']/div[2]/div[2]/div[1]/section/div[3]/div/div/section/div/div/div/div[" + position + "]/div/section/div[2]/section[2]/section[1]/section[1]/span",
        "//*[@id='app']/div[2]/div[2]/div[1]/section/div[2]/div/div/section/div/div/div/div[" + position + "]/section/section/section[1]/div[1]/section[1]/span[1]",
        "//*[@id='app']/div[2]/div[2]/div[1]/section/div[2]/div/div/section/div/div/div/div[" + position + "]/div/section/div[2]/section[2]/section[1]/section[1]/span"]

    # old_layout_xpath = "//*[@id='app']/div[2]/div[2]/div[1]/section/div[2]/div/div/section/div/div/div/div[" + position + "]/section/section/section[1]/div[1]/section[1]/span[1]"
    # new_layout_xpath = "//*[@id='app']/div[2]/div[2]/div[1]/section/div[2]/div/div/section/div/div/div/div[" + position + "]/div/section/div[2]/section[2]/section[1]/section[1]/span"

    for xpath in xpaths:
        try:
            element = web_driver.find_element(By.XPATH, xpath)
            return element.get_attribute("innerHTML").strip()
        except StaleElementReferenceException:
            return "N/A"
        except NoSuchElementException:
            print("\t\tAd Code Element Does Not Exist - NoSuchElementException", file=f)
        except TimeoutException:
            print("\t\tAd Code Element timed out- TimeoutException", file=f)


def check_next_ad_exists(web_driver, pos):
    position = str(pos)
    xpaths = ["//*[@id='app']/div[2]/div[2]/div[1]/section/div[3]/div/div/section/div/div/div/div[" + position + "]",
              "//*[@id='app']/div[2]/div[2]/div[1]/section/div[2]/div/div/section/div/div/div/div[" + position + "]"]
    # current_ad_xpath = "//*[@id='app']/div[2]/div[2]/div[1]/section/div[2]/div/div/section/div/div/div/div[" + position + "]"

    for xpath in xpaths:
        try:
            # wait_10s.until(expected_conditions.presence_of_element_located((By.XPATH, current_ad_xpath)))
            next_ad_element = web_driver.find_element(By.XPATH, xpath)
            if next_ad_element:
                print("\t\tNext Ad Exists", file=f)
                return True
            else:
                print("\t\tNext Ad Does Not Exist - 'Else'", file=f)
                # return False
        except NoSuchElementException:
            print("\t\tNext Ad Does Not Exist - NoSuchElementException", file=f)
            # return False
    return False


def check_next_page_exists(web_driver):
    xpaths = ["//*[@id='app']/div[2]/div[2]/div[1]/section/div[4]/ul/li[6]/button",
              "//*[@id='app']/div[2]/div[2]/div[1]/section/div[3]/ul/li[7]/button"]

    for xpath in xpaths:
        try:
            disabled_btn_attr = web_driver.find_element(By.XPATH, xpath).get_attribute("disabled")
            if type(disabled_btn_attr) == NoneType:
                print("\t\tNext Page Exists", file=f)
                return True
            else:
                print("\t\tNext Page Does Not Exist - 'Else NoneType'", file=f)
        except NoSuchElementException:
            print("\t\tNext Page Does Not Exist - 'NoSuchElementException'", file=f)
    return False


def navigate_to_page(web_driver, page_number):
    page = str(page_number)
    # pagination = web_driver.find_element(By.XPATH, "//*[@id='app']/div[2]/div[2]/div[1]/section/div[3]/ul/li[7]/button")
    # web_driver.execute_script("arguments[0].click();", pagination)]
    web_driver.get("https://comercial.website.com/ZAP_OLX/0/listings?pageSize=10&pageNumber=" + page)
    try:
        if web_driver.find_element(By.XPATH, "//*[@id='privacy-term-alert']/button"):
            print("\t\tFound Privacy Term Alert", file=f)
            element2 = web_driver.find_element(By.XPATH, "//*[@id='privacy-term-alert']/button")
            web_driver.execute_script("arguments[0].click();", element2)
            print("\t\tPrivacy Term Alert Closed", file=f)
    except NoSuchElementException:
        print("\t\tPrivacy Term Alert Not Found. Moving on...", file=f)
    web_driver.find_element(By.CLASS_NAME, "app-header__logo-container")


def update_ad_description(web_driver, text):
    # WAIT FOR 10s - EXPLICIT
    wait_10s.until(
        expected_conditions.presence_of_element_located((By.XPATH,
                                                         "//*[@id='category-3']/section[3]/div/div/div/div/div/textarea"
                                                         )))
    textarea = web_driver.find_element(By.XPATH,
                                       "//*[@id='category-3']/section[3]/div/div/div/div/div/textarea")

    textarea_text = textarea.get_attribute("value")
    # print("\n\ntexto inicial: " + textarea_text + "\n", file=f)
    limit = 3
    count = 1

    while not textarea_text == "":
        textarea.send_keys(Keys.CONTROL + "a")
        textarea.send_keys(Keys.DELETE)
        time.sleep(1)
        textarea_text = textarea.get_attribute("value")
        # print("texto após clear: " + textarea_text + "\n", file=f)
        if textarea_text == "":
            textarea.send_keys(text)
            time.sleep(1)
            # textarea_text = textarea.get_attribute("value")
            # print("texto após send_keys: " + textarea_text + "\n\n", file=f)
            return "Save"
        elif count <= limit:
            count += 1
            continue
        else:
            break

    return "Dont save"


def update_ad_iptu(web_driver, obj, text):
    # WAIT FOR 10s - EXPLICIT
    textarea_text = ""
    try:
        # wait_10s.until(expected_conditions.presence_of_element_located((By.XPATH, xpath)))
        textarea = obj
        textarea_text = textarea.get_attribute("value")
    except NoSuchElementException:
        print("\t\tIptu Element does not exist - NoSuchElementException", file=f)
    except TimeoutException:
        print("\t\tIptu Element timed out - TimeoutException", file=f)

    # print("\n\ntexto inicial: " + textarea_text + "\n", file=f)
    limit = 3
    count = 1

    while not textarea_text == "":
        textarea.send_keys(Keys.CONTROL + "a")
        textarea.send_keys(Keys.DELETE)
        time.sleep(1)
        textarea_text = textarea.get_attribute("value")
        # print("texto após clear: " + textarea_text + "\n", file=f)
        if textarea_text == "":
            textarea.send_keys(text)
            time.sleep(1)
            # textarea_text = textarea.get_attribute("value")
            # print("texto após send_keys: " + textarea_text + "\n\n", file=f)
            return "Save"
        elif count <= limit:
            count += 1
            continue
        else:
            break

    return "Dont save"


def get_ad_last_updated(web_driver, pos):
    position = str(pos)
    # Layout antigo, alterado em 03/11/2022
    xpaths = [
        "//*[@id='top-page']/section/div[3]/div/div/section/div/div/div/div[" + position + "]/div/section/div[2]/section[2]/section[2]/section[2]/div/span[2]",
        "//*[@id='app']/div[2]/div[2]/div[1]/section/div[3]/div/div/section/div/div/div/div[" + position + "]/div/section/div[2]/section[2]/section[2]/section[2]/div/span[2]",
        "//*[@id='app']/div[2]/div[2]/div[1]/section/div[2]/div/div/section/div/div/div/div[" + position + "]/section/section/section[2]/section[1]/p",
        "//*[@id='app']/div[2]/div[2]/div[1]/section/div[2]/div/div/section/div/div/div/div[" + position + "]/div/section/div[2]/section[2]/section[2]/section[2]/div/span[2]",
    ]
    # old_layout_xpath = "//*[@id='app']/div[2]/div[2]/div[1]/section/div[2]/div/div/section/div/div/div/div[" + position + "]/section/section/section[2]/section[1]/p"
    # new_layout_xpath = "//*[@id='app']/div[2]/div[2]/div[1]/section/div[2]/div/div/section/div/div/div/div[" + position + "]/div/section/div[2]/section[2]/section[2]/section[2]/div/span[2]"

    for xpath in xpaths:
        try:
            date_text = web_driver.find_element(By.XPATH, xpath)
            date_text_replaced = date_text.get_attribute('innerHTML').replace("Atualizado em\n", "")
            date_text_replaced = date_text_replaced.replace("Atualizado\n", "")
            date_text_replaced = date_text_replaced.replace("Atualizado em ", "")
            date_text_replaced = date_text_replaced.replace("Atualizado ", "")
            return date_text_replaced
        except NoSuchElementException:
            print("\t\tAd Last Updated Element does not exist - NoSuchElementException", file=f)
        except TimeoutException:
            print("\t\tAd Last Updated Element timed out - TimeoutException", file=f)


def save_ad(web_driver):
    close_xpaths = ["//*[@id='app']/div[2]/span[2]/div",
                    "//*[@id='app']/div[2]/span[2]/div/svg/g/path[2]"]
    found_btn = False
    save_btn = web_driver.find_element(By.XPATH,
                                       "//*[@id='app']/div[2]/div[2]/div[1]/div/div[1]/footer/div/div/button[2]")

    web_driver.execute_script("arguments[0].click();", save_btn)
    time.sleep(2)
    for xpath in close_xpaths:
        try:
            close_btn = web_driver.find_element(By.XPATH, xpath)
            web_driver.execute_script("arguments[0].click();", close_btn)
            found_btn = True
            break
        except NoSuchElementException:
            print("\t\tClose Button Element does not exist - NoSuchElementException", file=f)
        except TimeoutException:
            print("\t\tClose Button Element timed out - TimeoutException", file=f)

    if not found_btn:
        print("\t\tIt was not possible to save Ad", file=f)
        raise NoSuchElementException("Close Button not found")

    # close_btn = web_driver.find_element(By.XPATH, "//*[@id='app']/div[2]/span[2]/div")


def exit_ad(web_driver):
    exit_btn = web_driver.find_element(By.XPATH,
                                       "//*[@id='app']/div[2]/div[2]/div[1]/div/div[1]/footer/div/div/button[1]")
    web_driver.execute_script("arguments[0].click();", exit_btn)

    try:
        confirm_btn = web_driver.find_element(By.XPATH,
                                              "//*[@id='app']/div[2]/div[2]/div[1]/div/div[3]/div/div/div[3]/button[2]")
        web_driver.execute_script("arguments[0].click();", confirm_btn)
    except NoSuchElementException:
        print("\t\t[WARN] exit_ad function did not found confirm_btn element", file=f)
    finally:
        time.sleep(1)


def log_to_file(df, item, page, order, code, assess, url, updated, old_text, new_text):
    # LOGGING ################################################
    df.loc[0, 'item'] = item
    df.loc[0, 'ad_page'] = page
    df.loc[0, 'ad_order'] = order
    df.loc[0, 'ad_code'] = code
    df.loc[0, 'assessment'] = assess
    df.loc[0, 'ad_url'] = url
    df.loc[0, 'ad_last_updated'] = updated
    df.loc[0, 'old_text'] = old_text
    df.loc[0, 'new_text'] = new_text
    df.loc[0, 'datetime'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # if file does not exist write header without indexes
    if not os.path.isfile(log_filename):
        df.to_csv(log_filename, header=True, index=False, index_label=False)
    else:  # else it exists so append without writing the header and indexes
        df.to_csv(log_filename, mode='a', header=False, index=False, index_label=False)
    ##########################################################


def sort_by_newest(web_driver):
    sort_xpaths = {'sort_obj1': "/html/body/div[3]/div[2]/div[2]/div[1]/section/div[2]/section[2]/section/div[1]/label/div/div[2]/select", 'sort_obj2': "//*[@id='297']"}

    try:
        sort_obj = web_driver.find_element(By.XPATH, sort_xpaths['sort_obj1'])
    except NoSuchElementException:
        sort_obj = web_driver.find_element(By.XPATH, sort_xpaths['sort_obj2'])

    sort_select = Select(sort_obj)
    sort_select.select_by_value('updatedAtAsc')


def set_ads_per_page(web_driver, amount):
    amount = str(amount)
    xpaths = {'obj1': "/html/body/div[3]/div[2]/div[2]/div[1]/section/div[2]/section[2]/section/div[2]/label/div/div[2]/select", 'obj2': "//*[@id='486']"}

    try:
        obj = web_driver.find_element(By.XPATH, xpaths['obj1'])
    except NoSuchElementException:
        obj = web_driver.find_element(By.XPATH, xpaths['obj2'])

    select = Select(obj)
    select.select_by_value(amount)


if __name__ == '__main__':
    # STARTING PROCESS ###########################################
    print("===============Robo Empresa --- v2===============", file=f)
    print("===============Session --- " + now.strftime("%Y%m%d%H%M%S") + "===============", file=f)
    print("===============START PROCESS===============", file=f)

    err_count = 0
    err_limit = 3
    item_log_df = pd.DataFrame(
        columns=['item', 'ad_page', 'ad_order', 'ad_code', 'assessment', 'ad_url', 'ad_last_updated', 'old_text',
                 'new_text', 'datetime'])
    ad_order = 1
    ad_page = 1
    item_number = 1

    print("=====LOGIN=====", file=f)
    login(driver, username, password)
    print("=====NAVIGATING MENU ADVERTISING=====", file=f)
    navigate_menu_advertising(driver)
    # sort_by_newest(driver)
    # set_ads_per_page(driver, 100)

    while err_count < err_limit:
        try:
            navigate_to_page(driver, ad_page)
            ##############################################################

            while True:
                if check_next_ad_exists(driver, ad_order):
                    print("=====START OF ITEM=====", file=f)
                    # STARTING CURRENT AD ####################################
                    ad_code = get_ad_code(driver, ad_order)
                    print("\tCode: " + ad_code, file=f)
                    ad_last_updated = get_ad_last_updated(driver, ad_order)
                    print("\tLast Updated: " + ad_last_updated, file=f)
                    ##########################################################

                    # CHECKING IF ALREADY UPDATED - CONTINUE IF TRUE #########
                    # print(datetime.today(), file=f)
                    # print(datetime.strptime(ad_last_updated.strip(), "%d/%m/%Y %H:%M:%S"), file=f)
                    try:
                        timedelta = datetime.today() - datetime.strptime(ad_last_updated.strip(), "%d/%m/%Y %H:%M:%S")
                    except ValueError:
                        timedelta = datetime.today() - datetime.strptime(ad_last_updated.strip(), "%d/%m/%Y %H:%M")

                    # print(timedelta, file=f)
                    # print(str(timedelta.days) + "\n", file=f)
                    if timedelta.days < 1:
                        print("\tRecently Updated! Timedelta = 1 > " + str(timedelta.days), file=f)
                        print("=====END OF ITEM=====\n", file=f)
                        assessment = "Recently Updated"
                        log_to_file(item_log_df, item_number, ad_page, ad_order, ad_code, assessment, "N/A",
                                    ad_last_updated,
                                    "N/A", "N/A")
                        ad_order += 1
                        item_number += 1
                        continue
                    ##########################################################

                    access_ad(driver, ad_order)
                    ad_url = driver.current_url
                    print("\tURL: " + ad_url, file=f)

                    # ASSESSMENT WORK - DESCRIPTION ########################################
                    # description = read_ad_description(driver)
                    # print("description:" + description, file=f)
                    # assessment = assess_ad_description(description)
                    # print("\tAssessment: " + assessment, file=f)
                    # if assessment == "Default Text Not Found":
                    #    new_desc = add_default_text(description)
                    #    print("\tDefault Text Added!", file=f)
                    # elif assessment == "Default Text Found":
                    #    new_desc = remove_default_text(description)
                    #    print("\tDefault Text Removed!", file=f)
                    # else:
                    #    new_desc = description
                    #    print("\tText Unaltered!", file=f)

                    # ASSESSMENT WORK - IPTU ###############################################
                    iptu_obj = read_ad_iptu(driver)
                    if iptu_obj.get_attribute("type") == "text":
                        iptu_value = iptu_obj.get_attribute("value").replace(".", "")
                        print("\tIPTU: R$ " + iptu_value, file=f)
                        if iptu_input == "a":
                            new_iptu_value = str(int(iptu_value) + 1)
                            print("\tAdded R$ 1", file=f)
                            assessment = "Added R$ 1"
                        elif iptu_input == "d":
                            new_iptu_value = str(int(iptu_value) - 1)
                            print("\tSubtracted R$ 1", file=f)
                            assessment = "Subtracted R$ 1"
                        else:
                            print("\tUnaltered", file=f)
                            new_iptu_value = iptu_value
                            assessment = "Unaltered"
                    elif iptu_obj.get_attribute("type") == "radio":
                        assessment = "Isento"
                        print("\tEstate IPTU Free! Saving...", file=f)
                        save_ad(driver)
                        # driver.back()
                        print("\tAd Saved! Logging item...", file=f)
                        log_to_file(item_log_df, item_number, ad_page, ad_order, ad_code, assessment,
                                    ad_url,
                                    ad_last_updated, "0", "0")
                        print("\tItem Logged! Backing do ads menu...", file=f)
                        exit_ad(driver)
                        print("\tBack to ads menu", file=f)
                        print("=====END OF ITEM=====\n", file=f)
                        ad_order += 1
                        item_number += 1

                    ##########################################################

                    print("", file=f)

                    # UPDATE AND SAVE WORK - DESCRIPTION ###################################
                    # save_status = update_ad_description(driver, new_desc)
                    # if save_status == "Save":
                    #    print("\tAd Updated! Saving...", file=f)
                    #    save_ad(driver)
                    #    # driver.back()
                    #    print("\tAd Saved! Logging item...", file=f)
                    #    # PREPARE NEXT AD ##########################################
                    #    log_to_file(item_log_df, item_number, ad_page, ad_order, ad_code, assessment, ad_url,
                    #                ad_last_updated,
                    #                description.replace("\n", " "), new_desc.replace("\n", " "))
                    #    print("\tItem logged! Backing do ads menu...", file=f)
                    #    ##########################################################
                    # else:
                    #    log_to_file(item_log_df, item_number, ad_page, ad_order, ad_code, assessment + " | " + save_status,
                    #                ad_url,
                    #                ad_last_updated, description.replace("\n", " "), new_desc.replace("\n", " "))
                    #    print("\tAd Not saved! Item Logged! Backing do ads menu...", file=f)
                    #    exit_ad(driver)

                    # UPDATE AND SAVE WORK - IPTU ###################################
                    save_status = update_ad_iptu(driver, iptu_obj, new_iptu_value)
                    if save_status == "Save":
                        print("\tAd Updated! Saving...", file=f)
                        save_ad(driver)
                        # driver.back()
                        print("\tAd Saved! Logging item...", file=f)
                        # PREPARE NEXT AD ##########################################
                        log_to_file(item_log_df, item_number, ad_page, ad_order, ad_code, assessment, ad_url,
                                    ad_last_updated,
                                    iptu_value, new_iptu_value)
                        print("\tItem logged! Backing do ads menu...", file=f)
                        ##########################################################
                    else:
                        log_to_file(item_log_df, item_number, ad_page, ad_order, ad_code,
                                    assessment + " | " + save_status,
                                    ad_url,
                                    ad_last_updated, iptu_value, new_iptu_value)
                        print("\tAd Not saved! Item Logged! Backing do ads menu...", file=f)
                        exit_ad(driver)
                    ##########################################################

                    # PREPARE NEXT AD ##########################################

                    print("\tBack to ads menu", file=f)
                    print("=====END OF ITEM=====\n", file=f)
                    ad_order += 1
                    item_number += 1
                    ##########################################################

                elif check_next_page_exists(driver):
                    print("==========END OF PAGE==========", file=f)
                    # PREPARE NEXT PAGE ######################################
                    ad_order = 1
                    print("\tNavigating to next page...", file=f)
                    ad_page += 1
                    navigate_to_page(driver, ad_page)
                    ##########################################################
                    print("==========PAGE " + str(ad_page) + "==========", file=f)
                    print(driver.current_url + "\n", file=f)

                else:

                    # END OF PROCESS #########################################
                    print("===============END OF PROCESS===============\n", file=f)
                    driver.close()
                    quit()
                    ##########################################################
        except Exception as e:
            logging.error(traceback.format_exc())
            err_count += 1
            print("\n\n\t\t==============================EXCEPTION CAUGHT. RESTARTING PROCESS. (" + str(
                err_count) + "/" + str(err_limit) + ")==============================\n\n", file=f)
            log_to_file(item_log_df, "N/A", "N/A", "N/A", "N/A",
                        "Exception Caught. " + repr(e) + " (" + str(err_count) + "/" + str(err_limit-1) + ")",
                        "N/A",
                        "N/A",
                        "N/A", "N/A")
            ad_order += 1
            # driver.quit()
            # time.sleep(10)
            # Chrome driver
            # service_obj = Service("/_Dev/chrome-webdriver/chromedriver")
            # driver = ""
            # driver = webdriver.Chrome(service=service_obj)
            # 5 seconds is max timeout
            # driver.implicitly_wait(7)
            # explicit 10s wait
            # wait_10s = WebDriverWait(driver, 10)
            # driver.delete_all_cookies()
    driver.quit()
    f.close()
