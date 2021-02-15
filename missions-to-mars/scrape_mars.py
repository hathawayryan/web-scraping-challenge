# Dependencies
from bs4 import BeautifulSoup
import requests
import pandas as pd


def scrape():
    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

    # Retrieve page with the requests module
    response = requests.get(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(response.text, 'html.parser')

    #finds the title of this section and stores it as variable
    section = soup.find('div', class_="content_title")
    title = section.text.strip()

    #finds the paragraph description of this section and stores it as variable
    section = soup.find('div', class_="rollover_description_inner")
    paragraph = section.text.strip()

    #uses the url below and scrapes table containing mars data, then exports it to html
    space_facts_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(space_facts_url)
    mars_df = tables[0]
    mars_df.rename(columns={0: "Measurement", 1: "Result"}, inplace = True)
    mars_df.set_index('Measurement', inplace=True)
    mars_df.to_html('mars_table.html')

    html_table = mars_df.to_html()
    html_table = html_table.replace('\n', '')


    #uses url below and find sthe titles of four hemispheres on mars along with links 
    #to high resolution images of each hemisphere, stores these as dictionary
    astrogeology_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    # Retrieve page with the requests module
    response = requests.get(astrogeology_url)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(response.text, 'html.parser')

    images_sections = soup.find_all('div', class_="item")

    hemisphere_links_list = []

    for section in images_sections:
        hemisphere_url = 'https://astrogeology.usgs.gov/' + section.a['href']
        # Retrieve page with the requests module
        temp_response = requests.get(hemisphere_url)

        # Create BeautifulSoup object; parse with 'html.parser'
        temp_soup = BeautifulSoup(temp_response.text, 'html.parser')
        temp_title = section.find('h3').text
        
        temp_download = temp_soup.find('div', class_ = 'downloads')
        temp_li = temp_download.find('li')
        temp_link = temp_li.a['href']
        

        hemisphere_links_list.append({'title': temp_title, 
            'img_url' :temp_link})

    final_dict = {
        "title": title,
        "paragraph": paragraph,
        "table" : html_table,
        "hemisphere_list" : hemisphere_links_list
    }

    return final_dict
    

