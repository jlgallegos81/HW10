{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Mission to Mars"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Prep notebook"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {
    "slideshow": {
     "slide_type": "slide"
    }
   },
   "outputs": [],
   "source": [
    "# Modules\n",
    "import pandas as pd\n",
    "import requests\n",
    "from splinter import Browser\n",
    "from bs4 import BeautifulSoup as bs"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [],
   "source": [
    "#ChromeDriver \n",
    "executable_path = {'executable_path': 'chromedriver'}\n",
    "browser = Browser('chrome', **executable_path, headless = False )"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Scrape news site and pull Mars specific articles."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Mars 2020 Unwrapped and Ready for More Testing\n",
      "In time-lapse video, bunny-suited engineers remove the inner layer of protective foil on NASA's Mars 2020 rover after it was relocated for testing.\n"
     ]
    }
   ],
   "source": [
    "#Connect to NASA Mars news site\n",
    "nasaUrl = 'https://mars.nasa.gov/news'\n",
    "browser.visit(nasaUrl)\n",
    "\n",
    "#Create the HTML object\n",
    "html = browser.html\n",
    "\n",
    "#Time for BeautifulSoup\n",
    "soup = bs(html, 'html.parser')\n",
    "\n",
    "#Look up latest news title and paragraph\n",
    "newsTitle = soup.find('div', class_ = 'content_title').find('a').text\n",
    "newsParagraph = soup.find('div', class_ = 'article_teaser_body').text\n",
    "\n",
    "#See if it worked\n",
    "print(newsTitle)\n",
    "print(newsParagraph)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Scrape for Mars images."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "https://www.jpl.nasa.gov/spaceimages/images/wallpaper/PIA19346-1920x1200.jpg\n"
     ]
    }
   ],
   "source": [
    "#JPL image site\n",
    "pixUrl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'\n",
    "browser.visit(pixUrl)\n",
    "\n",
    "#Create the html object\n",
    "htmlImage = browser.html\n",
    "\n",
    "#Parse with BS\n",
    "soup = bs(htmlImage, 'html.parser')\n",
    "\n",
    "#Featured image\n",
    "featuredImage = soup.find('article')['style'].replace('background-image: url(','').replace(');','')[1:-1]\n",
    "\n",
    "#Main url\n",
    "mainUrl = 'https://www.jpl.nasa.gov'\n",
    "\n",
    "#Create link\n",
    "featuredImage = mainUrl + featuredImage\n",
    "\n",
    "print(featuredImage)\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Scrape twitter for mars weather update."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Mars Weather: \n",
      "InSight sol 316 (2019-10-16) low -101.8ºC (-151.3ºF) high -25.7ºC (-14.3ºF)\n",
      "winds from the SSE at 4.7 m/s (10.5 mph) gusting to 18.2 m/s (40.8 mph)\n",
      "pressure at 7.10 hPapic.twitter.com/tXtGZA6IPW\n"
     ]
    }
   ],
   "source": [
    "#Mars weather twitter\n",
    "marsTwitter = 'https://twitter.com/marswxreport?lang=en'\n",
    "browser.visit(marsTwitter)\n",
    "\n",
    "#Html object\n",
    "htmlMars = browser.html\n",
    "\n",
    "#Noodle time\n",
    "soup = bs(htmlMars, 'html.parser')\n",
    "\n",
    "#Scrape it\n",
    "marsTweets = soup.find_all('div', class_ = 'js-tweet-text-container')\n",
    "\n",
    "#print(marsTweets)\n",
    "\n",
    "#Find related tweets\n",
    "for tweet in marsTweets:\n",
    "    marsWeather = tweet.find('p').text\n",
    "    if \"sol\" and \"pressure\" in marsWeather:\n",
    "        print(f'Mars Weather: \\n{marsWeather}')\n",
    "        break\n",
    "    else:\n",
    "        pass"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Scrape Mars facts."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "                         Mars Value     Earth Values\n",
      "Description                                         \n",
      "Diameter:                  6,779 km        12,742 km\n",
      "Mass:               6.39 × 10^23 kg  5.97 × 10^24 kg\n",
      "Moons:                            2                1\n",
      "Distance from Sun:   227,943,824 km   149,598,262 km\n",
      "Length of Year:      687 Earth days      365.24 days\n",
      "Temperature:          -153 to 20 °C      -88 to 58°C\n"
     ]
    }
   ],
   "source": [
    "#Mars facts url\n",
    "marsFacts = 'https://space-facts.com/mars'\n",
    "\n",
    "#Scrape for Mars facts\n",
    "marsFactsDb = pd.read_html(marsFacts)[0]\n",
    "\n",
    "#print(marsFactsDb)\n",
    "\n",
    "#Pretty up\n",
    "marsFactsDb.columns = ['Description', 'Mars Value', 'Earth Values']\n",
    "marsFactsDb.set_index('Description', inplace = True)\n",
    "\n",
    "print(marsFactsDb)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "'<table border=\"1\" class=\"dataframe\">\\n  <thead>\\n    <tr style=\"text-align: right;\">\\n      <th></th>\\n      <th>Mars Value</th>\\n      <th>Earth Values</th>\\n    </tr>\\n    <tr>\\n      <th>Description</th>\\n      <th></th>\\n      <th></th>\\n    </tr>\\n  </thead>\\n  <tbody>\\n    <tr>\\n      <th>Diameter:</th>\\n      <td>6,779 km</td>\\n      <td>12,742 km</td>\\n    </tr>\\n    <tr>\\n      <th>Mass:</th>\\n      <td>6.39 × 10^23 kg</td>\\n      <td>5.97 × 10^24 kg</td>\\n    </tr>\\n    <tr>\\n      <th>Moons:</th>\\n      <td>2</td>\\n      <td>1</td>\\n    </tr>\\n    <tr>\\n      <th>Distance from Sun:</th>\\n      <td>227,943,824 km</td>\\n      <td>149,598,262 km</td>\\n    </tr>\\n    <tr>\\n      <th>Length of Year:</th>\\n      <td>687 Earth days</td>\\n      <td>365.24 days</td>\\n    </tr>\\n    <tr>\\n      <th>Temperature:</th>\\n      <td>-153 to 20 °C</td>\\n      <td>-88 to 58°C</td>\\n    </tr>\\n  </tbody>\\n</table>'"
      ]
     },
     "execution_count": 8,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "#Convert data to html table\n",
    "marsFactsDb.to_html()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Scrape Hemisphere info"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "https://astrogeology.usgs.gov/cache/images/cfa62af2557222a02478f1fcd781d445_cerberus_enhanced.tif_full.jpg\n",
      "https://astrogeology.usgs.gov/cache/images/3cdd1cbf5e0813bba925c9030d13b62e_schiaparelli_enhanced.tif_full.jpg\n",
      "https://astrogeology.usgs.gov/cache/images/ae209b4e408bb6c3e67b6af38168cf28_syrtis_major_enhanced.tif_full.jpg\n",
      "https://astrogeology.usgs.gov/cache/images/7cf2da4bf549ed01c17f206327be4db7_valles_marineris_enhanced.tif_full.jpg\n"
     ]
    }
   ],
   "source": [
    "#Hemisphere Url\n",
    "marsHemi = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'\n",
    "browser.visit(marsHemi)\n",
    "\n",
    "#One more HTML object\n",
    "htmlHemi = browser.html\n",
    "\n",
    "#Sopita\n",
    "soup = bs(htmlHemi, 'html.parser')\n",
    "\n",
    "#Pull items that contain hemi info\n",
    "marsItems = soup.find_all('div', class_ = 'item')\n",
    "\n",
    "#Create placeholders\n",
    "hemiImages = []\n",
    "#hemiTitles = []\n",
    "\n",
    "#Obtain the images\n",
    "for i in marsItems:\n",
    "#Title    \n",
    "    title = i.find('h3').text\n",
    "#Full res link\n",
    "    baseImageUrl = i.find('a', class_ = 'itemLink product-item')['href']\n",
    "#Main link\n",
    "    hemiMainUrl = 'https://astrogeology.usgs.gov'\n",
    "#Visit full link\n",
    "    browser.visit(hemiMainUrl + baseImageUrl)\n",
    "#Another html object\n",
    "    hemiImageHtml = browser.html\n",
    "\n",
    "#Ramen time\n",
    "    soup = bs(hemiImageHtml, 'html.parser')\n",
    "    \n",
    "#Full size image source\n",
    "    imageUrl = hemiMainUrl + soup.find('img', class_ = 'wide-image')['src']\n",
    "    \n",
    "#Lets put it all together now\n",
    "    hemiImages.append({'title': title, 'imageUrl' : imageUrl})\n",
    "    #hemiTitles.append({'title': title})\n",
    "    #print(f'{title}')\n",
    "    print(f'{imageUrl}')\n",
    "    "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "[{'title': 'Cerberus Hemisphere Enhanced',\n",
       "  'imageUrl': 'https://astrogeology.usgs.gov/cache/images/cfa62af2557222a02478f1fcd781d445_cerberus_enhanced.tif_full.jpg'},\n",
       " {'title': 'Schiaparelli Hemisphere Enhanced',\n",
       "  'imageUrl': 'https://astrogeology.usgs.gov/cache/images/3cdd1cbf5e0813bba925c9030d13b62e_schiaparelli_enhanced.tif_full.jpg'},\n",
       " {'title': 'Syrtis Major Hemisphere Enhanced',\n",
       "  'imageUrl': 'https://astrogeology.usgs.gov/cache/images/ae209b4e408bb6c3e67b6af38168cf28_syrtis_major_enhanced.tif_full.jpg'},\n",
       " {'title': 'Valles Marineris Hemisphere Enhanced',\n",
       "  'imageUrl': 'https://astrogeology.usgs.gov/cache/images/7cf2da4bf549ed01c17f206327be4db7_valles_marineris_enhanced.tif_full.jpg'}]"
      ]
     },
     "execution_count": 13,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "hemiImages\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
