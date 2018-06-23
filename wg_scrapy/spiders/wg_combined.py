import datetime
import scrapy
from scrapy.crawler import CrawlerProcess
import os
from os.path import exists
import re

numbers = re.compile('\d+(?:\.\d+)?')

# INPUTS
#category_input = str(2)
#from_date_input = '15-07-2018'
#to_date_input = '22-10-2018'
output_json = 'wg_results.json'

# FUNCTIONS

def convert_date_to_ten_digit_code(date):
    import time
    tm = time.strptime(date, '%d-%m-%Y')
    time = time.mktime(tm)
    time_int = int(time)
    time_str = str(time_int)
    return time_str

# CONVERT INPUTS

# category = str(category_input)
# from_date = convert_date_to_ten_digit_code(from_date_input)
# to_date = convert_date_to_ten_digit_code(to_date_input)

# CALL URL

#generic_url = "https://www.wg-gesucht.de/wohnungen-in-Berlin.8.2.1.0.html?offer_filter=1&noDeact=1&city_id=8&category={}&rent_type=0&dFr={}&dTo={}"
#full_url = generic_url.format(category,from_date,to_date)
generic_url = 'https://www.wg-gesucht.de/wohnungen-in-Berlin.8.2.1.0.html?offer_filter=1&noDeact=1&city_id=8&category=2&rent_type=0&dFr=1531605600'

start_url = [generic_url]

# delete json
def delete_file(filename):
    if exists(filename):
        try:
            os.remove(filename)
        except OSError as ioe:
            print('File {0} remove has failed. Error: {1}'.format(filename, ioe))

delete_file(output_json)

class CoinMarketCapICOSpider(scrapy.Spider):
    name = 'CMC_ICO_crawler'
    allowed_domains = ['coinmarketcap.com']
    start_urls = start_url

    def parse(self, response):
        time = datetime.datetime.now()
        table = response.xpath('//div[@id="main_column"]')
        rows = table.xpath('//div[@class="panel panel-default  list-details-ad-border"]')
        for row in rows:
            dates = row.css('b::text').extract()
            if len(dates) == 3:
                ava_from = dates[0]
                ava_to = dates[1]
                online_since = dates[2]
            elif len(dates) == 2:
                ava_from = dates[0]
                ava_to = ''
                online_since = dates[1]
            yield {
                'url' : "https://www.wg-gesucht.de/" + str(row.css('a::attr(href)').extract_first()),
                'size' : float(numbers.findall(str(row.css('a::text').extract()[0]).split('|')[0].replace(' ',''))[0]),
                'price': float(numbers.findall(str(row.css('a::text').extract()[0]).split('|')[1].replace(' ', ''))[0]),
                'title': str(row.css('h3').css('a::text').extract_first()).strip(),
                'description': re.sub(' +',' ',str(row.css('p::text').extract_first()).strip()).replace("\n", " "),
                'avalible_from': str(ava_from).replace('Verfügbar:','').replace(' ','').strip(),
                'avalible_to': str(ava_to).replace(' ','').replace('-','').strip(),
                'online_since': online_since.replace('Online:','').replace(' ','').strip(),
            }


if __name__ == "__main__":
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'FEED_FORMAT': 'json',
        'FEED_URI': output_json
    })

    process.crawl(CoinMarketCapICOSpider)
    process.start() # the script will block here until the crawling is finished


###################### EMAIL #############################################

# load modules
import pandas as pd
import smtplib
import datetime
import json
import os
# from googletrans import Translator
# translator = Translator()


pd.set_option('display.max_colwidth', -1)

#inputs
keywords = ['Kreuzberg','Görlitzer Park', 'Neukölln','Neukolln','Neukoelln','Dachboden','Attic','Dachgeschosswohnung']

output_json = 'wg_results.json'

with open('../../config/wg_config.json', 'r') as f:
    config_info = json.load(f)

mypassword = config_info['email_password']
from_email = config_info['from_email']
to_email = config_info['to_email']
to_email2 = config_info['to_email2']

# load files
df = pd.read_json(output_json)

# check if already sent
dir_path = 'wg_sent_list.csv'
if os.path.exists(dir_path) and os.access(dir_path, os.R_OK):
    df_sent = pd.read_csv(dir_path)
    df = df[~df['url'].isin(list(df_sent['url']))]
else:
    df_sent = pd.DataFrame()

# check if keyword
text_out_list = []
df_sent = pd.DataFrame()
for index, text in enumerate(df['title'] + ' ' + df['description']):
    for word in keywords:
        if word.lower() in text.lower():
            text_out = str(df.iloc[index])
            text_out_list.append(text)

            # if not send email
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(from_email, mypassword)

            SUBJECT = "New flat with *** {} *** keyword match!".format(word)
            #TEXT = translator.translate(text_out, src='de',dest='en')
            TEXT = text_out

            msg = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
            msg = msg.encode('utf-8')
            print(msg)
            server.sendmail(from_email, to_email, msg)
            #server.sendmail(from_email, to_email2, msg)
            server.quit()

            df_temp = df.iloc[index]
            df_temp['alert_status'] = 'alert sent'
            df_temp['alert_time'] = str(datetime.datetime.now())
            df_sent = df_sent.append(df_temp)

#make record of email sent
if os.path.exists(dir_path) and os.access(dir_path, os.R_OK):
    with open(dir_path, 'a') as f:
        df_sent.to_csv(f, header=False,index=False)
else:
    df_sent.to_csv(dir_path,index=False)


