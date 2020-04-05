#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver import Chrome, ChromeOptions, Remote
from time import sleep
from selenium.webdriver.common.keys import Keys
import configparser
import random

tweet_content = """
これ呟きますー
 """

# 設定ファイル読み取り
def _get(inifile, section, name):
  try:
    return inifile.get(section, name)
  except Exception as err:
    return "error: could not read " + name
# ランダム間隔
def _getRandomNum():
    return random.randint(1,3)
# 自動ツイート
def autotweet(browser: webdriver, inifile):
    browser.get(_get(inifile, 'twitter', 'url'))
    sleep(_getRandomNum())
    # ユーザーid
    user_box = browser.find_element_by_name(_get(inifile, 'user', 'id_name'))
    user_box.send_keys(_get(inifile, 'user', 'id'))
    sleep(_getRandomNum())
    password_box = browser.find_element_by_name(_get(inifile, 'user', 'pass_name'))
    password_box.send_keys(_get(inifile, 'user', 'pass'))
    sleep(_getRandomNum())
    login_btn = browser.find_element_by_xpath(_get(inifile, 'user', 'login_xpath'))
    login_btn.click()
    sleep(_getRandomNum())
    # ツイートフォームの取得
    tweet_box = browser.find_element_by_css_selector(_get(inifile, 'twitter', 'tweet_box_css'))
    tweet_box.click()
    tweet_box.send_keys(tweet_content)
    sleep(_getRandomNum())
    # ツイートする
    tweet_button = browser.find_element_by_xpath(_get(inifile, 'twitter', 'tweet_button_xpath'))
    tweet_button.click()
    sleep(_getRandomNum())

if __name__ == '__main__':
    # Chromeの日本語
    options = ChromeOptions()
    options.add_experimental_option('prefs', {'intl.accept_languages': 'ja'})

    inifile = configparser.ConfigParser()
    inifile.read("/app/sns/setting.ini")
    try:
        # HEADLESSブラウザに接続
        browser = webdriver.Remote(
            command_executor='http://selenium-hub:4444/wd/hub',
            desired_capabilities=options.to_capabilities())
        browser.implicitly_wait(10)
        # 自動ツイート
        autotweet(browser, inifile)

    finally:
        # 終了
        browser.close()
        browser.quit()