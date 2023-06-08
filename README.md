# Plaquemines Parish Assessor Assessment Listing Scraping with Scrapy

Sample URL
https://plaqueminesassessor.azurewebsites.net/Details?parcelNumber=1622237/0

Steps to run the script:
1. Put all plaqueminesassessor URLs in sns_url.txt file
2. Run the below command to scrape all required fields and save in CSV file.

Use below command in terminal to run script

```
scrapy crawl plaque -O output.csv --nolog
```
