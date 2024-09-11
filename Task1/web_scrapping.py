#import libraries
import requests
import pandas as pd
from bs4 import BeautifulSoup

#define the URL and other parameters
base_url = 'https://www.airlinequality.com/airline-reviews/air-canada'
pages = 10
page_size = 100

#list to store collected reviews
reviews = []

for i in range(1, pages + 1):
    print(f"Scraping page {i}")

    # Create URL to collect links from paginated data
    url = f"{base_url}/page/{i}/?sortby=post_date%3ADesc&pagesize={page_size}"

    #send a GET request
    response = requests.get(url)

    #check if the request was successful
    if response.status_code == 200:
        #parse content using BeautifulSoup
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')

        #Extract reviews from specific div class
        review_divs = soup.find_all('div', {"class": "text_content"})

        # Strip leading/trailing whitespace from the text and append to the list
        for para in review_divs:
            reviews.append(para.get_text(strip=True))

        print(f"   ---> {len(reviews)} total reviews")
    else:
        print(f"Failed to retrieve page {i}, status code: {response.status_code}")
        break

# convert reviews to a DataFrame and save to CSV
df = pd.DataFrame(reviews, columns=['Review'])
df.to_csv('air_canada_reviews.csv', index=False)
