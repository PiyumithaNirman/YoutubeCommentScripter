from selenium import webdriver
from selenium.common import exceptions
import sys
import time
from openpyxl import Workbook


def scrape(url):
    driver = webdriver.Chrome('C:\webdrivers\chromedriver')

    driver.get(url)
    driver.maximize_window()
    time.sleep(5)

    try:
        title = driver.find_element_by_xpath('//*[@id="container"]/h1/yt-formatted-string').text
        views = driver.find_element_by_xpath(
            '//*[@id="container"]//*[@id="info"]//*[@id="info-text"]//*[@id="count"]/yt-view-count-renderer').text
        date = driver.find_element_by_xpath(
            '//*[@id="container"]//*[@id="info"]//*[@id="date"]/yt-formatted-string').text
        likeNdislike = driver.find_element_by_xpath(
            '//*[@id="container"]//*[@id="info"]//*[@id="menu-container"]//*[@id="menu"]/ytd-menu-renderer//*['
            '@id="top-level-buttons"]').text

        txt = likeNdislike.split()

        comment_section = driver.find_element_by_xpath('//*[@id="comments"]')
    except exceptions.NoSuchElementException:

        error = "Error: Double check selector OR "
        error += "element may not yet be on the screen at the time of the find operation"
        print(error)

    driver.execute_script("arguments[0].scrollIntoView();", comment_section)
    time.sleep(7)

    last_height = driver.execute_script("return document.documentElement.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")

        time.sleep(20)

        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")

    try:
        username_elems = driver.find_elements_by_xpath('//*[@id="author-text"]')
        comment_elems = driver.find_elements_by_xpath('//*[@id="content-text"]')

    except exceptions.NoSuchElementException:
        error = "Error: Double check selector OR "
        error += "element may not yet be on the screen at the time of the find operation"
        print(error)

    print("> VIDEO TITLE: " + title + "\n")
    print("> VIDEO VIEWS: " + views + "\n")
    print("> PUBLISHED DATE: " + date + "\n")
    print("> LIKE: " + txt[0] + "\n")
    print("> DISLIKE: " + txt[1] + "\n")

    print("> USERNAMES & COMMENTS:")

    for username, comment in zip(username_elems, comment_elems):
        print(username.text + ": " + comment.text + "\n")

    driver.close()


if __name__ == "__main__":
    scrape(sys.argv[1])
