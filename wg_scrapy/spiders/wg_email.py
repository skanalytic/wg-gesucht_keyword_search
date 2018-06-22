# load modules
import pandas as pd
import smtplib
import datetime

pd.set_option('display.max_colwidth', -1)

import json
import os


with open('../../config/wg_config.json', 'r') as f:
    config_info = json.load(f)

mypassword = config_info['email_password']
from_email = config_info['from_email']
to_email = config_info['to_email']

#inputs
keywords = ['helle']

# load files
df = pd.read_json('wg_results.json')

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
            text_out = str(df.iloc[index]).encode('ascii', 'ignore').decode('ascii')
            text_out_list.append(text)

            # check if already emailed

            # if not send email
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(from_email, mypassword)

            SUBJECT = "New flat with *** {} *** keyword match!".format(word)
            TEXT = text_out

            msg = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
            print(msg)
            server.sendmail(from_email, to_email, msg)
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


