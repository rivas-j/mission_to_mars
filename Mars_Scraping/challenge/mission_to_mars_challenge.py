{
 "cells": [
  {
   "cell_type": "markdown",
   "id": "7e2cb647",
   "metadata": {},
   "source": [
    "### Beginning of Challenge Code"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "995c5783",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Import Splinter, BeautifulSoup, and Pandas\n",
    "from splinter import Browser\n",
    "from bs4 import BeautifulSoup as soup\n",
    "import pandas as pd\n",
    "from webdriver_manager.chrome import ChromeDriverManager"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "86710ab3",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Set the executable path and initialize Splinter\n",
    "executable_path = {'executable_path': ChromeDriverManager().install()}\n",
    "browser = Browser('chrome', **executable_path, headless=False)"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "87d3568d",
   "metadata": {},
   "source": [
    "### Visit the NASA Mars News Site"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "2b655587",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Visit the mars nasa news site\n",
    "url = 'https://redplanetscience.com/'\n",
    "browser.visit(url)\n",
    "\n",
    "# Optional delay for loading the page\n",
    "browser.is_element_present_by_css('div.list_text', wait_time=1)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "b56604db",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Convert the browser html to a soup object and then quit the browser\n",
    "html = browser.html\n",
    "news_soup = soup(html, 'html.parser')\n",
    "\n",
    "slide_elem = news_soup.select_one('div.list_text')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "6e0479c0",
   "metadata": {},
   "outputs": [],
   "source": [
    "slide_elem.find('div', class_='content_title')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "79eb6bb2",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Use the parent element to find the first a tag and save it as `news_title`\n",
    "news_title = slide_elem.find('div', class_='content_title').get_text()\n",
    "news_title"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "962c2981",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Use the parent element to find the paragraph text\n",
    "news_p = slide_elem.find('div', class_='article_teaser_body').get_text()\n",
    "news_p"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "e1d00da1",
   "metadata": {},
   "source": [
    "### JPL Space Images Featured Image"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "5d3a3106",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Visit URL\n",
    "url = 'https://spaceimages-mars.com'\n",
    "browser.visit(url)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "6ba04f9c",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Find and click the full image button\n",
    "full_image_elem = browser.find_by_tag('button')[1]\n",
    "full_image_elem.click()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "45cd49ff",
   "metadata": {
    "scrolled": true
   },
   "outputs": [],
   "source": [
    "# Parse the resulting html with soup\n",
    "html = browser.html\n",
    "img_soup = soup(html, 'html.parser')\n",
    "img_soup"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "b3ecccb2",
   "metadata": {},
   "outputs": [],
   "source": [
    "# find the relative image url\n",
    "img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')\n",
    "img_url_rel"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "b1fb889a",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Use the base url to create an absolute url\n",
    "img_url = f'https://spaceimages-mars.com/{img_url_rel}'\n",
    "img_url"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "3f4f5a9e",
   "metadata": {},
   "source": [
    "### Mars Facts"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "00f87304",
   "metadata": {},
   "outputs": [],
   "source": [
    "df = pd.read_html('https://galaxyfacts-mars.com')[0]\n",
    "df.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "1f23a360",
   "metadata": {},
   "outputs": [],
   "source": [
    "df.columns=['Description', 'Mars', 'Earth']\n",
    "df.set_index('Description', inplace=True)\n",
    "df"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "728b712a",
   "metadata": {},
   "outputs": [],
   "source": [
    "df.to_html()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "b1c54d65",
   "metadata": {},
   "source": [
    "# D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "63897401",
   "metadata": {},
   "source": [
    "### Hemispheres"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "0692b795",
   "metadata": {},
   "outputs": [],
   "source": [
    "# 1. Use browser to visit the URL \n",
    "url = 'https://marshemispheres.com/'\n",
    "\n",
    "browser.visit(url)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "1a67b2eb",
   "metadata": {},
   "outputs": [],
   "source": [
    "# 2. Create a list to hold the images and titles.\n",
    "hemisphere_image_urls = []"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "dc2d7787",
   "metadata": {},
   "outputs": [],
   "source": [
    "html = browser.html\n",
    "hemi_soup = soup(html, 'html.parser')\n",
    "hemi_soup"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "f4fea4cd",
   "metadata": {},
   "outputs": [],
   "source": [
    "# 2. Create a list to hold the images and titles.\n",
    "hemisphere_image_urls = []\n",
    "\n",
    "# 3. Write code to retrieve the image urls and titles for each hemisphere.\n",
    "# class that contains all image page urls: \"collapsible results\"\n",
    "# class that contains url to full size image: \"download\" (1st instance of href)\n",
    "hemi_name_list_raw = hemi_soup.find_all('h3')\n",
    "hemi_name_list = []\n",
    "hemi_list_index = 0\n",
    "\n",
    "hemi_name_list_raw.pop(-1)\n",
    "\n",
    "\n",
    "for hemi_name in hemi_name_list_raw:\n",
    "    hemi_name_list.append(hemi_name.text)\n",
    "hemi_name_list\n",
    "\n",
    "\n",
    "\n",
    "for image in hemi_name_list:\n",
    "    hemispheres = {}\n",
    "    # a) click on each hemisphere link\n",
    "    browser.links.find_by_partial_text(hemi_name_list[hemi_list_index]).click()\n",
    "    hemi_list_index = hemi_list_index + 1\n",
    "    #b) navigate to the full-resolution image page\n",
    "    \n",
    "    #c) retrieve the full-resolution image URL string and title for the hemisphere image\n",
    "    html = browser.html\n",
    "    img_soup = soup(html, 'html.parser')\n",
    "    img_url_elem = img_soup.find('li')\n",
    "    img_url_rel = img_url_elem.find('a').get('href')\n",
    "    img_url = f'https://data-class-mars-hemispheres.s3.amazonaws.com/Mars_Hemispheres/{img_url_rel}'\n",
    "    \n",
    "    img_title_elem = img_soup.find('h2')\n",
    "    img_title = img_title_elem.get_text()\n",
    "    \n",
    "    hemispheres['img_url']=img_url\n",
    "    hemispheres['title']=img_title\n",
    "    hemisphere_image_urls.append(hemispheres)\n",
    "    #d) use browser.back() to navigate back to the beginning to get the next hemisphere image\n",
    "    browser.back()\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "23ceb222",
   "metadata": {
    "scrolled": true
   },
   "outputs": [],
   "source": [
    "# 4. Print the list that holds the dictionary of each image url and title.\n",
    "hemisphere_image_urls"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "7cad302a",
   "metadata": {},
   "outputs": [],
   "source": [
    "# 5. Quit the browser\n",
    "browser.quit()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "3b3cdefd",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "PythonData",
   "language": "python",
   "name": "pythondata"
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
   "version": "3.7.11"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
