
# Dependencies
from bs4 import BeautifulSoup
from splinter import Browser 
import requests
import pymongo
import pandas as pd
import time 


def init_browser():
    executable_path = {'executable_path':'chromedriver.exe'}
    return Browser('chrome',**executable_path,headless=False)


def scrape():
    browser = init_browser()
    mars_data = {}
#part1 
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')
    results = soup.find_all(class_ = 'list_text')
    title_list = []
    text_list = []
    for result in results:
        article_titles = result.find_all(class_ = 'content_title')
        for title in article_titles:
            title_list.append(title.text.strip())
        article_text = result.find_all(class_ = 'article_teaser_body')
        for teaser_body in article_text:
            text_list.append(teaser_body.text.strip())
    news_title = title_list[0]
    news_text = text_list[0] 
    mars_data["Ntitle"] = news_title
    mars_data["Ntext"] = news_text
#### JPL Mars Space Images - Featured Image
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    xpath = '//footer//a[@class="button fancybox"]'
    results = browser.find_by_xpath(xpath)
    img = results[0]
    img.click()
    browser.is_element_present_by_css("img.fancybox-image", wait_time=1)
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')
    featured_image_url = soup.find('img',class_ = 'fancybox-image')['src']
    if "http:" not in featured_image_url: featured_image_url = "http://www.jpl.nasa.gov"+featured_image_url
    # featured_image_url
    mars_data["featured_image_url"] = featured_image_url
#### Mars Weather
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')
    tweets = soup.find_all('p')
    for tweet in tweets:
        if 'Sol' in tweet.text:
            mars_weather = tweet.text
            break
    mars_data["mars_weather"] = mars_weather  
    
#### Mars Facts
    url = 'http://space-facts.com/mars/'
    tables = pd.read_html(url)
    df = pd.DataFrame(tables[0])
    df.columns = ["Attribute","Attribute Value"]
    df = df.set_index("Attribute")
    mars_facts = df.to_html(index =True, header =True)
    mars_data["mars_facts"] = mars_facts

### Mars Hemispheres
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    mars_hemis=[]
    for i in range (4):
        time.sleep(2)
        articles = browser.find_by_tag('h3')
        articles[i].click()
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        img_url = soup.find("img", class_="wide-image")["src"]
        if "http:" not in img_url: img_url = "http://astrogeology.usgs.gov"+img_url
        img_title = soup.find("h2",class_="title").text
        dictionary={"title":img_title,"img_url":img_url}
        mars_hemis.append(dictionary)
        browser.back()
    # print(mars_hemis)
    mars_data["mars_hemis"] = mars_hemis
    return mars_data


