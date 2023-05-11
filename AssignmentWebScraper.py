import csv
import json
import requests
from bs4 import BeautifulSoup

#defining the function and introducing api_key and search query to be stored in variables for calling in future
def scrape_google_results():
    api_key = 'RAXTUNKNR665UETR2EFL32DGUZMMV4W77LIB3D31J6UTDKBL74BI5PGOYYEF2TQPNBF68JPOLV9'
    search_query = 'site:youtube.com openinapp.co'

    #There are 100 results per page for google search so we will use the range func. for pages 1-101 
    #(for quick demonstration we will select pages 1&2, can do more it only requires more time and processing power)
    for page in range(1, 3):
        #status indicator, to see which page is being scraped line 13
        print(f'Scraping page {page}...')
        response = requests.get(
            url='https://app.scrapingbee.com/api/v1/',
            params={
                'api_key': api_key,
                'url': f'https://www.google.com/search?q={search_query}&start={(page-1)*10}',
                'custom_google': 'true'
            }
        )
        soup = BeautifulSoup(response.content, 'html.parser')

         #we will use beautifulsoup to extract the URLs of only the youtube channels 
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and ('/channel/' in href or '/c/' in href) and 'youtube.com' in href:
                channel_url = href.split('&')[0].replace('/c/', '/channel/')
                channel_title = link.text.strip()
                print(f'{channel_title}: {channel_url}')
                # now we will write the contents into a CSV file line 33
                with open('WebCrawlerResults.csv', mode='a', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow([channel_title, channel_url])
    print(f'Successfully scraped Google search results to WebCrawlerResults.csv')

scrape_google_results()
