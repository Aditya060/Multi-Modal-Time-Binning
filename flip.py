# import requests   
# from bs4 import BeautifulSoup as bs 
# import re 
# import nltk
# import matplotlib.pyplot as plt
# from wordcloud import WordCloud
# import os

# #Scraping review using beautifulsoup
# iphone_reviews=[]
# for i in range(1,10):
#   iphone=[]  
#   url="https://www.flipkart.com/apple-iphone-12-black-64-gb/product-reviews/itma2559422bf7c7?pid=MOBFWBYZU5FWK2VP&lid=LSTMOBFWBYZU5FWK2VPFMEI56&marketplace=FLIPKART&page="+str(i)
#   response = requests.get(url)
#   soup = bs(response.content,"html.parser")# creating soup object to iterate over the extracted content 
#   reviews = soup.findAll("p",attrs={"class","_2sc7ZR"})# Extracting the content under specific tags  
#   print(reviews)
#   for i in range(len(reviews)):
#     iphone.append(reviews[i].text)
#   iphone_reviews=iphone_reviews+iphone 
# #here we saving the extracted data 
# with open("macbook.txt","w",encoding='utf8') as output:
#     output.write(str(iphone_reviews))

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import re

# Scraping review using BeautifulSoup
iphone_reviews = []
iphone_ratings = []

for i in range(1, 120):
    url = "https://www.flipkart.com/apple-iphone-12-black-64-gb/product-reviews/itma2559422bf7c7?pid=MOBFWBYZU5FWK2VP&lid=LSTMOBFWBYZU5FWK2VPFMEI56&marketplace=FLIPKART&page=" + str(i)
    response = requests.get(url)
    soup = bs(response.content, "html.parser")  # Creating a soup object to iterate over the extracted content 
    reviews = soup.findAll("p", attrs={"class": "_2sc7ZR"})
    # reviews = soup.findAll("p._2sc7ZR")

    ratings = soup.findAll("div", attrs={"class": "_3LWZlK"})
      # Extracting the content under specific tags  

    for review in reviews:
        iphone_reviews.append(review.text)
        # print (review.text)
        # start_quote_index = review.find('"')
        # end_quote_index = review.rfind('"')
        # print(start_quote_index)
        # print (end_quote_index)
        # if start_quote_index != -1 and end_quote_index != -1:
        #   iphone_reviews.append(review.text[start_quote_index + 1:end_quote_index])

    for rating in ratings:
        iphone_ratings.append(rating.text)

# Create DataFrames for reviews and ratings
reviews_data = {'Reviews': iphone_reviews}
ratings_data = {'Ratings': iphone_ratings}

reviews_df = pd.DataFrame(reviews_data)
ratings_df = pd.DataFrame(ratings_data)

# Save to separate CSV files
reviews_df.to_csv('iphone_reviews.csv', index=False)
ratings_df.to_csv('iphone_ratings.csv', index=False)

# To save to XLSX, you'll need to install openpyxl: pip install openpyxl
# reviews_df.to_excel('iphone_reviews.xlsx', index=False, engine='openpyxl')
# ratings_df.to_excel('iphone_ratings.xlsx', index=False, engine='openpyxl')
