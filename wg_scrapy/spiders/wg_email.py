# load modules
import pandas as pd
import smtplib

pd.set_option('display.max_colwidth', -1)


#inputs
keywords = ['cosy']

# load files
df = pd.read_json('wg_results.json')

# check if keyword
text_out_list = []
for index, text in enumerate(df['title'] + ' ' + df['description']):
    for word in keywords:
        if word.lower() in text.lower():
            text_out = str(df.iloc[0]).encode('ascii', 'ignore').decode('ascii')
            text_out_list.append(text)

# check if already emailed



            # if not send email
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login("samuel.king@alumni.ie.edu", "***")

            SUBJECT = "New flat with *** {} *** keyword match!".format(word)
            TEXT = text_out

            msg = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
            print(msg)
            server.sendmail("samuel.king@alumni.ie.edu", "samuel.d.t.king@hotmail.co.uk", msg)
            server.quit()

            #make record of email


            ### MUST REMOVE PASSWORD!!! BEFORE GIT COMMIT !!!!