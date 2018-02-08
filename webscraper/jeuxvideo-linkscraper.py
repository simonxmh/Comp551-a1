#!/usr/bin/env python
#-*- coding: utf-8 -*-

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

def init_driver():
    path_to_chromedriver = './chromedriver'
    driver = webdriver.Chrome(executable_path = path_to_chromedriver)
    driver.wait = WebDriverWait(driver, 5)
    return driver

def is_element_present(parent, what):
  try: parent.find_element_by_css_selector(what)
  except NoSuchElementException: return False
  return True



def lookupLinks(driver):
    starting_link_1 = "http://www.jeuxvideo.com/forums/0-7-0-1-0-"
    starting_link_2 = "-0-general-jeux-video.htm"
    # driver.get(starting_link_1 + "1"+ starting_link_2)

    i=1
    while 1:
        driver.get(starting_link_1 + str(i) + starting_link_2)
        topicList=driver.find_element_by_css_selector(".topic-list.topic-list-admin")
        rows = topicList.find_elements_by_css_selector("li")
        for row in rows[1:]:
            if is_element_present(row,"span:nth-child(3)") == True:
                numResponse = row.find_element_by_css_selector("span:nth-child(3)")
            else:
                numResponse = 0
            # .get_attribute('innerText')

            # if 1 < int(numResponse.text) < 300: #less than 300 responses
            #     thread = row.find_element_by_css_selector("span.topic-subject > a")
            #     with open("links-jeuxvideo.txt", "a") as myfile:
            #         myfile.write(thread.get_attribute("href") + "\n")

            #####


            # thread = row.find_element_by_css_selector()
            if 1 < numResponse:
                present = is_element_present(row, "a:nth-child(2)")
                if present == True:
                    thread = row.find_element_by_css_selector("a:nth-child(2)")

                print thread.get_attribute("href")
                with open("links-jeuxvideo.txt", "a") as myfile:
                    myfile.write(thread.get_attribute("href").encode("utf-8") + "\n")
            ####

        i += 25
        time.sleep(1)

if __name__ == "__main__":
    driver = init_driver()
    lookupLinks(driver)
    time.sleep(5)
    driver.quit()
