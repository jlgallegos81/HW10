#!/usr/bin/env python
# coding: utf-8

# # Mission to Mars

# Prep notebook

# In[2]:


# Modules
import pandas as pd
import requests
from splinter import Browser
from bs4 import BeautifulSoup as bs


# In[3]:


#ChromeDriver 
executable_path = {'executable_path': 'chromedriver'}
browser = Browser('chrome', **executable_path, headless = False )


# Scrape news site and pull Mars specific articles.

# In[4]:


#Connect to NASA Mars news site
nasaUrl = 'https://mars.nasa.gov/news'
browser.visit(nasaUrl)

#Create the HTML object
html = browser.html

#Time for BeautifulSoup
soup = bs(html, 'html.parser')

#Look up latest news title and paragraph
newsTitle = soup.find('div', class_ = 'content_title').find('a').text
newsParagraph = soup.find('div', class_ = 'article_teaser_body').text

#See if it worked
print(newsTitle)
print(newsParagraph)


# Scrape for Mars images.

# In[5]:


#JPL image site
pixUrl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(pixUrl)

#Create the html object
htmlImage = browser.html

#Parse with BS
soup = bs(htmlImage, 'html.parser')

#Featured image
featuredImage = soup.find('article')['style'].replace('background-image: url(','').replace(');','')[1:-1]

#Main url
mainUrl = 'https://www.jpl.nasa.gov'

#Create link
featuredImage = mainUrl + featuredImage

print(featuredImage)


# Scrape twitter for mars weather update.

# In[6]:


#Mars weather twitter
marsTwitter = 'https://twitter.com/marswxreport?lang=en'
browser.visit(marsTwitter)

#Html object
htmlMars = browser.html

#Noodle time
soup = bs(htmlMars, 'html.parser')

#Scrape it
marsTweets = soup.find_all('div', class_ = 'js-tweet-text-container')

#print(marsTweets)

#Find related tweets
for tweet in marsTweets:
    marsWeather = tweet.find('p').text
    if "sol" and "pressure" in marsWeather:
        print(f'Mars Weather: \n{marsWeather}')
        break
    else:
        pass


# Scrape Mars facts.

# In[7]:


#Mars facts url
marsFacts = 'https://space-facts.com/mars'

#Scrape for Mars facts
marsFactsDb = pd.read_html(marsFacts)[0]

#print(marsFactsDb)

#Pretty up
marsFactsDb.columns = ['Description', 'Mars Value', 'Earth Values']
marsFactsDb.set_index('Description', inplace = True)

print(marsFactsDb)


# In[8]:


#Convert data to html table
marsFactsDb.to_html()


# Scrape Hemisphere info

# In[12]:


#Hemisphere Url
marsHemi = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(marsHemi)

#One more HTML object
htmlHemi = browser.html

#Sopita
soup = bs(htmlHemi, 'html.parser')

#Pull items that contain hemi info
marsItems = soup.find_all('div', class_ = 'item')

#Create placeholders
hemiImages = []
#hemiTitles = []

#Obtain the images
for i in marsItems:
#Title    
    title = i.find('h3').text
#Full res link
    baseImageUrl = i.find('a', class_ = 'itemLink product-item')['href']
#Main link
    hemiMainUrl = 'https://astrogeology.usgs.gov'
#Visit full link
    browser.visit(hemiMainUrl + baseImageUrl)
#Another html object
    hemiImageHtml = browser.html

#Ramen time
    soup = bs(hemiImageHtml, 'html.parser')
    
#Full size image source
    imageUrl = hemiMainUrl + soup.find('img', class_ = 'wide-image')['src']
    
#Lets put it all together now
    hemiImages.append({'title': title, 'imageUrl' : imageUrl})
    #hemiTitles.append({'title': title})
    #print(f'{title}')
    print(f'{imageUrl}')
    


# In[13]:


hemiImages





