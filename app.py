from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen as uReq
from flask import send_file, make_response
import csv
import pandas as pd

# Initialize the flask
app = Flask(__name__)

# Routing to home page and render index.html
@app.route('/')
def homePage():
    return render_template("index.html")

# Routing to review page
# If there is POST request, render the result.html else for GET render index.html
@app.route('/review',methods=['POST','GET'])
def index():
    if request.method == 'POST':
        try:
            query = request.form['content'].replace(" ","") 
            # edit the q= part in the url and assign the above query to q
            url = f"https://www.flipkart.com/search?q={query}"
            response = requests.get(url)
            soup = BeautifulSoup(response.content,"html.parser")
            navigate = soup.findAll("div", {"class": "_1AtVbE col-12-12"})
            first_item = navigate[3]
            first_item_url = "https://www.flipkart.com" + first_item.div.div.div.a['href']
            response2 = requests.get(first_item_url)
            soup2 = BeautifulSoup(response2.content,"html.parser")    
            # get the full item name
            item_name = soup2.div.div.h1.span.text
            navigate2 = soup2.findAll("div", {"class": "col JOpGWq"})
            # get the link for href which opens the reviews (Overall review)
            links_with_href = navigate2[0].find_all('a', href=True)
            # Get the last occurrence of the <a> tag
            if links_with_href:
                last_link = links_with_href[-1]
                href_value = last_link['href']
            all_reviews_url = "https://www.flipkart.com"+href_value
            response3 = requests.get(all_reviews_url)
            soup3 = BeautifulSoup(response3.content,"html.parser")
            navigate3 = soup3.findAll("div", {"class": "_2MImiq _1Qnn1K"})
            links = navigate3[0].select('nav a')
            titles_of_review = []
            stars_of_review = []
            reviews = []
            reviewers_name = []
            for link in links:
                href = link.get('href')
                pages = "https://www.flipkart.com"+href
                response4 = requests.get(pages)
                soup4 = BeautifulSoup(response4.content,"html.parser")
                navigate4 = soup4.findAll("div", {"class": "_27M-vq"})
                for i in range(len(navigate4)):
                    titles_of_review.append(navigate4[i].div.div.div.p.text)
                    stars_of_review.append(navigate4[i].div.div.div.div.text)
                    reviews.append(navigate4[i].div.div.find_all('div', {'class': ''})[0].div.text)
                    reviewers_name.append(navigate4[i].div.div.find_all('p', {'class': '_2sc7ZR _2V5EHH'})[0].text)

            filename = query + ".csv"
            header = ["Product", "Customer Name", "Rating", "Heading", "Comment"]
            rows = []
            for i in range(len(reviewers_name)):
                row = [item_name, reviewers_name[i], stars_of_review[i], titles_of_review[i], reviews[i]]
                rows.append(row)
            with open(filename, mode='w', newline='', encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(header)  # Write the header row
                writer.writerows(rows)  # Write the data rows
    
            return render_template('result.html', rows=rows[:10], filename=filename)
        except Exception as e:
            print('The Exception message is: ',e)
            return 'something is wrong'
    else:
        return render_template('index.html')

@app.route('/download_csv', methods=['POST'])
def download_csv():
    if request.method == 'POST':
        try:
            filename = request.form['filename']
            # Provide the correct path to the CSV file.
            file_path = f'./{filename}'

            # Serve the file for download.
            response = make_response(send_file(file_path, as_attachment=True))
            response.headers["Content-Disposition"] = f"attachment; filename={filename}"
            return response

        except Exception as e:
            print('The Exception message is: ', e)
            return 'something is wrong'
    else:
        return 'Invalid request method'

if __name__ == "__main__":
    app.run(debug=True)