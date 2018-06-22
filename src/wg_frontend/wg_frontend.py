# OVERALL GOALS

# To find apartments in berlin by keyword (e.g. attic / area) and get alerted as soon as they come up
# Would also be cool to have automated instant replies

# HOW TO BOOTSTRAP IT

# subset in url api call to just berlin and just my dates (can be variables)
# just have something that runs locally and can save output then can figure out the server
# should also spend some time exploring the site to check plan (e.g. do you need to scrape ALL or can you just go to last page)

# COCERNS

# will need to figure out efficient way to deal with translation issue
# Flats and 1-bedroom apartments are seperate things

# BREAKDOWN INTO TASKS

# Explore site
# Explore others git repos

# NOTES


### KEYWORDS

#LOCATION
# Kreuzberg
# Görlitzer Park
# Neukölln


# INPUTS

category_input = str(2)
from_date_input = '15-07-2018'
to_date_input = '22-10-2018'

# FUNCTIONS

def convert_date_to_ten_digit_code(date):
    import time
    tm = time.strptime(from_date_input, '%d-%m-%Y')
    time = time.mktime(tm)
    time_int = int(time)
    time_str = str(time_int)
    return time_str

# CONVERT INPUTS

category = str(category_input)
from_date = convert_date_to_ten_digit_code(from_date_input)
to_date = convert_date_to_ten_digit_code(to_date_input)

# CALL URL

generic_url = "https://www.wg-gesucht.de/wohnungen-in-Berlin.8.2.1.0.html?offer_filter=1&noDeact=1&city_id=8&category={}&rent_type=0&dFr={}&dTo={}"
full_url = generic_url.format(category,from_date,to_date)
print(full_url)

# RETREIVE DATA


# PARSE DATA

# CHECK FOR KEYWORDS

# CHECK IF PREVIOUSLY SENT

# IF NOT, SEND ALERTS

