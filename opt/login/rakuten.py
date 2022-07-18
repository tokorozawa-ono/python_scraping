#!/usr/bin/env python3
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from time import sleep
import configparser
import random
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

lotinfo = {
    'pay': {
        'title':'楽天Pay',
        'url': 'https://kuji.rakuten.co.jp/38c3861fdc?scid=su_1129',
        'element': '//*[@id="entry"]',
    },
    'Edy': {
        'title': '楽天Edy',
        'url': 'https://kuji.rakuten.co.jp/889373540e',
        'element': '//*[@id="entry"]',
    },
    'Infoseek': {
        'title': '楽天Infoseek',
        'url': 'https://kuji.rakuten.co.jp/14d330d3e0',
        'element': '//*[@id="entry"]',
    },
    'car': {
        'title': '楽天Car保険',
        'url': 'https://kuji.rakuten.co.jp/26d37b04b2',
        'element': '//*[@id="entry"]',
    },
    'openspace': {
        'title': '楽天くじ広場',
        'url': 'https://kuji.rakuten.co.jp/4351057845',
        'element': '//*[@id="entry"]',
    },
    'websearch': {
        'title': '楽天ウェブ検索',
        'url': 'https://kuji.rakuten.co.jp/6e7329f994',
        'element': '//*[@id="entry"]',
    },
    'securities': {
        'title': '楽天証券',
        'url': 'https://kuji.rakuten.co.jp/18584163d',
        'element': '//*[@id="entry"]',
    },
    'estate': {
        'title': '楽天不動産',
        'url': 'https://kuji.rakuten.co.jp/c8437c01c5',
        'element': '//*[@id="entry"]',
    },
    'blog': {
        'title': '楽天ブログ',
        'url': 'https://kuji.rakuten.co.jp/46211bf9dd',
        'element': '//*[@id="entry"]',
    },
}


# 設定ファイル読み取り
def _get(inifile, section, name):
  try:
    return inifile.get(section, name)
  except Exception as err:
    return "error: could not read " + name
# ランダム間隔
def _getRandomNum():
    return random.randint(3,7)
# 楽天ログイン
def execLogin(browser: webdriver, inifile):
    url = _get(inifile, 'login', 'url')
    browser.get(url)
    elem_username = browser.find_element(By.ID,"loginInner_u")
    elem_username.send_keys(_get(inifile, 'user', 'id'))
    elem_password = browser.find_element(By.ID,"loginInner_p")
    elem_password.send_keys(_get(inifile, 'user', 'pass'))
    sleep(1)
    elem_login_btn = browser.find_element(By.NAME, 'submit')
    elem_login_btn.click()
    return browser

# メールDEポイント
def execMailDePoint(browser: webdriver, inifile):
    browser.get(_get(inifile, 'mailde', 'url_list'))
    sleep(10)
    # 未読詳細ページ一覧取得
    pointlists = browser.find_elements(By.CSS_SELECTOR, 'li.unread div.listCont a')
    urlLinkList = []
    for index, point in enumerate(pointlists):
        url = point.get_attribute("href")
        urlLinkList.append(url)

    #　各リンク毎にリンク押下
    for index, linkUrl in enumerate(urlLinkList):
        browser.get(linkUrl)
        try:
            linkText = browser.find_element(By.CSS_SELECTOR, '.frameInner div div div a').get_attribute("href")
            browser.get(linkText)
        except NoSuchElementException as te:
            try:
                browser.find_element(By.CSS_SELECTOR, 'span.point_url').click()
            except NoSuchElementException as te2:
                print(te2)

# くじ
def execLottery(browser: webdriver):
    for key in lotinfo.keys():
        try:
            browser.get(lotinfo[key]['url'])
            sleep(4)
            html = browser.page_source
            # with open('kujipage.html', 'w', encoding='utf-8') as f:
            #     f.write(html)
            frm = browser.find_element(by=By.XPATH, value=lotinfo[key]['element'])
            frm.click()
            sleep(19)
        except Exception as e:
            print(lotinfo[key]['title'])
            print(e)

if __name__ == '__main__':
    # # Chromeの日本語
    # options = webdriver.ChromeOptions()
    options = webdriver.EdgeOptions()
    options.add_argument("--start-maximized")
    options.add_experimental_option('prefs', {'intl.accept_languages': 'ja'})
    options.add_argument("--disable-dev-shm-usage") #chrome bug
    # options.add_argument('--headless')

    # browser = webdriver.Remote(
    #     command_executor='http://standalone-chrome:4444/wd/hub',
    #     options=options)
    browser = webdriver.Remote(
        command_executor='http://standalone-edge:4444/wd/hub',
        options=options)
    inifile = configparser.ConfigParser()
    inifile.read("/app/login/setting.ini")
    try:

        # 共通ログイン
        browser = execLogin(browser, inifile)

        # メールでポイント
        execMailDePoint(browser, inifile)

        # くじ
        execLottery(browser)
    except Exception as e:
        print(e)
    finally:
        if 'browser' in locals() and browser is not None:
            # 終了
            browser.close()
            browser.quit()

