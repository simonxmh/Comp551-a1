#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def init_driver():
    path_to_chromedriver = './chromedriver'
    driver = webdriver.Chrome(executable_path = path_to_chromedriver)
    driver.wait = WebDriverWait(driver, 5)
    return driver


def lookupLinks(driver):
    starting_link = "https://steamcommunity.com/discussions/forum/26"
    driver.get(starting_link)

    navButtons = driver.find_elements_by_class_name("pagebtn")
    for navButton in navButtons:
        print navButton.text
        if navButton.get_attribute("rel")== "next":
            while 1:
                rows = driver.find_elements_by_css_selector("div.forum_topic")
                for row in rows:
                    numResponse = row.find_element_by_class_name("forum_topic_reply_count").text.replace(',', '')
                    if 1 < int(numResponse) < 300: #less than 300 responses
                        thread = row.find_element_by_class_name("forum_topic_overlay")
                        with open("links-steam.txt", "a") as myfile:
                            myfile.write(thread.get_attribute("href") + "\n")
                navButton.click()
                time.sleep(1)


def navToLinks(driver):
    with open("links.txt", "r") as linkfile:
        with open("steam.xml", "a") as convofile:
            numConvos = 0
            convofile.write("<dialog>\n")
            for line in linkfile:
                driver.get(line)

                speakers = []
                content = []

                if driver.find_element_by_css_selector(".forum_op_author"):
                    opname = driver.find_element_by_css_selector(".forum_op_author").text.encode("utf-8")
                    speakers.append(opname)
                else:
                    opname= ""

                comments = driver.find_element_by_class_name("commentthread_comments")

                comment_authors = comments.find_elements_by_css_selector("bdi")
                for i in comment_authors:
                    if i.text not in speakers:
                        speakers.append(i.text.encode("utf-8"))

                the_comment_content = comments.find_elements_by_class_name("commentthread_comment_content")

                for j in the_comment_content:
                    the_comment_author = j.find_element_by_css_selector("bdi").text.encode("utf-8")
                    the_comment_text = j.find_element_by_class_name("commentthread_comment_text").text.encode("utf-8")

                    content.append((speakers.index(the_comment_author)+1, the_comment_text))

                opcontent = driver.find_element_by_css_selector("div.content:nth-child(4)").text.encode("utf-8")

                if len(opcontent) < 1500: #filters out big image posts
                    convofile.write("<s>")
                    #opcontent
                    convofile.write('<utt uid = "1">')
                    convofile.write(opcontent)
                    convofile.write('</utt>')

                    #comment content
                    for comment in content:
                        convofile.write('<utt uid = "'+ str(comment[0]) +'">')
                        convofile.write(comment[1])
                        convofile.write('</utt>')

                    convofile.write("</s>")
                    numConvos = numConvos+1
                driver.implicitly_wait(3)
                print numConvos
            convofile.write("</dialog>\n")


if __name__ == "__main__":
    driver = init_driver()
    lookupLinks(driver)
    #navToLinks(driver)
    time.sleep(5)
    driver.quit()
