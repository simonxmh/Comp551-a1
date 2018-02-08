#!/usr/bin/env python
#-*- coding: utf-8 -*-

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
    starting_link = "http://www.jeuxvideo.com/forums/0-7-0-1-0-1-0-general-jeux-video.htm"
    driver.get(starting_link)

    navButtons = driver.find_elements_by_class_name("pagi-suivant-actif")
    for navButton in navButtons:
        print navButton.text
        while 1:
            topicList=driver.find_element_by_css_selector(".topic-list.topic-list-admin")
            rows = topicList.find_elements_by_css_selector("li")
            for row in rows:
                print row.get_attribute("topic_subject")
                numResponse = row.find_element_by_css_selector("span.topic-count")   
                # .get_attribute('innerText')
                print numResponse.text
                # if 1 < int(numResponse.text) < 300: #less than 300 responses
                #     thread = row.find_element_by_css_selector("span.topic-subject > a")
                #     with open("links-jeuxvideo.txt", "a") as myfile:
                #         myfile.write(thread.get_attribute("href") + "\n")

                #####
                # thread = row.find_element_by_css_selector().text
                # with open("links-jeuxvideo.txt", "a") as myfile:
                #     myfile.write(thread.get_attribute("href") + "\n")
                # #####
            navButton.click()
            time.sleep(1)


def navToLinks(driver):
    with open("links-jeuxvideo.txt", "r") as linkfile:
        with open("jeuxvideo.xml", "a") as convofile:
            numConvos = 0
            convofile.write("<dialog>\n")
            for line in linkfile:
                driver.get(line)

                speakers = []
                content = []

                # if driver.find_element_by_css_selector(".bloc-pseudo-msg"):
                #     opname = driver.find_element_by_css_selector(".bloc-pseudo-msg").text.encode("utf-8")
                #     speakers.append(opname)
                # else:
                #     opname= ""

                #comments = driver.find_element_by_class_name("bloc-message-forum ")

                comment_authors = driver.find_elements_by_css_selector("a.xXx.bloc-pseudo-msg.text-user")
                for i in comment_authors:
                    if i.text not in speakers:
                        speakers.append(i.text.encode("utf-8"))
                print(speakers)

                the_comment_content = driver.find_elements_by_class_name("inner-head-content")
                print len(the_comment_content)
                for j in the_comment_content:
                    the_comment_author = j.find_element_by_css_selector(".bloc-pseudo-msg").text.encode("utf-8")
                    the_comment_text = j.find_element_by_css_selector("div.txt-msg.text-enrichi-forum").text.encode("utf-8")

                    content.append((speakers.index(the_comment_author)+1, the_comment_text))

                if len(content[0]) < 1500: #filters out big image posts
                    convofile.write("<s>")
                    #opcontent
                    convofile.write('<utt uid = "1">')
                    convofile.write(content[0])
                    convofile.write('</utt>')

                    #comment content
                    for comment in content:
                        convofile.write('<utt uid = "'+ str(comment[0]) +'">')
                        paragraphs=comment.find_element_by_css_selector("p")
                        for para in paragraphs:
                            convofile.write(para.text)
                        #convofile.write(comment[1])
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
