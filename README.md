# Flipkart review scrapping project using Flask

## Details of step logic for scrpping rating 
1) Go to the flipkart website with query
query = "iphone14"
url = f"https://www.flipkart.com/search?q={query}"
response = requests.get(url)
soup = BeautifulSoup(response.content,"html.parser")

2) Select the first item in the list to get its review (scope: can sort by popularity and then get the review of popular item)
The item can be accessed through <div class="_1AtVbE col-12-12">
Here the first 3 class="_1AtVbE col-12-12" will be for sidebar hence we get the first item details in the 4th class
navigate = soup.findAll("div", {"class": "_1AtVbE col-12-12"})
first_item = navigate[3]

3) Go to the URL for first item 
first_item_url = "https://www.flipkart.com" + first_item.div.div.div.a['href']
response2 = requests.get(first_item_url)
soup2 = BeautifulSoup(response2.content,"html.parser")

4) Get the full name of the item using
item_name = soup2.div.div.h1.span.text

5) The Ratings & Reviews tab is in <div class="col JOpGWq">
navigate2 = soup2.findAll("div", {"class": "col JOpGWq"})

6) From this we need to extract the link for all reviews. The link will be in the last 'a' 
links_with_href = navigate2[0].find_all('a', href=True)
if links_with_href:
    last_link = links_with_href[-1]
    href_value = last_link['href']
all_reviews_url = "https://www.flipkart.com"+href_value
response3 = requests.get(all_reviews_url)
soup3 = BeautifulSoup(response3.content,"html.parser")

7) To fetch the reviews from different pages we need to get the link for the navigation for different pages. The pages navigation is in <div class="_2MImiq _1Qnn1K">
navigate3 = soup3.findAll("div", {"class": "_2MImiq _1Qnn1K"})
links = navigate3[0].select('nav a')

8) From this we can fetch the ratings details
