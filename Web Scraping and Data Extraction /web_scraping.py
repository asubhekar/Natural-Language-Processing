# -*- coding: utf-8 -*-
"""Web_Scraping.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1KGYYkX-d3vmMxdQYTwLBklk8yQOVqBcd

# <center>Web Scraping</center>

<div class="alert alert-block alert-warning">Each assignment needs to be completed independently. Never ever copy others' work or let someone copy your solution (even with minor modification, e.g. changing variable names). Anti-Plagiarism software will be used to check all submissions. No last minute extension of due date. Be sure to start working on it ASAP! </div>

## Collecting Movie Reviews

Write a function `getReviews(url)` to scrape all **reviews on the first page**, including,
- **title** (see (1) in Figure)
- **reviewer's name** (see (2) in Figure)
- **date** (see (3) in Figure)
- **rating** (see (4) in Figure)
- **review content** (see (5) in Figure. For each review text, need to get the **complete text**.)
- **helpful** (see (6) in Figure).


Requirements:
- `Function Input`: book page URL
- `Function Output`: save all reviews as a DataFrame of columns (`title, reviewer, rating, date, review, helpful`). For the given URL, you can get 24 reviews.
- If a field, e.g. rating, is missing, use `None` to indicate it.

    
![alt text](IMDB.png "IMDB")
"""

from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

import requests
import pandas as pd
import re

from bs4 import BeautifulSoup
# Add your import statements

page = requests.get(page_url)

def getReviews(page_url):

    reviews = None
    #print(page.text)
    movie_r = []
    dates_r = []
    reviewer_r = []
    title_r = []
    review_r = []
    helpful_r = []
    rating_r = []


    soup = BeautifulSoup(page.content, 'html.parser')
    movie_title = soup.find_all('a', itemprop = 'url')
    for movie in movie_title:
        movie_r.append(movie.text)
    print(movie_r[0])


    reviewer = soup.find_all('span', class_ ='display-name-link')
    ratings = soup.find_all('div', class_ = 'ipl-ratings-bar')
    dates = soup.find_all('span', class_ = 'review-date')
    review_title = soup.find_all('a', class_ = 'title')
    act_review = soup.find_all('div', class_= 'text show-more__control')
    review_help = soup.find_all('div', class_= 'actions text-muted')
    for title in review_title:
        title = title.text
        title = re.sub(r'^\s+|\s+$','',title)
        title_r.append(title)
    for rating in ratings:
        rating = rating.text
        rating = re.sub(r'^\s+|\s+$','', rating)
        rating_r.append(rating)
    for review in reviewer:
        reviewer_r.append(review.text)
    for date in dates:
        dates_r.append(date.text)
    for act in act_review:
        act = act.text
        act = re.sub(r'^\s+|\s+$','',act)
        review_r.append(act)
    for hel in review_help:
        hel = hel.text.split('.')[0]
        hel = re.sub(r'^\s+|\s+$','', hel)
        helpful_r.append(hel)



    df = pd.DataFrame()
    df["Title"] = title_r
    df["Reviewer"] = reviewer_r
    df["Ratings"] = rating_r
    df["Date"] = dates_r
    df["Review"] = review_r
    df["Helpful"] = helpful_r

    reviews = df

    return reviews

# Test your function

page_url = 'https://www.imdb.com/title/tt1745960/reviews?sort=totalVotes&dir=desc&ratingFilter=0'
#reviews = getReviews(page_url)

#print(len(reviews))
reviews

"""## Collect Dynamic Content

Write a function `get_N_review(url, webdriver)` to scrape **at least 100 reviews** by clicking "Load More" button 5 times through Selenium WebDrive,


Requirements:
- `Function Input`: book page `url` and a Selenium `webdriver`
- `Function Output`: save all reviews as a DataFrame of columns (`title, reviewer, rating, date, review, helpful`). For the given URL, you can get 24 reviews.
- If a field, e.g. rating, is missing, use `None` to indicate it.


"""

def getReviews(page_url, driver):

    reviews = None
    driver.get(page_url)
    title_r = []
    reviewer_r = []
    rating_r = []
    dates_r = []
    review_r = []
    helpful_r = []

    for i in range(2):
        time.sleep(0.5)
        more_link=driver.find_element_by_css_selector("button.ipl-load-more__button")
        more_link.click()

        time.sleep(1)

    movie_title = driver.find_elements_by_xpath('.//*[@id="main"]/section/div[1]/div/div/h3/a')
    print(movie_title[0].text)

    rev_title = driver.find_elements_by_css_selector("a.title")
    for title in rev_title:
        title = title.text
        title = re.sub(r'^\s+|\s+$','',title)
        title_r.append(title)

    reviewer = driver.find_elements_by_css_selector("span.display-name-link")
    for rev in reviewer:
        rev = rev.text
        rev = re.sub(r'^\s+|\s+$','',rev)
        reviewer_r.append(rev)

    ratings = driver.find_elements_by_css_selector("span.rating-other-user-rating")
    for rate in ratings:
        rate = rate.text
        rate = re.sub(r'^\s+|\s+$','',rate)
        rating_r.append(rate)

    date = driver.find_elements_by_css_selector("span.review-date")
    for dte in date:
        dte = dte.text
        dte = re.sub(r'^\s+|\s+$','',dte)
        dates_r.append(dte)

    act_review = driver.find_elements_by_css_selector("div.text.show-more__control")
    for act in act_review:
        act = act.text
        act = re.sub(r'^\s+|\s+$','',act)
        review_r.append(act)

    helpful = driver.find_elements_by_css_selector("div.action.text-muted")
    for hel in helpful:
        hel = hel.text.split('.')[0]
        hel = re.sub(r'^\s+|\s+$','',hel)
        helpful_r.append(hel)




    df = pd.DataFrame()
    df["Title"] = title_r
    df["Reviewer"] = reviewer_r
    df["Ratings"] = rating_r
    df["Date"] = dates_r
    df["Reviews"] = review_r
    #df["Helpful"] = helpful_r

    reviews = df
    # add your code here

    return reviews

# Test the function
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
executable_path = 'driver/geckodriver'

driver = webdriver.Safari()

page_url = 'https://www.imdb.com/title/tt1745960/reviews?sort=totalVotes&dir=desc&ratingFilter=0'
reviews = getReviews(page_url, driver)

driver.quit()

#print(len(reviews))
reviews

driver.quit()
