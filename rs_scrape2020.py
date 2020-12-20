##Rolling Stone EDA##

#Importing Libraries#
import os
import selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import numpy as np

#Setting up Working Directory##
print(os.getcwd())
os.chdir('/Users/brandonnussbaum/Documents/UTHealth/Fall 2020/Data Science/Python/Rolling Stone EDA')

#Setting up the Webdriver to link with the browser and extract our information
#Not using Beautiful Soup because RS uses JavaScript DOM code instead of standard HTML/XML code
driver_path = '/Users/brandonnussbaum/Documents/UTHealth/Fall 2020/Data Science/Python/Rolling Stone EDA/chromedriver'
driver=webdriver.Chrome(driver_path)
driver.get('https://www.rollingstone.com/music/music-lists/best-albums-of-all-time-1062063/') #2020 List

rank_list = []
album_list = []
subtitle_list = []
description_list = []


while True:
    try:
        driver.implicitly_wait(10)
        
        content = driver.find_element_by_id('pmc-gallery-vertical')
        
        articles = content.find_elements_by_tag_name('article')
    
        for article in articles: 
            rank = article.find_element_by_class_name('c-gallery-vertical-album__number')
            rank_list.append(rank.text)
            album = article.find_element_by_class_name('c-gallery-vertical-album__title')
            album_list.append(album.text)
            subtitle = article.find_element_by_class_name('c-gallery-vertical-album__subtitle')
            subtitle_list.append(subtitle.text)
            description = article.find_element_by_class_name('c-gallery-vertical-album__description')
            description_list.append(description.text)
            
        driver.get(driver.find_element_by_link_text('Load More').get_attribute('href'))
        
    except NoSuchElementException:
        print('Scrape Complete')
        break

driver.close()

#Creating Dataframe from lists of extracted data
list_top500_2020 = pd.DataFrame(
   { 'Rank': rank_list,
    'Album': album_list,
    'Subtitle': subtitle_list,
    'Description': description_list }
    )

#Exporting our dataframe to clean in a separate program
list_top500_2020.to_csv('list_top500_2020.csv')