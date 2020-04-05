#!/usr/bin/env python3
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from selenium.webdriver import Chrome, ChromeOptions, Remote
from time import sleep
import configparser
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


# 設定ファイル読み取り
def _get(inifile, section, name):
  try:
    return inifile.get(section, name)
  except Exception as err:
    return "error: could not read " + name
# ランダム間隔
def _getRandomNum():
    return random.randint(3,7)
# 楽天検索
def execSearch(browser: webdriver, inifile):
    browser.get(_get(inifile, 'search', 'url'))
    # 検索ワード抽出
    contents = browser.find_elements_by_class_name(_get(inifile, 'search', 'search_class'))
    searchWords = []
    for content in contents:
        values = content.get_attribute("value")
        searchWords.append(values)

    # ログインボタンの押下(楽天検索、メールDEポイント共通)
    browser.find_element_by_link_text(_get(inifile, 'search', 'login_context')).click()
    sleep(_getRandomNum())

    login_user = browser.find_element_by_name(_get(inifile, 'user', 'id_name'))
    login_user.send_keys(_get(inifile, 'user', 'id'))
    login_password = browser.find_element_by_name(_get(inifile, 'user', 'pass_name'))
    login_password.send_keys(_get(inifile, 'user', 'pass'))
    browser.find_element_by_name("submit").click()
    sleep(_getRandomNum())

    ## 検索ワードを一つずつ処理
    for index, searchWord in enumerate(searchWords):
        search_box = browser.find_element_by_name("qt")
        search_box.clear()
        search_box.send_keys(searchWord)
        if index == 0:
            browser.find_element_by_id('search-submit').submit()
        else:
            browser.find_element_by_id('searchBtn').click()
        sleep(_getRandomNum())

# 楽天検索
def execMailDePoint(browser: webdriver, inifile):
    browser.get(_get(inifile, 'mailde', 'url_list'))
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "listCont"))
    )
    # 未読詳細ページ一覧取得
    pointlists = browser.find_elements_by_css_selector('li.unread div.listCont a')
    urlLinkList = []
    for index, point in enumerate(pointlists):
        url = point.get_attribute("href")
        urlLinkList.append(url)

    #　各リンク毎にリンク押下
    for index, linkUrl in enumerate(urlLinkList):
        browser.get(linkUrl)
        try:
            linkText = browser.find_element_by_css_selector('.frameInner div div div a').get_attribute("href")
            browser.get(linkText)
        except NoSuchElementException as te:
            print(linkUrl)

if __name__ == '__main__':
    # Chromeの日本語
    options = ChromeOptions()
    options.add_experimental_option('prefs', {'intl.accept_languages': 'ja'})

    inifile = configparser.ConfigParser()
    inifile.read("/app/login/setting.ini")
    try:
        # HEADLESSブラウザに接続
        browser = webdriver.Remote(
            command_executor='http://selenium-hub:4444/wd/hub',
            desired_capabilities=options.to_capabilities())

        # 楽天検索
        execSearch(browser, inifile)

        # メールでポイント
        execMailDePoint(browser, inifile)

    finally:
        # 終了
        browser.close()
        browser.quit()
