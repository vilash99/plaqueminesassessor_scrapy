import scrapy

class PlaquemineScrap(scrapy.Spider):
    name = "plaque"

    def start_requests(self):
        file_name = 'sns_url.txt'

        # Read Text file data
        with open(file_name, 'r') as f:
            url_list = f.read().split('\n')

        for current_url in url_list:
            if current_url == "":
                continue

            yield scrapy.http.JsonRequest(url=current_url, callback = self.scrap_data)

    def scrap_data(self, response):
        print("Working URL: " + response.url)

        def clean_data(raw_data):
            """Remove unwanted \r characters from string"""
            try:
                extracted_data = raw_data.replace("\r", "")
            except:
                extracted_data = raw_data

            return extracted_data.strip()

        def extract_with_css(query, index):
            """Extract data using CSS query"""
            extracted_data = ""
            try:
                extracted_data = response.css(query).extract()[index]
                extracted_data = clean_data(extracted_data)
            except:
                extracted_data = ""

            return extracted_data


        def extract_with_xpath(query):
            """Extract data using XPATH query"""
            extracted_data = ""
            try:
                extracted_data = response.xpath(query).get()
                extracted_data = clean_data(extracted_data)
            except:
                extracted_data = ""

            return extracted_data


        yield {
            'URL': response.url,
            'parcel_no' : extract_with_css('div#parcelDetails div span::text', 1),
            'owner_name' : extract_with_css('div[data-group="ownerName"] div span', 1),
            'mailing_address' : extract_with_css('div[data-group="mailingAddress"] div span', 0),
            'ward' : extract_with_css('div[data-group="ward"] div span::text', 0),
            'p_type' : extract_with_css('div[data-group="ptype"] div span', 0),
            'legal' : extract_with_css('div[data-group="legal"] div span', 1),
            'physical_address' : extract_with_css('div[data-group="physicalAddress"] div span', 0),
            'parcel_class' : extract_with_css('div[data-group="items"] table tbody tr td::text', 0),
            'parcel_assessed_value' : extract_with_css('div[data-group="items"] table tbody tr td::text', 1),
            'parcel_assessed_unit' : extract_with_css('div[data-group="items"] table tbody tr td::text', 3),
            'parcel_total' : extract_with_css('div[data-group="items"] table tbody tr.total td::text', 1),
            'parcel_total_unit' : extract_with_css('div[data-group="items"] table tbody tr.total td::text', 3),
            'deeds_type' : extract_with_xpath('//div[3]/div/table/tbody/tr/td[2]/text()'),
            'deeds_date' : extract_with_xpath('//div[3]/div/table/tbody/tr/td[3]'),
            'deeds_amount' : extract_with_xpath('//div[3]/div/table/tbody/tr/td[4]/text()'),
            'owner_primary' : extract_with_css('div[data-group="ownership"] table tbody tr td::text', 2),
            'owner_percent' : extract_with_css('div[data-group="ownership"] table tbody tr td::text', 3),
            'location_subdivision' : extract_with_css('div[data-group="locations"] table tbody tr td::text', 0),
            'taxpayer_tax' : extract_with_css('div[data-group="taxes"] table tbody tr.total td::text', 2),
        }
