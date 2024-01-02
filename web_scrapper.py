import requests
from bs4 import BeautifulSoup
import csv
import os

def download_image(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)

url = input("Enter the URL to scrape quotes and images from: ")

response = requests.get(url)
html = response.content

soup = BeautifulSoup(html, 'html.parser')

quotes = soup.find_all('span', class_='text')
authors = soup.find_all('small', class_='author')
images = soup.find_all('img')

os.makedirs('downloaded_images', exist_ok=True)

with open('quotes_and_images.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Quote', 'Author', 'Image'])

    for quote, author, image in zip(quotes, authors, images):
        img_url = image.get('src')
        if img_url:
            img_filename = os.path.join('downloaded_images', img_url.split('/')[-1])
            download_image(img_url, img_filename)
        else:
            img_filename = "No image"
        
        writer.writerow([quote.text, author.text, img_filename])

print("Quotes and images have been saved to quotes_and_images.csv")
