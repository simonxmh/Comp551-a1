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
                try:

                    if is_element_present(driver, ".text-admin") == True:
                        admin = driver.find_elements_by_css_selector(".text-admin")
                        for i in admin:
                            if i.text not in speakers:
                                speakers.append(i.text.encode("utf-8"))

                    if is_element_present(driver, ".text-modo") == True:
                        mods = driver.find_elements_by_css_selector(".text-modo")
                        for i in mods:
                            if i.text not in speakers:
                                speakers.append(i.text.encode("utf-8"))

                    if is_element_present(driver, "div.bloc-pseudo-msg") == True:
                        deleted = driver.find_elements_by_css_selector("div.bloc-pseudo-msg")
                        for i in deleted:
                            if i.text not in speakers:
                                speakers.append(i.text.encode("utf-8"))

                    comment_authors = driver.find_elements_by_css_selector("a.xXx.bloc-pseudo-msg.text-user")
                    for i in comment_authors:
                        if i.text not in speakers:
                            speakers.append(i.text.encode("utf-8"))
                    # print(speakers)

                    the_comment_content = driver.find_elements_by_class_name("inner-head-content")
                    # print len(the_comment_content)
                    for j in the_comment_content:
                        the_comment_author = j.find_element_by_css_selector(".bloc-pseudo-msg").text.encode("utf-8")
                        the_comment_text = j.find_element_by_css_selector("div.txt-msg.text-enrichi-forum").text.encode("utf-8")

                        content.append((speakers.index(the_comment_author)+1, the_comment_text))


                    if len(content[0][1]) < 15000: #filters out big image posts
                        convofile.write("<s>")
                        #opcontent
                        # convofile.write('<utt uid = "1">')
                        # convofile.write(content[0][1])
                        # convofile.write('</utt>')

                        #comment content
                        for comment in content:
                            convofile.write('<utt uid = "'+ str(comment[0]) +'">')
                            convofile.write(comment[1])
                            convofile.write('</utt>')

                        convofile.write("</s>\n")
                        numConvos = numConvos+1
                except NoSuchElementException: continue
                driver.implicitly_wait(1)
                print numConvos
            convofile.write("</dialog>\n")


if __name__ == "__main__":
    driver = init_driver()
    navToLinks(driver)
    time.sleep(5)
    driver.quit()
