#!/usr/bin/env python3
from selenium import webdriver

from selenium.webdriver import Chrome, ChromeOptions, Remote
from time import sleep
import configparser
import random
from selenium.common.exceptions import NoSuchElementException

# 設定ファイル読み取り
def _get(inifile, section, name):
  try:
    return inifile.get(section, name)
  except Exception as err:
    return "error: could not read " + name

def _getRandomNum():
    return random.randint(1,4);

def execLogin(browser: webdriver, inifile):

    # Googleにアクセス
    browser.get(_get(inifile, 'init', 'url'))

    # ログインボタンの押下
    browser.find_element_by_link_text(_get(inifile, 'init', 'login_context')).click()
    sleep(_getRandomNum())

    login_user = browser.find_element_by_name(_get(inifile, 'user', 'id_name'))
    login_user.send_keys(_get(inifile, 'user', 'id'))
    login_password = browser.find_element_by_name(_get(inifile, 'user', 'pass_name'))
    login_password.send_keys(_get(inifile, 'user', 'pass'))
    browser.find_element_by_name("submit").click()
    sleep(_getRandomNum())

    ## 任意の処理

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

        # 処理記載
        execLogin(browser, inifile)

    finally:
        # 終了
        browser.close()
        browser.quit()

