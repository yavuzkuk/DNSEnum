from zoneinfo import reset_tzpath

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from  selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options




def CRTsh(driver,url):
    try:
        subdomains = []
        crtshUrl = "https://crt.sh/?q="

        crtshUrl += url
        driver.get(crtshUrl)

        trTags = driver.find_elements(By.TAG_NAME, value="TR")

        for tr in trTags:
            tdTags = tr.find_elements(By.TAG_NAME, "TD")[4:5]

            for td in tdTags:
                tdText = td.text.strip()
                if str.__contains__(tdText,url):
                    subdomains.append(tdText)

        return  subdomains
    except:
        print("")


def Bing(driver,url):
    subdomains = []
    bingUrl = "https://www.bing.com/search?q=site:"

    bingTargetUrl = bingUrl + url

    driver.get(bingTargetUrl)

    pagination = driver.find_element(By.CSS_SELECTOR,"li.b_pag")

    pagesNumbers = pagination.find_elements(By.CSS_SELECTOR,"li a.b_widePag")

    topNumber = 0
    for number in pagesNumbers:
        if number.text.isnumeric() and int(number.text) > topNumber :
            topNumber = int(number.text)

    if not topNumber == 0:
        topNumber = (topNumber-1)*10+2

        for i in range(1,topNumber,10):
            targetUrl = bingTargetUrl + "&first=" + str(i)

            driver.get(targetUrl)
            urls = driver.find_elements(By.TAG_NAME,"cite")

            for url in urls:
                subdomains.append(url.text.split(" ")[0])

        return  subdomains
    else:
        driver.get(bingTargetUrl)

        urls = driver.find_elements(By.TAG_NAME, "cite")

        for url in urls:
            subdomains.append(url.text.split(" ")[0])

def Google(driver,url):
    subdomains = []
    googleUrl = "https://www.google.com.tr/search?q=inurl:"

    googleTargetUrl = googleUrl+url

    driver.get(googleTargetUrl)

    pagination = driver.find_elements(By.CSS_SELECTOR,"td.NKTSme")

    topNumber = 0
    for number in pagination:
        if int(number.text) > topNumber:
            topNumber = int(number.text)

    if not topNumber == 0:
        for i in range(0,topNumber*10,10):
            targetUrl = googleTargetUrl + "&start=" + str(i)

            driver.get(targetUrl)

            cites = driver.find_elements(By.TAG_NAME, "cite")

            for cite in cites:
                if not cite == " " and url in cite.text:
                    subdomains.append(cite.text.split(" ")[0])
        return  subdomains
    else:
        cites = driver.find_elements(By.TAG_NAME,"cite")

        for cite in cites:
            if not cite == " " and url in cite.text:
                subdomains.append(cite.text.split(" ")[0])
        return  subdomains


def Yahoo(driver,url):
    subdomains = []
    yahooUrl = "https://search.yahoo.com/search?p=indomain:"

    yahooTargetUrl = yahooUrl+url

    driver.get(yahooTargetUrl)

    aTags = driver.find_elements(By.CSS_SELECTOR,"div.pages a")

    topNumber = 0

    for i in aTags:
        if int(i.text) > topNumber:
            topNumber = int(i.text)

    if not topNumber == 0:
        for i in range(1,topNumber*7,7):
            targetUrl = yahooTargetUrl + "&b=" + str(i)

            driver.get(targetUrl)
            hrefTitle = driver.find_elements(By.CSS_SELECTOR,"div.compTitle h3 a span.d-ib")

            for href in hrefTitle:
                if url in href.text:
                    splitHref =  href.text.split(" ")[0]
                    subdomains.append(splitHref)
        return  subdomains
    else:

        driver.get(yahooTargetUrl)

        hrefTitle = driver.find_elements(By.CSS_SELECTOR,"div.compTitle h3 a span.d-ib")

        for href in hrefTitle:
            if url in href.text:
                splitHref = href.text.split(" ")[0]
                subdomains.append(splitHref)
        return  subdomains

def Yandex(driver,url):
    subdomains = []
    yandexUrl = "https://yandex.com.tr/search?text=inurl: "

    yandexTargetUrl = yandexUrl+url

    chrome_options = Options()

    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    driver.get(yandexTargetUrl)

    pagination = driver.find_elements(By.CSS_SELECTOR,"a.Pager-Item")

    topNumber = 0
    for i in pagination:
        if i.text.isnumeric() and int(i.text) > topNumber:
            topNumber = int(i.text)

    if not topNumber == 0:
        for i in range(0,topNumber+1):
            targetUrl = yandexTargetUrl + "&p=" + str(i)

            driver.get(targetUrl)

            bTags = driver.find_elements(By.CSS_SELECTOR,"div.Organic-Subtitle a.Link_theme_outer b")

            for bTag in bTags:
                if url in bTag.text:
                    subdomains.append(bTag.text)

        return  subdomains

    else:
        driver.get(yandexTargetUrl)

        bTags = driver.find_elements(By.CSS_SELECTOR, "div.Organic-Subtitle a.Link_theme_outer b")

        for bTag in bTags:
            if url in bTag.text:
                subdomains.append(bTag.text)

        return subdomains