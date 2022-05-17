# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ### Visit the NASA Mars News Site


# Visit the mars nasa news site
url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')


slide_elem.find('div', class_='content_title')


# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### JPL Space Images Featured Image


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup


# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# Use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Facts


df = pd.read_html('https://galaxyfacts-mars.com')[0]

df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)

df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

 # ### Hemispheres


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []


html = browser.html
hemi_soup = soup(html, 'html.parser')

# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.

hemi_name_list_raw = hemi_soup.find_all('h3')
hemi_name_list = []
hemi_list_index = 0

hemi_name_list_raw.pop(-1)


for hemi_name in hemi_name_list_raw:
    hemi_name_list.append(hemi_name.text)


for image in hemi_name_list:
    hemispheres = {}
    # a) click on each hemisphere link
    browser.links.find_by_partial_text(hemi_name_list[hemi_list_index]).click()
    hemi_list_index = hemi_list_index + 1
    #b) navigate to the full-resolution image page
    
    #c) retrieve the full-resolution image URL string and title for the hemisphere image
    html = browser.html
    img_soup = soup(html, 'html.parser')
    img_url_elem = img_soup.find('li')
    img_url_rel = img_url_elem.find('a').get('href')
    img_url = f'https://data-class-mars-hemispheres.s3.amazonaws.com/Mars_Hemispheres/{img_url_rel}'
    
    img_title_elem = img_soup.find('h2')
    img_title = img_title_elem.get_text()
    
    hemispheres['img_url']=img_url
    hemispheres['title']=img_title
    hemisphere_image_urls.append(hemispheres)
    #d) use browser.back() to navigate back to the beginning to get the next hemisphere image
    browser.back()



# 4. Print the list that holds the dictionary of each image url and title.
print(hemisphere_image_urls)


# 5. Quit the browser
browser.quit()





